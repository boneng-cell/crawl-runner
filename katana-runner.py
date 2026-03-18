import subprocess
import os
import sys
from urllib.parse import urlparse

target = os.getenv("TARGET", "").strip()
cookie = os.getenv("COOKIE", "").strip()
use_headers = os.getenv("USE_HEADERS", "false").lower() == "true"
if not target:
    print("ERROR: TARGET tidak boleh kosong")
    sys.exit(1)
if not target.startswith("http://") and not target.startswith("https://"):
    target = "https://" + target
parsed = urlparse(target)
if not parsed.hostname:
    print("ERROR: URL tidak valid")
    sys.exit(1)
domain = parsed.hostname
if parsed.port:
    domain = f"{domain}_{parsed.port}"
output = f"{domain}.txt"
headers = []
if use_headers:
    headers.extend([
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language: en-US,en;q=0.9",
        "Referer: https://google.com"
    ])
if cookie:
    headers.append(f"Cookie: {cookie}")
cmd = ["katana", "-u", target]
for h in headers:
    cmd.extend(["-H", h])
cmd.extend([
    "-fr", "(logout|log-out|signout|sign-out|sign_off|exit|destroy|terminate|delete-session|invalidate)",
    "-jc", "-xhr", "-fx",
    "-d", "5",
    "-c", "5",
    "-rl", "3",
    "-rd", "2",
    "-timeout", "15",
    "-retry", "2",
    "-tlsi",
    "-aff",
    "-s", "breadth-first",
    "-o", output
])
print("[INFO] Running command:")
print(" ".join(cmd))
go_bin = os.path.expanduser("~/go/bin")
os.environ["PATH"] += os.pathsep + go_bin
try:
    subprocess.run(cmd, check=True)
except FileNotFoundError:
    print("ERROR: Katana tidak ditemukan di PATH")
    sys.exit(1)
except subprocess.CalledProcessError as e:
    print(f"ERROR: Katana gagal ({e})")
    sys.exit(1)
print(f"[INFO] Output saved to: {output}")
