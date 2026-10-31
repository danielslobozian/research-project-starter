# Ranking by arm

Scores share one scale across arms: log strength, centred on the mean item; 95% interval from a topic bootstrap. 4075 verdicts on 5 topics (S13, S23, T3, T9, T20). Price per report in USD; B and C include the RB.

## Arm A: the casual question

| # | Model | Effort | Score [95% CI] | Price / report | Median min |
|---|---|---|---|---|---|
| 1 | Claude Opus 5.5 | medium | +1.96 [+1.47, +2.85] | $0.79 | 2.6 |
| 2 | GPT-6.1 Sol | low | +0.80 [+0.23, +1.14] | $0.14 | 1.6 |
| 3 | GPT-6 Astra | medium | +0.41 [-0.39, +1.03] | $0.94 | 4.2 |
| 4 | Mistral Large 4 | thinking high | -0.70 [-1.71, +0.12] | $0.14 | 2.6 |
| 5 | Claude Haiku 5.5 | medium | -1.21 [-1.62, -1.09] | $0.21 | 1.3 |
| 6 | GPT-6 Luna | medium | -1.48 [-1.87, -1.29] | $0.007 | 0.6 |
| 7 | GLM-5.3 Flash | thinking high | -1.53 [-2.15, -1.22] | $0.028 | 1.3 |
| 8 | Claude Sonnet 5.5 | medium | -1.79 [-2.49, -1.44] | $0.21 | 0.9 |
| 9 | Mistral Medium 3.5 | Vibe default | -4.11 [-4.53, -3.97] | $0.23 | 1.6 |
| 10 | Qwen3.5 9B (local) | thinking on | -4.60 [-5.58, -4.22] | $0.017 | 1.6 |
| 11 | Qwen3.5 4B (local) | thinking on | -5.27 [-6.38, -4.81] | $0.023 | 1.2 |
| 12 | Gemma 4 12B (local) | default | -5.70 [-7.21, -4.93] | $0.012 | 0.8 |

Not run in arm A: Claude Haiku 5.5 (xhigh), GPT-6.1 Sol (high), GPT-6 Luna (xhigh).

## Arm B: the research brief (RB), then research from it

| # | Model | Effort | Score [95% CI] | Price / report | Median min |
|---|---|---|---|---|---|
| 1 | Claude Opus 5.5 | medium | +6.09 [+5.49, +7.34] | $4.18 | 13.6 |
| 2 | GPT-6.1 Sol | high | +5.94 [+5.70, +6.69] | $1.44 | 13.1 |
| 3 | GPT-6.1 Sol | low | +3.75 [+3.51, +4.32] | $0.78 | 5.1 |
| 4 | Claude Haiku 5.5 | xhigh | +3.58 [+2.99, +4.68] | $2.13 | 17.3 |
| 5 | GPT-6 Astra | medium | +3.48 [+3.09, +4.01] | $4.84 | 12.5 |
| 6 | GPT-6 Luna | xhigh | +2.52 [+2.22, +3.12] | $0.094 | 5.9 |
| 7 | Mistral Large 4 | thinking high | +2.47 [+2.17, +2.93] | $0.85 | 14.8 |
| 8 | Claude Sonnet 5.5 | medium | +1.83 [+1.21, +2.81] | $1.24 | 3.6 |
| 9 | GLM-5.3 Flash | thinking high | +1.47 [+1.34, +1.88] | $0.16 | 4.5 |
| 10 | Claude Haiku 5.5 | medium | +0.95 [+0.50, +1.63] | $0.64 | 4.8 |
| 11 | GPT-6 Luna | medium | +0.45 [+0.25, +0.72] | $0.034 | 1.9 |
| 12 | Mistral Medium 3.5 | Vibe default | -3.37 [-3.90, -3.07] | $0.71 | 5.0 |
| 13 | Qwen3.5 9B (local) | thinking on | -3.41 [-4.38, -2.66] | $0.050 | 4.9 |
| 14 | Qwen3.5 4B (local) | thinking on | -4.31 [-5.25, -4.02] | $0.12 | 7.0 |
| 15 | Gemma 4 12B (local) | default | -5.35 [-6.72, -4.41] | $0.038 | 3.9 |

## Arm C: the full engine with the RB

| # | Model | Effort | Score [95% CI] | Price / report | Median min |
|---|---|---|---|---|---|
| 1 | Claude Opus 5.5 | medium | +5.79 [+5.17, +7.14] | $7.29 | 19.0 |
| 2 | Claude Sonnet 5.5 | medium | +4.14 [+3.42, +5.59] | $3.11 | 12.2 |
| 3 | GPT-6.1 Sol | high | +3.15 [+2.75, +3.77] | $1.92 | 20.2 |
| 4 | Mistral Large 4 | thinking high | +2.36 [+1.94, +3.23] | $1.18 | 17.1 |
| 5 | GPT-6 Astra | medium | +1.62 [+1.35, +2.16] | $7.80 | 16.3 |
| 6 | GPT-6.1 Sol | low | +1.47 [+1.36, +1.82] | $1.33 | 8.7 |
| 7 | GPT-6 Luna | medium | +1.34 [+0.89, +1.86] | $0.11 | 6.4 |
| 8 | GLM-5.3 Flash | thinking high | +1.18 [+0.13, +2.54] | $0.30 | 8.4 |
| 9 | Claude Haiku 5.5 | medium | +1.00 [-0.29, +2.32] | $1.15 | 11.4 |
| 10 | Mistral Medium 3.5 | Vibe default | -1.67 [-2.05, -1.57] | $1.31 | 7.7 |
| 11 | Qwen3.5 9B (local) | thinking on | -3.47 [-5.07, -2.57] | $0.045 | 6.4 |
| 12 | Qwen3.5 4B (local) | thinking on | -4.38 [-5.43, -3.85] | $0.086 | 7.6 |
| 13 | Gemma 4 12B (local) | default | -5.43 [-6.64, -4.56] | $0.047 | 6.5 |

Not run in arm C: Claude Haiku 5.5 (xhigh), GPT-6 Luna (xhigh).
