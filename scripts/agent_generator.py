import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_BASE = os.path.join(BASE_DIR, "outputs", "accounts")


def build_system_prompt(account_data):
    company = account_data.get("company_name", "the company")
    hours = account_data.get("business_hours", {})
    timezone = hours.get("timezone", "local timezone")

    prompt = f"""
You are Clara, the AI voice assistant for {company}.

BUSINESS HOURS:
Days: {hours.get("days")}
Start: {hours.get("start")}
End: {hours.get("end")}
Timezone: {timezone}

========================
OFFICE HOURS FLOW
========================
1. Greet the caller warmly.
2. Ask the purpose of the call.
3. Collect caller name and phone number.
4. Route or transfer the call according to business rules.
5. If transfer fails:
   - Apologize
   - Inform dispatch will follow up.
6. Ask if they need anything else.
7. Close politely.

========================
AFTER HOURS FLOW
========================
1. Greet caller.
2. Ask purpose of call.
3. Confirm if emergency.
4. If emergency:
   - Immediately collect name, phone number, and address.
   - Attempt transfer.
   - If transfer fails:
       Apologize and assure rapid follow-up.
5. If non-emergency:
   - Collect details.
   - Inform follow-up during business hours.
6. Ask if anything else needed.
7. Close politely.

IMPORTANT RULES:
- Do not mention internal systems.
- Do not mention function calls.
- Only collect information necessary for routing.
"""

    return prompt.strip()


def generate_agent_spec(account_id, version):
    memo_path = os.path.join(
        OUTPUT_BASE, account_id, version, "memo.json"
    )

    if not os.path.exists(memo_path):
        return

    with open(memo_path, "r", encoding="utf-8") as f:
        account_data = json.load(f)

    agent_spec = {
        "agent_name": f"{account_data.get('company_name', account_id)} Assistant",
        "voice_style": "Professional and calm",
        "system_prompt": build_system_prompt(account_data),
        "key_variables": {
            "business_hours": account_data.get("business_hours"),
            "emergency_definition": account_data.get("emergency_definition"),
            "integration_constraints": account_data.get("integration_constraints")
        },
        "call_transfer_protocol": account_data.get("call_transfer_rules"),
        "fallback_protocol": "If transfer fails, apologize and inform dispatch will follow up.",
        "version": version
    }

    agent_path = os.path.join(
        OUTPUT_BASE, account_id, version, "agent_spec.json"
    )

    with open(agent_path, "w", encoding="utf-8") as f:
        json.dump(agent_spec, f, indent=2)

    print(f"✅ Agent spec generated for {account_id} ({version})")


def main():
    accounts = os.listdir(OUTPUT_BASE)

    for account_id in accounts:
        for version in ["v1", "v2"]:
            generate_agent_spec(account_id, version)

    print("\n🎉 Agent specs generation complete.")


if __name__ == "__main__":
    main()