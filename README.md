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
- a rewritten title
- rewritten bullet points
- a short human review note

The system works in two stages:

**Stage 1: Rule and completeness check**  
This stage handles more deterministic parts of the workflow, such as missing attributes, repeated wording, vague language, or simple formatting issues.

**Stage 2: Model-based rewrite**  
The model rewrites the title and bullet points into a cleaner version and explains the main changes.

This project uses two course concepts:
- **Structured output**: the app always returns the same output sections
- **Context engineering**: the prompt includes platform rules, product attributes, and instructions not to invent unsupported claims

The baseline is the current manual process: checklist-based review and manual rewriting.

## 3. Evaluation and results
The project is evaluated on a small set of sample listings across a few simple product categories.

I compare the app against the manual baseline on four dimensions:
- rule compliance accuracy
- rewrite quality
- information preservation
- time saved

In general, the app works best when the input attributes are clear and complete. It is useful for spotting generic wording and producing cleaner rewrites. Its main weakness is that it can become too generic when the input information is limited.

## 4. Artifact snapshot
The repository includes:
- the Streamlit app
- prompt files
- platform rules and sample inputs
- evaluation files
- screenshots or sample outputs

The app interface includes a simple input form and a structured results page. The output shows compliance issues, missing information, a rewritten title, rewritten bullet points, and a human review note.

## 5. Setup and usage
Install dependencies:

```bash
pip install -r requirements.txt
```
Run the app:
```bash
streamlit run app.py
```
How to use:
- Open the app in the browser
- Enter a product category
- Enter product attributes
- Paste a draft title and bullet points
- Select a platform rule set
- Submit and review the output

## 6. Human review boundary
This system is a listing preparation aid, not an automatic publishing tool. The final output should always be reviewed by a human before publication.

The system should not be fully trusted when the input is incomplete or when the rule set is unclear. To reduce that risk, the app is designed to rely on user-provided product facts and to flag missing information instead of guessing.
