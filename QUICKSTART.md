# Quick Start Guide

## For Researchers

### Quick Test (5 minutes)

1. **Preview a test case:**
   ```bash
   python scripts/generate_prompts.py --preview
   ```

2. **Generate 10 test cases:**
   ```bash
   python scripts/generate_prompts.py --num-cases 10 --output results/my_test.json
   ```

3. **Query your LLM** with the prompts from `results/my_test.json`

4. **Save responses** as a JSON array in `results/my_responses.json`

5. **Evaluate results:**
   ```bash
   python scripts/evaluate_responses.py \
     --test-cases results/my_test.json \
     --responses results/my_responses.json
   ```

### Full Study (1-2 hours)

1. **Generate 100+ test cases:**
   ```bash
   python scripts/generate_prompts.py --num-cases 100
   ```

2. **Run systematic LLM testing** with multiple models

3. **Evaluate and compare results** across models

4. **Analyze for patterns:**
   - Detection accuracy
   - False positive rates
   - Position bias
   - Response consistency

## Common Variations

### Different List Sizes

Test with smaller lists (easier):
```bash
python scripts/generate_prompts.py --num-cases 50 --list-size 5
```

Test with larger lists (harder):
```bash
python scripts/generate_prompts.py --num-cases 50 --list-size 20
```

### Custom Data Sources

1. Create your own `data/custom_fabrications.txt`
2. Modify `generate_prompts.py` to load from your file:
   ```python
   pokemon = load_data_file("custom_fabrications.txt")
   ```

## Troubleshooting

### Issue: Scripts not found
**Solution:** Make sure you're in the repository root directory:
```bash
cd Pokemon-Drugs-Names
```

### Issue: Import errors
**Solution:** Use Python 3.6+:
```bash
python3 scripts/generate_prompts.py --preview
```

### Issue: File not found errors
**Solution:** Ensure data files exist:
```bash
ls data/medications.txt data/pokemon.txt
```

### Issue: Evaluation shows 0% accuracy
**Solution:** Check that:
1. Response order matches test case order
2. Responses mention the fabricated medication name
3. Response format is correct (JSON array of strings)

## Tips for Better Results

### Prompt Engineering

Try different prompt variations:
- More specific instructions
- Medical context setting
- Request for explanations
- Multiple-choice format

### Data Quality

- Use medications from same therapeutic class (harder)
- Mix common and rare medications
- Include look-alike/sound-alike real drugs

### Evaluation Extensions

Add custom metrics:
- Confidence scoring
- Explanation quality
- Time to response
- Context awareness

## Example Response Format

```json
[
  "After reviewing the medications, I found that 'Pikachu' is not a legitimate medication...",
  "The fabricated medication is 'Charizard'...",
  "All medications appear legitimate except for 'Mewtwo'..."
]
```

## Further Reading

See full documentation in `README.md` for:
- Detailed methodology
- Research applications
- Contributing guidelines
- Citation information
