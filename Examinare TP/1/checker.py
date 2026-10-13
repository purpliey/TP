
import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    # scot "/" de la începutul lui path, ca să nu apară "//"
    return "https://" + host + "/" + path.lstrip("/")


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")



def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    try:
        r = requests.get(url, timeout=TIMEOUT)
        print("Status:", r.status_code)
        print("Content-Type:", r.headers.get("Content-Type"))
    except requests.RequestException as e:
        print("Cererea a eșuat:", type(e).__name__)


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        r = requests.get(url, timeout=TIMEOUT)
    except requests.Timeout:
        return {"status": None, "error": "timeout"}
    except requests.ConnectionError:
        return {"status": None, "error": "site inaccesibil"}
    except requests.RequestException as e:
        return {"status": None, "error": type(e).__name__}

    return {
        "status": r.status_code,
        "content_type": r.headers.get("Content-Type"),
        "length": len(r.content),
        "server": r.headers.get("Server", "unknown"),
    }


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    results = []
        for url in SITES:
            info = check_site(url)
            info["url"] = url
            results.append(info)




def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        r = requests.get(url, timeout=TIMEOUT)
    except requests.RequestException as e:
        return {"status": None, "error": type(e).__name__}
    present = [h for h in SECURITY_HEADERS if h in r.headers]
    missing = [h for h in SECURITY_HEADERS if h not in r.headers]
    score = len(present) * 100 // len(SECURITY_HEADERS)
    return {"present": present, "missing": missing, "score": score}


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    status = None
    error = None
    tries = 0

    while tries < attempts:
        tries += 1
        try:
            r = requests.get(url, timeout=TIMEOUT)
        except requests.RequestException as e:
            status = None
            error = type(e).__name__
            continue
        status = r.status_code
        error = None
        if status < 500:
            break
    result = {"status": status, "attempts": tries}
    if error is not None:
        result["error"] = error
    return result

