# Evaluation Notes

## Evaluation goal
The goal of the evaluation is to compare the app against the manual baseline on a small set of realistic product listing examples.

## Baseline
The baseline is the current manual process:
1. read the draft listing
2. compare it against a simple checklist
3. rewrite it by hand

## Test set
The test set includes 12 sample listings across three categories:
- water bottles
- face moisturizers
- throw pillow covers

Each case includes:
- structured product attributes
- a draft title
- draft bullet points
- expected main issues

## Evaluation dimensions
I will compare the app and the manual baseline on four dimensions:

### 1. Rule compliance accuracy
Did the app correctly identify the main rule or completeness issues in the draft?

### 2. Rewrite quality
Did the suggested revised version make the listing clearer and more specific?

### 3. Information preservation
Did the suggested rewrite stay grounded in the provided product attributes without inventing unsupported claims?

### 4. Time saved
Did the app reduce the time needed to review and improve the listing compared with manual review?

## Early observations
From the first sample cases, the rule-based checker is already useful for:
- identifying generic wording
- identifying repeated wording
- identifying missing required attributes
- flagging weak bullet points

The mock rewrite output is helpful as a first-pass revision, but it is still limited. It improves structure and attribute coverage, but it does not yet produce natural marketplace-ready copy. That is an important current limitation.

## Main failure patterns to watch
- incomplete input attributes may lead to weak rewrite suggestions
- some rewrites may become too generic
- some listings may become more compliant but less natural
- ambiguous platform rules may lead to inconsistent judgment

## What this means
At this stage, the app already supports the workflow better than a blank manual start, especially for issue detection. However, the revision quality is still only a prototype, so the tool should be treated as a review aid rather than a final publishing system.
