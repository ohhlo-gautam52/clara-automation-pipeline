import json
import os
import re
from copy import deepcopy

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(BASE_DIR, "scripts", "account_template.json")
DEMO_FOLDER = os.path.join(BASE_DIR, "dataset", "demo")
OUTPUT_BASE = os.path.join(BASE_DIR, "outputs", "accounts")


def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_account_data(transcript_text, account_id):
    data = load_template()
    data["account_id"] = account_id

    # ----------------------------
    # Company Name Detection
    # ----------------------------
    company_match = re.search(r"(Company name is|We are)\s(.+)", transcript_text, re.IGNORECASE)
    if company_match:
        data["company_name"] = company_match.group(2).strip()
    else:
        data["questions_or_unknowns"].append("Company name not mentioned")

    # ----------------------------
    # Business Hours Detection
    # ----------------------------
    if re.search(r"Monday to Friday", transcript_text, re.IGNORECASE):
        data["business_hours"]["days"] = ["Mon", "Tue", "Wed", "Thu", "Fri"]

    if re.search(r"9\s*to\s*5", transcript_text):
        data["business_hours"]["start"] = "09:00"
        data["business_hours"]["end"] = "17:00"

    if not data["business_hours"]["days"]:
        data["questions_or_unknowns"].append("Business days not specified")

    if not data["business_hours"]["start"]:
        data["questions_or_unknowns"].append("Business hours not specified")

    # ----------------------------
    # Emergency Definition Detection
    # ----------------------------
    emergency_keywords = [
        "sprinkler leak",
        "fire alarm triggered",
        "fire alarm going off",
        "active fire",
        "water leak"
    ]

    for keyword in emergency_keywords:
        if keyword.lower() in transcript_text.lower():
            data["emergency_definition"].append(keyword)

    if not data["emergency_definition"]:
        data["questions_or_unknowns"].append("Emergency definition not clearly specified")

    # ----------------------------
    # Notes
    # ----------------------------
    data["notes"] = "Generated from demo transcript (v1)."

    return data


def save_v1_output(account_data):
    account_id = account_data["account_id"]
    output_path = os.path.join(OUTPUT_BASE, account_id, "v1")

    os.makedirs(output_path, exist_ok=True)

    memo_path = os.path.join(output_path, "memo.json")

    with open(memo_path, "w", encoding="utf-8") as f:
        json.dump(account_data, f, indent=2)

    print(f"✅ Saved v1 memo for {account_id}")


def main():
    if not os.path.exists(DEMO_FOLDER):
        print("❌ dataset/demo folder not found.")
        return

    files = [f for f in os.listdir(DEMO_FOLDER) if f.endswith(".txt")]

    if not files:
        print("⚠ No .txt files found inside dataset/demo/")
        return

    for filename in files:
        file_path = os.path.join(DEMO_FOLDER, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            transcript_text = f.read()

        account_id = filename.replace(".txt", "")

        extracted_data = extract_account_data(transcript_text, account_id)
        save_v1_output(extracted_data)

    print("\n🎉 All demo transcripts processed successfully.")


if __name__ == "__main__":
    main()