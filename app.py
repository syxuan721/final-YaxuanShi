import json
import re
from collections import Counter
from pathlib import Path

import streamlit as st


# ----------------------------
# File loading
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

RULES_PATH = DATA_DIR / "platform_rules.json"
SAMPLES_PATH = DATA_DIR / "sample_inputs.json"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_rules():
    return load_json(RULES_PATH)


@st.cache_data
def load_samples():
    return load_json(SAMPLES_PATH)


# ----------------------------
# Text helpers
# ----------------------------
def normalize_text(text: str) -> str:
    return text.lower().strip()


def tokenize(text: str):
    return re.findall(r"\b[a-zA-Z]+\b", text.lower())


def find_repeated_words(text: str, min_count: int = 2):
    words = tokenize(text)
    counts = Counter(words)
    repeated = [word for word, count in counts.items() if count >= min_count]
    return repeated


def count_generic_words(text: str, generic_words: list[str]):
    text_lower = text.lower()
    found = []

    for word in generic_words:
        if word.lower() in text_lower:
            found.append(word)

    return found


def bullet_is_generic(bullet: str, generic_words: list[str]) -> bool:
    words = tokenize(bullet)
    if len(words) < 3:
        return True

    found_generic = count_generic_words(bullet, generic_words)
    if len(found_generic) > 0:
        return True

    generic_patterns = [
        "works well",
        "nice for",
        "great for",
        "good for",
        "high quality",
        "nice design",
    ]
    bullet_lower = bullet.lower()
    if any(pattern in bullet_lower for pattern in generic_patterns):
        return True

    return False


def attribute_covered(attr_value: str, combined_text: str) -> bool:
    return attr_value.lower() in combined_text.lower()


# ----------------------------
# Rule checks
# ----------------------------
def run_checks(category: str, attributes: dict, title: str, bullets: list[str], rules: dict):
    results = {
        "compliance_summary": [],
        "violations": [],
        "missing_information": [],
        "weak_points": [],
    }

    title_rules = rules["title_rules"]
    bullet_rules = rules["bullet_rules"]
    generic_words = rules["generic_words"]

    # Title length checks
    title_len = len(title)
    if title_len < title_rules["min_length"]:
        results["violations"].append(
            f"Title is too short ({title_len} characters). Minimum is {title_rules['min_length']}."
        )
    if title_len > title_rules["max_length"]:
        results["violations"].append(
            f"Title is too long ({title_len} characters). Maximum is {title_rules['max_length']}."
        )

    # Repeated words
    if title_rules.get("avoid_repeated_words", False):
        repeated = find_repeated_words(title)
        if repeated:
            results["weak_points"].append(
                f"Title contains repeated words: {', '.join(repeated)}."
            )

    # Generic words in title
    if title_rules.get("avoid_excessive_generic_words", False):
        found_generic = count_generic_words(title, generic_words)
        if found_generic:
            results["weak_points"].append(
                f"Title uses generic wording: {', '.join(found_generic)}."
            )

    # Bullet count checks
    non_empty_bullets = [b.strip() for b in bullets if b.strip()]
    bullet_count = len(non_empty_bullets)

    if bullet_count < bullet_rules["min_bullets"]:
        results["violations"].append(
            f"Too few bullet points ({bullet_count}). Minimum is {bullet_rules['min_bullets']}."
        )
    if bullet_count > bullet_rules["max_bullets"]:
        results["violations"].append(
            f"Too many bullet points ({bullet_count}). Maximum is {bullet_rules['max_bullets']}."
        )

    # Bullet-level checks
    for i, bullet in enumerate(bullets, start=1):
        bullet_clean = bullet.strip()

        if bullet_rules.get("avoid_empty_bullets", False) and not bullet_clean:
            results["violations"].append(f"Bullet {i} is empty.")
            continue

        word_count = len(tokenize(bullet_clean))
        if word_count < bullet_rules["min_words_per_bullet"]:
            results["weak_points"].append(
                f"Bullet {i} is too short ({word_count} words)."
            )

        if bullet_rules.get("avoid_generic_bullets", False) and bullet_is_generic(
            bullet_clean, generic_words
        ):
            results["weak_points"].append(f"Bullet {i} is too generic.")

    # Required attribute coverage
    required_map = title_rules.get("required_attributes_by_category", {})
    required_attrs = required_map.get(category.lower(), [])

    combined_text = title + " " + " ".join(non_empty_bullets)

    for attr_name in required_attrs:
        attr_value = attributes.get(attr_name, "")
        if not attr_value:
            results["missing_information"].append(
                f"Missing required attribute value for '{attr_name}'."
            )
        elif not attribute_covered(str(attr_value), combined_text):
            results["missing_information"].append(
                f"Listing does not clearly mention required attribute '{attr_name}: {attr_value}'."
            )

    # Summary
    if not results["violations"] and not results["weak_points"] and not results["missing_information"]:
        results["compliance_summary"].append("No obvious issues found in the rule-based check.")
    else:
        results["compliance_summary"].append("The listing has issues that should be reviewed before publication.")

    return results


