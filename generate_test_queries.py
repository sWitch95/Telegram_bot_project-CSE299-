# generate_test_queries.py
import json
import random

# Path to your modified dataset
DATA_FILE = "data/modified_drug_dataset.json"
OUTPUT_FILE = "data/test_hundred_queries.json"

# Number of total queries
TOTAL_QUERIES = 100
ENGLISH_RATIO = 0.5  # 50% English, 50% Bangla

# English & Bangla query patterns
ENGLISH_PATTERNS = [
    "What is {name}?",
    "Tell me about {name}",
    "What are the uses of {name}?",
    "Explain {name}",
    "Give me information about {name}"
]

BANGLA_PATTERNS = [
    "{name} কী?",
    "{name} সম্পর্কে বলুন",
    "{name} এর ব্যবহার কী?",
    "{name} ব্যাখ্যা করুন",
    "{name} এর তথ্য দিন"
]

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Only take generic names
    generic_entries = [entry for entry in data if entry.get("Type", "").lower() == "generic"]

    # Build query set
    queries = []
    for entry in generic_entries:
        name = entry.get("Name", "").strip()
        reference = entry.get("Indication Description", "") or entry.get("Description", "")

        if not name or not reference:
            continue

        # English queries
        for pattern in ENGLISH_PATTERNS:
            queries.append({
                "query": pattern.format(name=name),
                "reference": reference
            })

        # Bangla queries
        for pattern in BANGLA_PATTERNS:
            queries.append({
                "query": pattern.format(name=name),
                "reference": reference
            })

    # Shuffle and trim to required size
    random.shuffle(queries)
    queries = queries[:TOTAL_QUERIES]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(queries, f, ensure_ascii=False, indent=2)

    print(f"✅ Generated {len(queries)} test queries at {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
