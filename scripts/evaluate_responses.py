#!/usr/bin/env python3
"""
Evaluate LLM responses to medication discernment test cases.

This script analyzes LLM responses to determine if the model successfully
identified fabricated medications in the test prompts.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Tuple


def load_test_cases(filepath: str) -> List[Dict]:
    """Load test cases from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def normalize_medication_name(name: str) -> str:
    """Normalize medication name for comparison."""
    return name.lower().strip()


def check_fabricated_detected(
    response: str, 
    fabricated_medication: str,
    medication_list: List[str]
) -> Tuple[bool, Dict]:
    """
    Check if the LLM correctly identified the fabricated medication.
    
    Args:
        response: LLM's response text
        fabricated_medication: The actual fabricated medication in the list
        medication_list: Full list of medications shown to LLM
    
    Returns:
        Tuple of (success: bool, details: dict)
    """
    response_lower = response.lower()
    fabricated_lower = normalize_medication_name(fabricated_medication)
    
    # Check if fabricated medication is mentioned in response
    fabricated_mentioned = fabricated_lower in response_lower
    
    # Check for false positives (real meds incorrectly flagged)
    false_positives = []
    for med in medication_list:
        if med != fabricated_medication:
            med_lower = normalize_medication_name(med)
            if med_lower in response_lower:
                false_positives.append(med)
    
    # Determine success
    success = fabricated_mentioned and len(false_positives) == 0
    
    details = {
        "fabricated_detected": fabricated_mentioned,
        "false_positives": false_positives,
        "false_positive_count": len(false_positives)
    }
    
    return success, details


def evaluate_responses(
    test_cases: List[Dict],
    responses: List[str],
    output_file: str = None
) -> Dict:
    """
    Evaluate LLM responses against test cases.
    
    Args:
        test_cases: List of test case dictionaries
        responses: List of LLM response strings (same order as test_cases)
        output_file: Optional path to save evaluation results
    
    Returns:
        Dictionary with evaluation metrics
    """
    if len(test_cases) != len(responses):
        raise ValueError(
            f"Mismatch: {len(test_cases)} test cases but {len(responses)} responses"
        )
    
    results = []
    correct_detections = 0
    total_false_positives = 0
    
    for i, (test_case, response) in enumerate(zip(test_cases, responses)):
        success, details = check_fabricated_detected(
            response,
            test_case["fabricated_medication"],
            test_case["medication_list"]
        )
        
        if success:
            correct_detections += 1
        
        total_false_positives += details["false_positive_count"]
        
        result = {
            "test_case_id": test_case["id"],
            "success": success,
            "fabricated_medication": test_case["fabricated_medication"],
            **details,
            "response": response
        }
        results.append(result)
    
    # Calculate metrics
    total_cases = len(test_cases)
    accuracy = correct_detections / total_cases if total_cases > 0 else 0
    avg_false_positives = total_false_positives / total_cases if total_cases > 0 else 0
    
    evaluation = {
        "total_test_cases": total_cases,
        "correct_detections": correct_detections,
        "accuracy": accuracy,
        "total_false_positives": total_false_positives,
        "avg_false_positives_per_case": avg_false_positives,
        "individual_results": results
    }
    
    # Save to file if specified
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(evaluation, f, indent=2)
        print(f"Evaluation results saved to {output_path}")
    
    return evaluation


def print_summary(evaluation: Dict):
    """Print summary of evaluation results."""
    print("\n" + "="*60)
    print("EVALUATION SUMMARY")
    print("="*60)
    print(f"Total Test Cases: {evaluation['total_test_cases']}")
    print(f"Correct Detections: {evaluation['correct_detections']}")
    print(f"Accuracy: {evaluation['accuracy']:.2%}")
    print(f"Total False Positives: {evaluation['total_false_positives']}")
    print(f"Avg False Positives/Case: {evaluation['avg_false_positives_per_case']:.2f}")
    print("="*60 + "\n")


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Evaluate LLM responses to medication discernment tests"
    )
    parser.add_argument(
        "--test-cases",
        type=str,
        required=True,
        help="Path to test cases JSON file"
    )
    parser.add_argument(
        "--responses",
        type=str,
        required=True,
        help="Path to responses JSON file (list of response strings)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results/evaluation.json",
        help="Output file path (default: results/evaluation.json)"
    )
    
    args = parser.parse_args()
    
    # Load data
    print(f"Loading test cases from {args.test_cases}...")
    test_cases = load_test_cases(args.test_cases)
    
    print(f"Loading responses from {args.responses}...")
    with open(args.responses, 'r') as f:
        responses_data = json.load(f)
    
    # Handle different response file formats
    if isinstance(responses_data, list):
        responses = responses_data
    elif isinstance(responses_data, dict) and "responses" in responses_data:
        responses = responses_data["responses"]
    else:
        raise ValueError("Unexpected response file format")
    
    # Evaluate
    print("Evaluating responses...")
    evaluation = evaluate_responses(test_cases, responses, args.output)
    
    # Print summary
    print_summary(evaluation)


if __name__ == "__main__":
    main()
