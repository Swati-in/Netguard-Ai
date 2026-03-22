import time
import random
from log_parser import parse_bulk_logs
from ai_analyzer import analyze_logs
from db import save_logs
from bson import ObjectId

def clean_doc(doc: dict) -> dict:
    return {k: (str(v) if isinstance(v, ObjectId) else v) for k, v in doc.items()}

# --- Attack Log Templates ---

def ssh_brute_force_attack(target_ip="192.168.1.105"):
    logs = []
    usernames = ["root", "admin", "ubuntu", "pi", "oracle", "postgres", "user"]
    for i in range(8):
        logs.append(
            f"Mar 21 22:00:{str(i).zfill(2)} server sshd[1337]: Failed password for "
            f"{random.choice(usernames)} from {target_ip} port {random.randint(1024, 65535)} ssh2"
        )
    return logs

def port_scan_attack(attacker_ip="10.0.0.99"):
    ports = random.sample(range(1, 9999), 15)
    ports_str = ",".join(map(str, sorted(ports)))
    return [
        f"2026-03-21 22:00:00 PORTSCAN detected from {attacker_ip} ports={ports_str}"
    ]

def web_exploit_attack(attacker_ip="185.220.101.45"):
    logs = []
    payloads = [
        f'{attacker_ip} - - [21/Mar/2026:22:00:01 +0000] "GET /etc/passwd HTTP/1.1" 403 512',
        f'{attacker_ip} - - [21/Mar/2026:22:00:02 +0000] "GET /.env HTTP/1.1" 404 128',
        f'{attacker_ip} - - [21/Mar/2026:22:00:03 +0000] "POST /wp-admin HTTP/1.1" 401 256',
        f'{attacker_ip} - - [21/Mar/2026:22:00:04 +0000] "GET /admin/config HTTP/1.1" 403 512',
        f'{attacker_ip} - - [21/Mar/2026:22:00:05 +0000] "PUT /api/users HTTP/1.1" 200 1024',
    ]
    return payloads

def firewall_block_storm(attacker_ip="203.0.113.42"):
    logs = []
    ports = [22, 3306, 5432, 27017, 6379, 9200]
    for port in ports:
        logs.append(
            f"2026-03-21 22:00:00 FIREWALL BLOCK TCP src={attacker_ip} "
            f"dst=10.0.0.1 dport={port}"
        )
    return logs


# --- Scenario Runner ---

def run_scenario(name: str, raw_logs: list):
    print(f"\n{'='*50}")
    print(f"🚨 ATTACK SCENARIO: {name}")
    print(f"{'='*50}")
    print(f"📥 Injecting {len(raw_logs)} malicious log entries...")

    parsed = parse_bulk_logs(raw_logs)
    print(f"🔍 Parsed {len(parsed)} log entries")

    print(f"🤖 Sending to Claude AI for analysis...")
    enriched = analyze_logs(parsed)
    cleaned = [clean_doc(doc) for doc in enriched]
    save_logs(enriched)

    print(f"\n📊 Results:")
    for log in cleaned:
        severity = log.get("severity", "UNKNOWN")
        emoji = {"CRITICAL": "🔴", "WARNING": "🟡", "NORMAL": "✅"}.get(severity, "⚪")
        print(f"  {emoji} [{severity}] {log.get('explanation', 'N/A')}")
        print(f"     ⚡ Action: {log.get('recommended_action', 'N/A')}")

    return cleaned


def run_full_attack_simulation():
    print("\n" + "🔥"*25)
    print("   NETGUARD AI — ATTACK SIMULATION STARTING")
    print("🔥"*25)
    print("\n⚠️  Watch your dashboard at http://localhost:5173\n")

    # Scenario 1
    time.sleep(1)
    run_scenario(
        "SSH Brute Force Attack",
        ssh_brute_force_attack("192.168.1.105")
    )

    print("\n⏳ Next attack in 3 seconds...")
    time.sleep(3)

    # Scenario 2
    run_scenario(
        "Port Scan Reconnaissance",
        port_scan_attack("10.0.0.99")
    )

    print("\n⏳ Next attack in 3 seconds...")
    time.sleep(3)

    # Scenario 3
    run_scenario(
        "Web Application Exploit Attempt",
        web_exploit_attack("185.220.101.45")
    )

    print("\n⏳ Next attack in 3 seconds...")
    time.sleep(3)

    # Scenario 4
    run_scenario(
        "Firewall Block Storm",
        firewall_block_storm("203.0.113.42")
    )

    print("\n" + "✅"*25)
    print("   SIMULATION COMPLETE")
    print("✅"*25)
    print("\n🔄 Refresh your dashboard to see all detected threats!")


if __name__ == "__main__":
    run_full_attack_simulation()