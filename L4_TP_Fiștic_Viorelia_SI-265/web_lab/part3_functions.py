# Laborator: funcții, metode și importuri pe web
# Student: Fiștic Viorelia

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import time
import requests


SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]


# Ex. 21 + Ex. 23: fetch cu parametru implicit pentru timeout
def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    return requests.get(url, timeout=timeout)


# Ex. 22 + Ex. 26: get_status cu adnotări de tip
def get_status(url: str) -> int:
    return fetch(url).status_code


# Ex. 24 + Ex. 25: get_title (fără rețea) cu docstring
def get_title(html: str) -> str:
    start = html.find("<title>")
    end = html.find("</title>")
    if start == -1 or end == -1:
        return ""
    start += len("<title>")
    return html[start:end].strip()


# Ex. 27
def page_exists(url: str) -> bool:
    try:
        return fetch(url).ok
    except requests.RequestException:
        return False


# Ex. 28
def check_paths(base: str, paths: list) -> dict:
    results = {}
    for i, path in enumerate(paths):
        if i > 0:
            time.sleep(1)
        results[path] = get_status(base + path)
    return results


# Ex. 29
def get_header(url: str, name: str, default: str = "lipsește") -> str:
    return fetch(url).headers.get(name, default)


# Ex. 30
def security_headers(url: str) -> dict:
    headers = fetch(url).headers
    return {name: name in headers for name in SECURITY_HEADERS}


# Ex. 31
def score_headers(results: dict) -> str:
    return f"{sum(results.values())}/{len(results)}"


# Ex. 32
def fetch_robots(base: str):
    try:
        response = fetch(base + "/robots.txt")
    except requests.RequestException:
        return None
    if response.status_code == 200:
        return response.text
    return None


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


# Ex. 33
def response_times(*urls: str) -> dict:
    times = {}
    for i, url in enumerate(urls):
        if i > 0:
            time.sleep(1)
        times[url] = fetch(url).elapsed.total_seconds()
    return times


# Ex. 34
def log(message: str, **details) -> None:
    parts = [message] + [f"{key}={value}" for key, value in details.items()]
    print(" | ".join(parts))


# ---------------------------------------------------------------
# Apeluri (fiecare funcție este apelată cel puțin o dată)
# ---------------------------------------------------------------
if __name__ == "__main__":
    print("Ex. 21:", fetch(BASE_URL).status_code)
    time.sleep(1)

    print("\nEx. 22:")
    for cale in ["/", "/robots.txt", "/sitemap.xml"]:
        print(cale, get_status(BASE_URL + cale))
        time.sleep(1)

    print("\nEx. 23:")
    print("timeout implicit:", fetch(BASE_URL).status_code)
    time.sleep(1)
    print("timeout=3:", fetch(BASE_URL, timeout=3).status_code)
    time.sleep(1)

    print("\nEx. 24:")
    html = fetch(BASE_URL).text
    print("Titlu:", get_title(html))

    print("\nEx. 25:")
    help(get_title)

    print("\nEx. 26:")
    try:
        get_status(123)  # type: ignore
    except requests.RequestException as err:
        print("Eroare la get_status(123):", type(err).__name__)
    # Adnotările de tip NU opresc apelul: Python nu le verifică la rulare.
    # Ele sunt doar documentație pentru oameni și pentru instrumente
    # (mypy, editorul). Aici eroarea apare abia în requests, nu din cauza hint-ului.
    time.sleep(1)

    print("\nEx. 27:")
    print(page_exists(BASE_URL))
    print(page_exists("https://this-domain-does-not-exist.invalid"))
    time.sleep(1)

    print("\nEx. 28:")
    print(check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))
    time.sleep(1)

    print("\nEx. 29:")
    print("Server:", get_header(BASE_URL, name="Server"))
    time.sleep(1)

    print("\nEx. 30 + 31:")
    rezultat = security_headers(BASE_URL)
    print(rezultat)
    print("Scor:", score_headers(rezultat))
    time.sleep(1)

    print("\nEx. 32:")
    robots = fetch_robots(BASE_URL)
    print("Disallow:", disallowed_paths(robots))
    print("Disallow pentru None:", disallowed_paths(None))
    time.sleep(1)

    print("\nEx. 33:")
    print(response_times(BASE_URL, BASE_URL + "/robots.txt"))

    print("\nEx. 34:")
    log("verificat", url=BASE_URL, status=200)

# ---------------------------------------------------------------
# Verificați-vă: print() vs return
# ---------------------------------------------------------------
# print() doar afișează o valoare pe ecran; funcția nu o poate folosi mai
# departe (apelantul primește None). return trimite valoarea înapoi
# apelantului, care o poate stoca, compara, salva sau transmite altei funcții.
