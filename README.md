# Meesho Reseller Growth Pipeline

## Project Overview

This project implements an offline reseller growth monitoring pipeline for Meesho-style reseller data.

The pipeline combines SQL analysis, a deterministic growth engine, a reliable narrative/prompt layer, and an offline agent workflow.

The project focuses on:

* Revenue analysis
* Reseller performance monitoring
* Month-on-Month (MoM) growth detection
* Data validation
* Flagged-category identification
* Stakeholder narrative generation
* Privacy-safe reseller references
* Automated agent testing

---

# Project Structure

```text
meesho-reseller-growth-pipeline
│
├── data
│   ├── generate_dataset.py
│   ├── meesho_reseller.db
│   ├── orders.csv
│   └── resellers.csv
│
├── part1_sql
│   ├── fixtures
│   ├── queries.sql
│   ├── run_queries.py
│   └── output
│       ├── inactive_resellers.csv
│       ├── june_aov.csv
│       ├── left_join_count_demo.csv
│       ├── monthly_category_revenue.csv
│       ├── region_revenue.csv
│       └── top_resellers.csv
│
├── part2_engine
│   ├── growth_engine.py
│   ├── test_growth_engine.py
│   └── fixtures
│       ├── corrupted_feed.csv
│       └── monthly_category_revenue.csv
│
├── part3_narrative
│   ├── masking.py
│   ├── narrative_report.md
│   └── prompt_pack.md
│
├── part4_agent
│   ├── agent_spec.md
│   ├── mock_agent_runner.py
│   └── test_agent.py
│
└── README.md
```

---

# Part 1 — SQL Analysis

## Objective

Analyze reseller and order data using SQL and generate reusable CSV outputs.

## Outputs

The SQL pipeline generates:

* Monthly category revenue
* Region revenue
* Top resellers
* Inactive resellers
* LEFT JOIN count demonstration
* June delivered-order AOV

## Run

From the project root:

```powershell
cd E:\meesho-reseller-growth-pipeline\part1_sql
python run_queries.py
```

The generated CSV files are stored in:

```text
part1_sql/output/
```

---

# Part 2 — Reliable Growth Engine

## Objective

Calculate Month-on-Month revenue growth and classify changes using an 8% monitoring threshold.

## Classification Rules

```text
Absolute MoM change > 8%
→ flagged

Absolute MoM change < 8%
→ not_flagged

Absolute MoM change = 8%
→ escalate_exact_boundary
```

## Data Validation

The engine detects:

* Missing category
* Missing revenue
* Non-numeric revenue
* Negative revenue

## Fixtures

Valid monthly data:

```text
part2_engine/fixtures/monthly_category_revenue.csv
```

Corrupted data:

```text
part2_engine/fixtures/corrupted_feed.csv
```

## Test

```powershell
cd E:\meesho-reseller-growth-pipeline\part2_engine
python test_growth_engine.py
```

---

# Part 3 — Reliable AI Narrative and Prompt Pack

## Objective

Convert verified growth signals into stakeholder-ready narratives while preventing unsupported claims and reseller-name leakage.

## Components

### Prompt Pack

```text
part3_narrative/prompt_pack.md
```

Contains:

* Trigger
* Input List
* Prompt
* Checklist

### Narrative Report

```text
part3_narrative/narrative_report.md
```

Contains worked examples for flagged Ethnic Wear movements.

### Privacy Masking

```text
part3_narrative/masking.py
```

The masking layer converts reseller IDs into aliases.

Example:

```text
RS019 → ALIAS-19
RS006 → ALIAS-06
```

It also checks whether raw reseller names appear in externally facing text.

## Test

```powershell
cd E:\meesho-reseller-growth-pipeline\part3_narrative
python masking.py
```

Expected privacy results:

```text
Safe text: True
Unsafe text: False
```

---

# Part 4 — Offline Agent Workflow

## Objective

Build a deterministic offline agent that validates data, calculates growth, identifies flagged categories, and returns a structured JSON result.

## Agent Workflow

```text
Input CSV
   ↓
Validate feed
   ↓
Calculate MoM growth
   ↓
Classify categories
   ↓
Select flagged categories
   ↓
Rank by absolute MoM movement
   ↓
Select top 3
   ↓
Return JSON result
```

## Agent Files

### Specification

```text
part4_agent/agent_spec.md
```

### Agent Runner

```text
part4_agent/mock_agent_runner.py
```

### Automated Tests

```text
part4_agent/test_agent.py
```

---

# Part 4 — Valid Feed Test

Run:

```powershell
cd E:\meesho-reseller-growth-pipeline\part4_agent
python mock_agent_runner.py ..\part2_engine\fixtures\monthly_category_revenue.csv
```

The agent successfully identifies the latest month comparison:

```text
May → June
```

The top flagged categories are selected according to absolute MoM movement.

The verified flagged examples include:

```text
Ethnic Wear        -58.74%
Home & Kitchen      42.59%
Kids Wear            23.90%
```

---

# Part 4 — Corrupted Feed Test

Run:

```powershell
python mock_agent_runner.py ..\part2_engine\fixtures\corrupted_feed.csv
```

The agent returns:

```text
status: validation_failed
```

The corrupted feed contains three validation errors:

1. Negative revenue for Western Wear
2. Missing category
3. Missing revenue for Home & Kitchen

The agent correctly returns an empty flagged-category list rather than processing invalid data.

---

# Automated Agent Test

Run:

```powershell
python test_agent.py
```

Expected result:

```text
All Part 4 agent tests passed successfully.
```

---

# Reliability Principles

The pipeline follows these principles:

* Use only verified input values
* Do not invent revenue values
* Do not modify calculated percentages
* Validate data before processing
* Reject corrupted input
* Clearly distinguish facts from hypotheses
* Apply privacy masking to reseller references
* Produce deterministic output for identical input

---

# Technology Used

* Python
* SQLite
* SQL
* CSV
* Markdown
* JSON

No external AI API or API key is required for the offline workflow.

---

# Testing Summary

| Component                      | Status    |
| ------------------------------ | --------- |
| Part 1 SQL outputs             | Passed    |
| Part 2 growth engine           | Passed    |
| Part 2 validation              | Passed    |
| Part 3 privacy masking         | Passed    |
| Part 3 narrative               | Completed |
| Part 4 valid-feed agent        | Passed    |
| Part 4 corrupted-feed handling | Passed    |
| Part 4 automated tests         | Passed    |

---

# Final Result

The project provides an end-to-end offline reseller growth monitoring pipeline:

```text
Raw Data
   ↓
SQL Analysis
   ↓
Growth Engine
   ↓
Reliable Narrative Layer
   ↓
Privacy Masking
   ↓
Agent Workflow
   ↓
Validated Stakeholder Output
```

The system is designed to prioritize **data validation, deterministic calculations, explainability, privacy, and reliable decision support**.
