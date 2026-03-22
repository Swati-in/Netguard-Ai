import random
from faker import Faker
from datetime import datetime

fake = Faker()

def generate_log_line():
    log_types = [
        generate_ssh_log,
        generate_http_log,
        generate_firewall_log,
        generate_port_scan_log,
    ]
    return random.choice(log_types)()

def generate_ssh_log():
    status = random.choices(
        ["Failed password", "Accepted password", "Invalid user"],
        weights=[60, 20, 20]
    )[0]
    ip = fake.ipv4_public()
    user = random.choice(["root", "admin", "ubuntu", "pi", fake.user_name()])
    port = random.randint(1024, 65535)
    timestamp = datetime.now().strftime("%b %d %H:%M:%S")
    return f"{timestamp} server sshd[{random.randint(1000,9999)}]: {status} for {user} from {ip} port {port} ssh2"

def generate_http_log():
    ip = fake.ipv4_public()
    method = random.choice(["GET", "POST", "PUT", "DELETE"])
    path = random.choice(["/admin", "/login", "/api/users", "/.env", "/wp-admin", "/etc/passwd"])
    status = random.choices([200, 401, 403, 404, 500], weights=[30, 20, 20, 20, 10])[0]
    size = random.randint(100, 5000)
    timestamp = datetime.now().strftime("%d/%b/%Y:%H:%M:%S +0000")
    return f'{ip} - - [{timestamp}] "{method} {path} HTTP/1.1" {status} {size}'

def generate_firewall_log():
    action = random.choices(["BLOCK", "ALLOW"], weights=[40, 60])[0]
    src_ip = fake.ipv4_public()
    dst_ip = fake.ipv4_private()
    port = random.choice([22, 80, 443, 3306, 5432, 6379, 27017])
    protocol = random.choice(["TCP", "UDP"])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{timestamp} FIREWALL {action} {protocol} src={src_ip} dst={dst_ip} dport={port}"

def generate_port_scan_log():
    ip = fake.ipv4_public()
    ports = sorted(random.sample(range(1, 9999), random.randint(5, 15)))
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{timestamp} PORTSCAN detected from {ip} ports={','.join(map(str, ports))}"

def generate_bulk_logs(n=20):
    return [generate_log_line() for _ in range(n)]