# ----------------------------
# UI helpers
# ----------------------------
def sample_label(sample: dict) -> str:
    return f"Sample {sample['id']}: {sample['category']}"


def format_attributes_text(attributes: dict) -> str:
    lines = []
    for key, value in attributes.items():
        lines.append(f"{key}: {value}")
    return "\n".join(lines)


def parse_attributes_text(text: str) -> dict:
    attributes = {}
    for line in text.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            attributes[key.strip().lower()] = value.strip()
    return attributes


# ----------------------------
# Streamlit app
# ----------------------------
st.set_page_config(page_title="Product Listing Compliance Checker", layout="wide")

st.title("Product Listing Compliance Checker")
st.write(
    "This app checks one draft product listing for basic rule and completeness issues before publication."
)

rules = load_rules()
samples = load_samples()

st.subheader("Load a sample input")
sample_options = {sample_label(sample): sample for sample in samples}
selected_label = st.selectbox("Choose a sample", options=list(sample_options.keys()))
selected_sample = sample_options[selected_label]

if st.button("Load selected sample"):
    st.session_state["category"] = selected_sample["category"]
    st.session_state["attributes_text"] = format_attributes_text(selected_sample["attributes"])
    st.session_state["draft_title"] = selected_sample["draft_title"]
    st.session_state["draft_bullets"] = "\n".join(selected_sample["draft_bullets"])

# Default state
if "category" not in st.session_state:
    st.session_state["category"] = selected_sample["category"]
if "attributes_text" not in st.session_state:
    st.session_state["attributes_text"] = format_attributes_text(selected_sample["attributes"])
if "draft_title" not in st.session_state:
    st.session_state["draft_title"] = selected_sample["draft_title"]
if "draft_bullets" not in st.session_state:
    st.session_state["draft_bullets"] = "\n".join(selected_sample["draft_bullets"])

st.subheader("Listing input")

col1, col2 = st.columns(2)

with col1:
    category = st.text_input("Product category", key="category")
    attributes_text = st.text_area(
        "Product attributes (one per line, format: key: value)",
        height=180,
        key="attributes_text",
    )

with col2:
    draft_title = st.text_area("Draft title", height=100, key="draft_title")
    draft_bullets_text = st.text_area(
        "Draft bullet points (one bullet per line)",
        height=180,
        key="draft_bullets",
    )

st.subheader("Platform rule set")
st.json(rules)

if st.button("Run rule-based check"):
    attributes = parse_attributes_text(attributes_text)
    bullets = draft_bullets_text.splitlines()

    results = run_checks(
        category=category,
        attributes=attributes,
        title=draft_title,
        bullets=bullets,
        rules=rules,
    )

    st.subheader("Results")

    st.markdown("### Compliance summary")
    for item in results["compliance_summary"]:
        st.write(f"- {item}")

    st.markdown("### Violations")
    if results["violations"]:
        for item in results["violations"]:
            st.write(f"- {item}")
    else:
        st.write("- None")

    st.markdown("### Missing information")
    if results["missing_information"]:
        for item in results["missing_information"]:
            st.write(f"- {item}")
    else:
        st.write("- None")

    st.markdown("### Weak points")
    if results["weak_points"]:
        for item in results["weak_points"]:
            st.write(f"- {item}")
    else:
        st.write("- None")

    st.markdown("### Human review note")
    st.info(rules["human_review_note"])
