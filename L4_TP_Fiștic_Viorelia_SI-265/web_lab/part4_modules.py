# Laborator: funcții, metode și importuri pe web
# Student: Fiștic Viorelia

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import hashlib
import json
import re
import socket
import ssl
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import requests


# Ex. 35
def describe_url(url: str) -> dict:
    p = urlparse(url)
    return {
        "scheme": p.scheme,
        "netloc": p.netloc,
        "path": p.path,
        "query": p.query,
        "fragment": p.fragment,
    }


# Ex. 36
def make_absolute(base: str, relative_links: list) -> list:
    return [urljoin(base, link) for link in relative_links]


# Ex. 37
def extract_links(html: str) -> list:
    links = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(links))


# Ex. 38
def split_links(links: list, domain: str) -> tuple:
    internal, external = [], []
    for link in links:
        full = urljoin("https://" + domain, link)
        parsed = urlparse(full)
        if parsed.scheme not in ("http", "https"):
            continue
        if parsed.netloc == domain:
            internal.append(full)
        else:
            external.append(full)
    return internal, external


# Ex. 39
class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)


# Testul din laborator: întâi pe HTML cunoscut
test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

finder = ImageFinder()
finder.feed(test_html)
print(finder.images)

assert finder.images == [
    "/logo.png",                            # imagine obișnuită
    "poza.jpg",                             # tag scris cu majuscule
    "https://cdn.example.com/banner.webp",  # tag care se închide singur
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul a trecut!")


def find_images(url: str) -> list:
    response = requests.get(url, timeout=TIMEOUT)
    finder = ImageFinder()
    finder.feed(response.text)
    print(len(finder.images), "imagini găsite")
    for src in finder.images:
        print(src)
    print("Număr '<img' în text:", response.text.lower().count("<img"))
    return finder.images


# Ex. 40
def page_fingerprint(url: str) -> str:
    response = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(response.content).hexdigest()


# Ex. 41
def save_headers(url: str, filename: str = "headers.json") -> None:
    response = requests.get(url, timeout=TIMEOUT)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(dict(response.headers), file, indent=2)


def load_header(filename: str, name: str) -> str:
    with open(filename, encoding="utf-8") as file:
        headers = json.load(file)
    return headers.get(name, "lipsește")


# Ex. 42
def resolve(hostname: str) -> str:
    return socket.gethostbyname(hostname)


# Ex. 43
def cert_days_left(hostname: str) -> int:
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as secure:
            cert = secure.getpeercert()
    expires = datetime.fromtimestamp(
        ssl.cert_time_to_seconds(cert["notAfter"]), tz=timezone.utc
    )
    return (expires - datetime.now(timezone.utc)).days


if __name__ == "__main__":
    print("\n--- Ex. 35 ---")
    for nume, valoare in describe_url("https://cybercor.org/path?x=1#top").items():
        print(f"{nume}: {valoare}")

    print("\n--- Ex. 36 ---")
    for rel, full in zip(["/about", "contact.html", "../index.html"],
                         make_absolute(BASE_URL, ["/about", "contact.html", "../index.html"])):
        print(rel, "->", full)

    print("\n--- Ex. 37 + 38 ---")
    html = requests.get(BASE_URL, timeout=TIMEOUT).text
    links = extract_links(html)
    print(len(links), "legături unice")
    interne, externe = split_links(links, "cybercor.org")
    print(len(interne), "interne,", len(externe), "externe")
    time.sleep(1)

    print("\n--- Ex. 39 (pagina reală) ---")
    find_images(BASE_URL)
    time.sleep(1)

    print("\n--- Ex. 40 ---")
    amprenta1 = page_fingerprint(BASE_URL)
    time.sleep(1)
    amprenta2 = page_fingerprint(BASE_URL)
    print(amprenta1)
    print(amprenta2)
    print("Identice:", amprenta1 == amprenta2)
    time.sleep(1)

    print("\n--- Ex. 41 ---")
    save_headers(BASE_URL)
    print("Content-Type din fișier:", load_header("headers.json", "Content-Type"))

    print("\n--- Ex. 42 ---")
    print("IP cybercor.org:", resolve("cybercor.org"))

    print("\n--- Ex. 43 ---")
    print("Zile rămase certificat:", cert_days_left("cybercor.org"))

# Verificați-vă: cine apelează handle_starttag()?

# O apelează chiar parserul (HTMLParser), din interiorul metodei feed():
# pe măsură ce citește HTML-ul și întâlnește un tag de deschidere, apelează
# automat handle_starttag(tag, attrs). Noi doar suprascriem metoda și
# lăsăm biblioteca să o apeleze.
