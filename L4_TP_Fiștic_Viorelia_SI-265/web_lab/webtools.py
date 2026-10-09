# Laborator: funcții, metode și importuri pe web
# Student: Fiștic Viorelia

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde
# Modul cu funcții reutilizabile pentru analiza unui site web.

import json
import re
import socket
import ssl
import time
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

import requests


# Ex. 47: constantă de modul, folosită în fetch()
DEFAULT_HEADERS = {"User-Agent": "WebLab-NumePrenume"}

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]


def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)


def get_status(url: str) -> int:
    return fetch(url).status_code


def get_title(html: str) -> str:
    start = html.find("<title>")
    end = html.find("</title>")
    if start == -1 or end == -1:
        return ""
    return html[start + len("<title>"):end].strip()


def security_headers(url: str) -> dict:
    headers = fetch(url).headers
    return {name: name in headers for name in SECURITY_HEADERS}


def score_headers(results: dict) -> str:
    return f"{sum(results.values())}/{len(results)}"


def check_paths(base: str, paths: list) -> dict:
    results = {}
    for i, path in enumerate(paths):
        if i > 0:
            time.sleep(1)
        results[path] = get_status(base + path)
    return results


def extract_links(html: str) -> list:
    return list(dict.fromkeys(re.findall(r'href="([^"]+)"', html)))


def split_links(links: list, domain: str) -> tuple:
    internal, external = [], []
    for link in links:
        full = urljoin("https://" + domain, link)
        parsed = urlparse(full)
        if parsed.scheme not in ("http", "https"):
            continue
        (internal if parsed.netloc == domain else external).append(full)
    return internal, external


def fetch_robots(base: str):
    try:
        response = fetch(base + "/robots.txt")
    except requests.RequestException:
        return None
    return response.text if response.status_code == 200 else None


def disallowed_paths(robots_text) -> list:
    if not robots_text:
        return []
    paths = []
    for line in robots_text.splitlines():
        line = line.split("#", 1)[0].strip()
        if line.lower().startswith("disallow:"):
            value = line.split(":", 1)[1].strip()
            if value:
                paths.append(value)
    return paths


def resolve(hostname: str) -> str:
    return socket.gethostbyname(hostname)


def cert_days_left(hostname: str) -> int:
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as secure:
            cert = secure.getpeercert()
    expires = datetime.fromtimestamp(
        ssl.cert_time_to_seconds(cert["notAfter"]), tz=timezone.utc
    )
    return (expires - datetime.now(timezone.utc)).days


def redirect_chain(http_url: str) -> list:
    response = fetch(http_url)
    chain = []
    for step in response.history:
        chain.append(f"{step.status_code} -> {step.headers.get('Location', '?')}")
    return chain


def _safe(func, *args):
    try:
        return func(*args)
    except (requests.RequestException, OSError, ssl.SSLError, KeyError):
        return None


def site_report(url: str, out_file: str = "report.json") -> dict:
    host = urlparse(url).netloc
    hostname = urlparse(url).hostname

    response = fetch(url)
    html = response.text
    time.sleep(1)

    chain = _safe(redirect_chain, "http://" + host + "/")
    time.sleep(1)

    headers_result = _safe(security_headers, url)
    time.sleep(1)

    robots = fetch_robots(url)
    internal, external = split_links(extract_links(html), host)

    report = {
        "url": url,
        "status": response.status_code,
        "final_url": response.url,
        "title": get_title(html),
        "ip": _safe(resolve, hostname),
        "redirects": chain,
        "security_score": score_headers(headers_result) if headers_result else None,
        "security_headers": headers_result,
        "cert_days_left": _safe(cert_days_left, hostname),
        "internal_links": len(internal),
        "external_links": len(external),
        "disallowed": disallowed_paths(robots),
    }

    if chain is None:
        redirects_txt = "indisponibil"
    else:
        redirects_txt = ", ".join(chain) if chain else "fără redirecționări"
    cert = report["cert_days_left"]
    if cert is None:
        cert_txt = "indisponibil"
    else:
        de = "" if 0 < cert % 100 < 20 else "de "
        cert_txt = f"{cert} {de}zile rămase"
    disallowed_txt = ", ".join(report["disallowed"]) or "niciuna"

    print(f"=== Raport site: {url} ===")
    print(f"{'Cod de stare:':<18}{report['status']}")
    print(f"{'URL final:':<18}{report['final_url']}")
    print(f"{'Titlu:':<18}{report['title']}")
    print(f"{'Adresă IP:':<18}{report['ip']}")
    print(f"{'Redirecționări:':<18}{redirects_txt}")
    print(f"{'Scor securitate:':<18}{report['security_score']}")
    print(f"{'Certificat:':<18}{cert_txt}")
    print(f"{'Legături:':<18}{len(internal)} interne, {len(external)} externe")
    print(f"{'Căi interzise:':<18}{disallowed_txt}")

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"Salvat în {out_file}")
    return report


# Ex. 46: `python webtools.py` -> __name__ == "__main__" -> autotestul rulează.
# Dacă alt fișier face `import webtools`, __name__ devine "webtools", deci
# blocul de mai jos nu se execută.
if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))
