# Demo Instructions

## Recommended demo flow

1. Open `README.md` and explain the project goal.
2. Show `docs/problem_statement.md` to demonstrate verified problem framing.
3. Show `outputs/reports/data_dictionary_inference.md` to explain schema verification.
4. Run the analysis command:

```bash
python -m src.main
```

5. Open generated outputs:
   - `outputs/tables/baseline_results.csv`
   - `outputs/tables/best_model_summary.csv`
   - `outputs/figures/`
6. Walk through the PPT draft in `ppt/slide_content.md`.

## Suggested talking points

- The project was built with a dataset-first workflow.
- The target mapping was verified from workbook columns before modeling.
- The baseline is intentionally pragmatic and interview-ready.
- The pipeline is modular, testable, and reproducible.
