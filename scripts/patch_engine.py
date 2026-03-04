import json
import os
import copy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_BASE = os.path.join(BASE_DIR, "outputs", "accounts")
ONBOARDING_FOLDER = os.path.join(BASE_DIR, "dataset", "onboarding")
CHANGELOG_FOLDER = os.path.join(BASE_DIR, "changelog")

os.makedirs(CHANGELOG_FOLDER, exist_ok=True)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def extract_onboarding_updates(text):
    updates = {}

    if "8 to 6" in text:
        updates["business_hours"] = {
            "days": ["Mon", "Tue", "Wed", "Thu", "Fri"],
            "start": "08:00",
            "end": "18:00",
            "timezone": "CST"
        }

    if "never create sprinkler jobs" in text.lower():
        updates["integration_constraints"] = [
            "Never create sprinkler jobs in ServiceTrade"
        ]

    return updates


def generate_detailed_diff(old_data, new_data):
    changes = []

    for key in new_data:
        old_value = old_data.get(key)
        new_value = new_data.get(key)

        if old_value != new_value:
            changes.append({
                "field": key,
                "old": old_value,
                "new": new_value
            })

    return changes


def process_onboarding_file(filename):
    account_id = filename.replace(".txt", "")
    onboarding_path = os.path.join(ONBOARDING_FOLDER, filename)

    v1_path = os.path.join(OUTPUT_BASE, account_id, "v1", "memo.json")

    if not os.path.exists(v1_path):
        print(f"❌ No v1 found for {account_id}")
        return

    v1_data = load_json(v1_path)

    with open(onboarding_path, "r", encoding="utf-8") as f:
        text = f.read()

    updates = extract_onboarding_updates(text)

    if not updates:
        print(f"⚠ No changes detected for {account_id}")
        return

    v2_data = copy.deepcopy(v1_data)
    v2_data.update(updates)

    detailed_changes = generate_detailed_diff(v1_data, v2_data)

    # Save v2 memo
    v2_folder = os.path.join(OUTPUT_BASE, account_id, "v2")
    os.makedirs(v2_folder, exist_ok=True)
    save_json(os.path.join(v2_folder, "memo.json"), v2_data)

    # Save detailed changelog
    changelog_path = os.path.join(CHANGELOG_FOLDER, f"{account_id}_changes.md")

    with open(changelog_path, "w", encoding="utf-8") as f:
        f.write("## Version v2 Changes\n\n")

        if not detailed_changes:
            f.write("No changes detected.\n")
        else:
            for change in detailed_changes:
                f.write(f"### {change['field']}\n")
                f.write(f"- Old: `{json.dumps(change['old'], indent=2)}`\n")
                f.write(f"- New: `{json.dumps(change['new'], indent=2)}`\n")
                f.write(f"- Reason: Confirmed during onboarding call\n\n")

    print(f"✅ v2 generated with detailed changelog for {account_id}")


def main():
    files = [f for f in os.listdir(ONBOARDING_FOLDER) if f.endswith(".txt")]

    if not files:
        print("⚠ No onboarding files found.")
        return

    for file in files:
        process_onboarding_file(file)

    print("\n🎉 All onboarding files processed.")


if __name__ == "__main__":
    main()