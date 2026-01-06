# Preference Alignment — Evaluation Pipeline
GPT-4o-mini Judge · Factuality Scoring · Multi-Model Benchmarking

This directory implements the **automated evaluation pipeline** used to benchmark:

- Original-DPO models
- Factual-DPO models (across Δ = 0, 2, 4, 6, 8, 10, 20, 30, 50, 100)

Evaluation is performed using **GPT-4o-mini** as an LLM-as-a-judge.

All evaluation configuration is pulled from:

```
src/project/config/config.yaml
```

---

## 📁 Evaluation Directory Structure

```
src/project/evaluation/
│
├── evaluations/
│   └── run_all_evaluations.py      # Main orchestrator
│
├── utils/
│   ├── eval_core_utils.py          # Generation + GPT judge scoring
│   └── eval_template.py            # Factual judge prompt
```

---

# ⚙️ Configuration Overview (Evaluation)

The configuration includes:

---

## 1️⃣ Evaluation Settings

```yaml
eval:
  data_file: "src/project/data_construction/data/skywork_extracted_test.jsonl"
  batch_size: 16
  max_new_tokens: 2048
  judge_concurrency: 10
```

---

## 2️⃣ Model Paths

```yaml
paths:
  original_root: "src/project/training/data/original/Models"
  modified_root: "src/project/training/data/modified/Models"
```

The evaluation script automatically locates checkpoints:

```
<short>_OriginalDPO/
<short>_delta<value>/
```

---

## 3️⃣ Model Registry & Δ Values

```yaml
models:
  - short: "gemma2-9b"
  - short: "llama3-8b"
  - short: "qwen3-8b"
```

```yaml
deltas: [0, 2, 4, 6, 8, 10, 20, 30, 50, 100]
```

Total evaluations:

```
7 models × 10 deltas = 70 comparisons
```

---

## 🧠 Factual Judge Model

```yaml
model:
  name: "gpt-4o-mini"
  temperature: 0.8
```

---

# 📊 Evaluation Metrics

For each model pair, the pipeline computes:

| Metric | Meaning |
|--------|---------|
| factuality_A | Mean factual score of Original-DPO model |
| factuality_B | Mean factual score of Δ-model |
| halluc_rate_A | % outputs scoring < 5 |
| halluc_rate_B | % outputs scoring < 5 |
| win_rate | How often Δ-model outperforms baseline |
| count | Total prompts evaluated |

Results saved to:

```
eval_results.json
```

---

# 🚀 Running Evaluation

```bash
python -m project.evaluation.evaluations.run_all_evaluations
```

The script:

1. Loads config
2. Loads evaluation prompts
3. Loads Original-DPO and Δ-models
4. Generates responses
5. Sends to GPT-4o-mini asynchronously
6. Computes metrics
7. Saves results

---

# 🧩 Core Components

## `eval_core_utils.py`

Includes:

- **batch_generate()** → Deterministic HF inference
- **judge_factual()** → Scores one answer
- **judge_many()** → Async batch scoring
- **evaluate_pair()** → Full evaluation for one (model, Δ)

---

## `eval_template.py`

Provides the factuality judge prompt using:

```
[[score]]
```

format.

---

# ✅ Summary

This evaluation pipeline provides:

- End-to-end factuality benchmarking
- Async OpenAI judge scoring
- Multi-model × multi-delta evaluation
- Config-driven reproducibility
- Clean JSON output for papers and analysis
