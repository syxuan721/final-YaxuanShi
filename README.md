# Product Listing Compliance Checker for Small E-commerce Sellers

## Project overview
This project is a small workflow tool for small e-commerce sellers or junior e-commerce operators. It focuses on one narrow task: reviewing a single product listing draft before publication, identifying weak or missing information, and rewriting the title and bullet points into a clearer version for human review.

The goal is not to build a broad copywriting assistant. The goal is to support one specific workflow that sellers often do manually.

## 1. Context, user, and problem
The target user is a small e-commerce seller or a junior e-commerce operator who prepares listings for one online marketplace.

In small teams, listing work is often manual and repetitive. Sellers may already know the product well, but turning product facts into a clear, complete, and platform-ready title and bullet points still takes time. It is easy to miss vague wording, repeated phrases, or missing attributes.

This project improves one specific workflow: checking and revising a draft listing before it is published.

## 2. Solution and design
I built a small Streamlit app. The user enters:
- product category
- product attributes
- draft title
- draft bullet points
- one selected platform rule set

The app then returns:
- a compliance summary
- weak or missing information
- a revised title
- revised bullet points
- a short human review note

### The system works in two stages.

### Stage 1: Rule and completeness check
This stage handles deterministic parts of the workflow, such as missing attributes, repeated wording, vague language, and simple formatting issues.

### Stage 2: Model-based rewrite
This stage produces a first-pass revised version of the title and bullet points for human review.

This project uses two course concepts:
- **Structured output**: the app always returns the same output sections
- **Context engineering**: the prompt includes platform rules, product attributes, and instructions not to invent unsupported claims

The baseline is the current manual process: checklist-based review and manual rewriting.

## 3. Evaluation and results
The project is evaluated on a small set of sample listings across three simple product categories:
- water bottles
- face moisturizers
- throw pillow covers

The current test set includes 12 sample cases. Each case contains structured product attributes, a draft title, draft bullet points, and expected main issues.

The app is compared against the manual baseline on four dimensions:
- rule compliance accuracy
- rewrite quality
- information preservation
- time saved

At the current stage, the strongest part of the system is the rule-based check. It is already useful for identifying generic wording, repeated wording, missing required attributes, and weak bullet points. The suggested rewrite is still a lightweight prototype. It improves structure and attribute coverage, but it does not yet produce fully natural marketplace-ready copy. Because of that, the tool is more reliable as a review aid than as a final publishing system.

### What worked
The strongest part of the current system is issue detection. The rule-based check is already useful for identifying generic wording, repeated wording, missing required attributes, and weak bullet points. The app also helps structure the workflow by giving the user a first-pass revised version for review.

### Current limits
The rewrite output is still a lightweight prototype, so it does not always produce natural marketplace-ready copy. Output quality drops when the product attributes are incomplete, and the platform rules used in this project are simplified rather than full real-world marketplace policies.

## 4. Artifact snapshot
The repository includes:
- the Streamlit app
- platform rules and sample inputs
- evaluation files
- screenshots of the app interface and outputs

At this stage, the app supports the core workflow from input to output:
1. the user loads or enters a draft listing
2. the app checks rule and completeness issues
3. the app returns structured review results
4. the app provides a first-pass revised title and revised bullet points

Example screenshots are included in the `screenshots/` folder:
- `app_input.png`: input form and sample loading
- `app_output.png`: rule-check results and suggested revisions

## 5. Setup and usage

Install dependencies:

```bash
pip install -r requirements.txt
```
Run the app:

```bash
python -m streamlit run app.py
```

How to use:
- Open the app in the browser
- Enter a product category
- Enter product attributes
- Paste a draft title and bullet points
- Select a platform rule set
- Submit and review the output

### Example
For a quick demo, load the sample case “Sample 1: water bottle” in the app. Then click Run rule-based check. The app will return a compliance summary, missing information, weak points, and a suggested revised title and bullet points.

## 6. Human review boundary

This system is a listing preparation aid, not an automatic publishing tool. The final output should always be reviewed by a human before publication.

The system should not be fully trusted when the input is incomplete or when the rule set is unclear. To reduce that risk, the app is designed to rely on user-provided product facts and to flag missing information instead of guessing.
