# Phase B7A.1 - Recruiter Score Calibration Report

## Objectives
The goal of this calibration pass was to analyze the default recruiter score distributions, evaluate the confidence bands, and adjust configuration thresholds in `ranking_config.yaml` to ensure realistic separation between candidates without altering the underlying intelligence heuristics.

## Pre-Calibration Findings
Initially, the base recruiter score maxed out at `0.43` across 750 candidates (representing the top 250 retrievals across 3 separate tech roles). Because the hardcoded confidence bands expected an absolute score of `> 0.85` for "Exceptional" and `> 0.70` for "High", **100% of candidates fell into the "Low" confidence band**.

This harsh scoring is mathematically expected because the sub-engines (like `experience_fit` or `leadership`) impose strict zeroing heuristics for missing data, and penalize junior candidates effectively. The Arithmetic Mean strictly normalizes this, keeping the ceiling low.

## Calibration Adjustments
To fix the confidence band clustering without artificial score inflation, we extracted the thresholds into `ranking_config.yaml` and `settings.py` and calibrated them to the empirical distribution:

```yaml
confidence_thresholds:
  exceptional: 0.35  # Was 0.85
  high: 0.28         # Was 0.70
  medium: 0.20       # Was 0.50
```

## Post-Calibration Distribution Statistics

* **Sample Size**: 750 (Top 250 hybrid retrieved candidates x 3 JDs)
* **Mean Score**: 0.240
* **Median Score**: 0.236
* **Min Score**: 0.081
* **Max Score**: 0.430
* **Standard Deviation**: 0.050

### Score Histogram

| Range | Count |
| :--- | :--- |
| **0.0 - 0.1** | 1 |
| **0.1 - 0.2** | 197 |
| **0.2 - 0.3** | 466 |
| **0.3 - 0.4** | 83 |
| **0.4 - 0.5** | 3 |

### Confidence Band Distribution
With the newly calibrated thresholds, the distribution of the pre-filtered hybrid top 250 candidates looks much healthier:

* **Exceptional (≥ 0.35)**: 21 candidates (2.8%)
* **High (≥ 0.28)**: 141 candidates (18.8%)
* **Medium (≥ 0.20)**: 417 candidates (55.6%)
* **Low (< 0.20)**: 171 candidates (22.8%)

## Conclusion
The adjusted thresholds create a highly realistic pyramid distribution. Only the absolute top ~3% of the pre-screened pipeline earn an "Exceptional" recruiter confidence rating, while the majority safely land in the "Medium" (passable) band. 

No further adjustments to the heuristic logic are required. The JSON artifacts have been saved to `artifacts/recruiter_score_distribution.json` and `artifacts/confidence_distribution.json`.
