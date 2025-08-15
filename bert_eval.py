# bert_eval.py
import json
import torch
from bert_score import score
from rag.langchain_pipeline import answer_query

TEST_FILE = "data/test_hundred_queries.json"

def main():
    with open(TEST_FILE, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    candidate_answers = []
    reference_answers = []

    for i, item in enumerate(test_data, 1):
        query = item["query"]
        reference = item["reference"]

        # Get bot's answer
        bot_answer = answer_query(query)

        candidate_answers.append(bot_answer)
        reference_answers.append(reference)

        print(f"[{i}] Query: {query}")
        print(f"Bot Answer: {bot_answer[:80]}...")
        print(f"Reference: {reference[:80]}...")
        print("-" * 60)

    # Compute BERTScore
    P, R, F1 = score(candidate_answers, reference_answers, lang="en", verbose=True)

    print(f"\n📊 Average Precision: {P.mean().item():.4f}")
    print(f"📊 Average Recall:    {R.mean().item():.4f}")
    print(f"📊 Average F1 Score:  {F1.mean().item():.4f}")

if __name__ == "__main__":
    # GPU হলে এটা use হবে
    if torch.cuda.is_available():
        print("⚡ Using GPU for BERTScore")
    else:
        print("🐢 Using CPU for BERTScore")
    main()
