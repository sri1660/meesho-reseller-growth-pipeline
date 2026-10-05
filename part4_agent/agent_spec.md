# Meesho Reseller Growth Monitoring — Agent Specification

## Objective

Build an offline agent workflow that monitors category revenue, validates incoming data, calculates Month-on-Month (MoM) growth, identifies flagged categories, and produces a reliable stakeholder-ready output.

## Agent Workflow

1. Load the monthly category revenue feed.
2. Validate the feed before performing calculations.
3. Calculate MoM growth for each category.
4. Classify each category using the Part 2 growth threshold.
5. Select flagged categories for monitoring.
6. Rank flagged categories by absolute MoM movement.
7. Select the top 3 flagged categories.
8. Produce a deterministic JSON result.
9. Report validation errors instead of processing corrupted input.

## Decision Rules

### Feed Validation

The agent must reject a feed when:

* category is missing
* revenue is missing
* revenue is not numeric
* revenue is negative

### MoM Classification

The Part 2 growth engine is used.

* Absolute MoM change greater than 8% → `flagged`
* Absolute MoM change less than 8% → `not_flagged`
* Absolute MoM change exactly 8% → `escalate_exact_boundary`

## Flagged Category Selection

Only categories classified as `flagged` are eligible for selection.

The agent ranks flagged categories by absolute MoM percentage in descending order.

The top 3 flagged categories are selected.

## Reliability Rules

The agent must:

* use only verified input values
* never invent revenue values
* never modify calculated percentages
* clearly report validation errors
* preserve the exact Part 2 classification rules
* produce deterministic output for the same input

## Output

The agent output contains:

* validation status
* input file
* previous month
* current month
* flagged categories
* previous revenue
* current revenue
* MoM percentage
* classification
* validation errors when the input is invalid
