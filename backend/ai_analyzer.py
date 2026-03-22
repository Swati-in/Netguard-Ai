import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def analyze_logs(parsed_logs: list[dict]) -> list[dict]:
    if not parsed_logs:
        return []

    log_summary = ""
    for i, log in enumerate(parsed_logs):
        log_summary += f"\nLog #{i+1}:\n"
        for key, value in log.items():
            if key != "raw":
                log_summary += f"  {key}: {value}\n"

    prompt = f"""You are a senior network security analyst. Analyze the following parsed network logs and classify each one.

For each log entry, respond with a JSON array where each object has:
- "log_index": the log number (1-based)
- "severity": one of "CRITICAL", "WARNING", "NORMAL"
- "category": one of "BRUTE_FORCE", "PORT_SCAN", "SUSPICIOUS_HTTP", "FIREWALL_BLOCK", "NORMAL_TRAFFIC", "DATA_EXFILTRATION"
- "explanation": a single plain-English sentence explaining what is happening and why it is or isn't a threat
- "recommended_action": a short action like "Block IP", "Monitor", "Ignore", "Investigate"

Here are the logs to analyze:
{log_summary}

Respond ONLY with a valid JSON array. No markdown, no backticks, no extra text. Just the raw JSON array.
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw_response = response.content[0].text.strip()

    # Clean response just in case
    if raw_response.startswith("```"):
        raw_response = raw_response.split("```")[1]
        if raw_response.startswith("json"):
            raw_response = raw_response[4:]
    raw_response = raw_response.strip()

    ai_results = json.loads(raw_response)

    # Merge AI results back into parsed logs
    enriched_logs = []
    for i, log in enumerate(parsed_logs):
        ai_data = next((r for r in ai_results if r["log_index"] == i + 1), {})
        enriched_logs.append({
            **log,
            "severity": ai_data.get("severity", "UNKNOWN"),
            "category": ai_data.get("category", "UNKNOWN"),
            "explanation": ai_data.get("explanation", "No analysis available"),
            "recommended_action": ai_data.get("recommended_action", "Monitor")
        })

    return enriched_logs