import re
from datetime import datetime

def parse_log_line(raw_log: str) -> dict:
    raw_log = raw_log.strip()

    # Try SSH log
    ssh_match = re.search(
        r"sshd\[\d+\]:\s+(Failed password|Accepted password|Invalid user)"
        r".*?for\s+(\S+)\s+from\s+([\d.]+)\s+port\s+(\d+)",
        raw_log
    )
    if ssh_match:
        status, user, ip, port = ssh_match.groups()
        threat = "high" if status in ["Failed password", "Invalid user"] else "low"
        return {
            "type": "SSH",
            "status": status,
            "user": user,
            "ip": ip,
            "port": int(port),
            "threat_hint": threat,
            "raw": raw_log,
            "timestamp": datetime.now().isoformat()
        }

    # Try HTTP log
    http_match = re.search(
        r'([\d.]+).*?"(\w+)\s+(\S+)\s+HTTP.*?"\s+(\d{3})\s+(\d+)',
        raw_log
    )
    if http_match:
        ip, method, path, status, size = http_match.groups()
        suspicious_paths = ["/.env", "/wp-admin", "/admin", "/etc/passwd", "/login"]
        threat = "high" if path in suspicious_paths or status.startswith("4") else "low"
        return {
            "type": "HTTP",
            "ip": ip,
            "method": method,
            "path": path,
            "status_code": int(status),
            "size": int(size),
            "threat_hint": threat,
            "raw": raw_log,
            "timestamp": datetime.now().isoformat()
        }

    # Try Firewall log
    fw_match = re.search(
        r"FIREWALL\s+(BLOCK|ALLOW)\s+(\w+)\s+src=([\d.]+)\s+dst=([\d.]+)\s+dport=(\d+)",
        raw_log
    )
    if fw_match:
        action, protocol, src, dst, port = fw_match.groups()
        threat = "high" if action == "BLOCK" else "low"
        return {
            "type": "FIREWALL",
            "action": action,
            "protocol": protocol,
            "src_ip": src,
            "dst_ip": dst,
            "port": int(port),
            "threat_hint": threat,
            "raw": raw_log,
            "timestamp": datetime.now().isoformat()
        }

    # Try Port Scan log
    ps_match = re.search(
        r"PORTSCAN detected from ([\d.]+) ports=([\d,]+)",
        raw_log
    )
    if ps_match:
        ip, ports = ps_match.groups()
        return {
            "type": "PORTSCAN",
            "ip": ip,
            "ports": [int(p) for p in ports.split(",")],
            "port_count": len(ports.split(",")),
            "threat_hint": "critical",
            "raw": raw_log,
            "timestamp": datetime.now().isoformat()
        }

    # Unknown log type
    return {
        "type": "UNKNOWN",
        "threat_hint": "low",
        "raw": raw_log,
        "timestamp": datetime.now().isoformat()
    }


def parse_bulk_logs(raw_logs: list[str]) -> list[dict]:
    return [parse_log_line(log) for log in raw_logs if log.strip()]