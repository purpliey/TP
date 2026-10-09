# Laborator: funcții, metode și importuri pe web
# Student: Fiștic Viorelia

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import argparse
import csv
import time
from datetime import datetime

# Ex. 44: import de modul întreg
import webtools
# Ex. 45: import de nume anume
from webtools import get_title, security_headers
# Ex. 47: importul constantei din modul
from webtools import DEFAULT_HEADERS

# Ex. 45: dacă main.py ar avea și o funcție proprie get_title, numele
# get_title ar indica ultima definiție/import întâlnit: definiția locală
# ar înlocui funcția importată (sau invers, dacă importul vine după def),
# fără niciun avertisment. De aceea webtools.get_title evită conflictul.

# Ex. 46: `python webtools.py` -> __name__ == "__main__" -> autotestul rulează.
# `python main.py` importă webtools, iar acolo __name__ == "webtools", deci
# blocul `if __name__ == "__main__"` din webtools nu se execută.


def save_csv(results: dict, filename: str = "report.csv") -> None:
    
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        writer.writerow(["path", "status", "checked_at"])
        for path, status in results.items():
            writer.writerow([path, status, datetime.now().isoformat()])


def main() -> None:

    # Ex. 48: URL-ul vine din linia de comandă, nu din BASE_URL
    parser = argparse.ArgumentParser(description="Analizează un site web.")
    parser.add_argument("url", help="ex.: https://cybercor.org")
    
    args = parser.parse_args()
    url = args.url.rstrip("/")

    # Ex. 44
    response = webtools.fetch(url)
    print("Titlu (webtools.get_title):", webtools.get_title(response.text))
    
    time.sleep(1)

    # Ex. 45 (nume importate direct)
    print("Titlu (get_title):", get_title(response.text))
    
    
    print("Antete de securitate:", security_headers(url))
    time.sleep(1)

    # Ex. 47
    print("DEFAULT_HEADERS:", DEFAULT_HEADERS)

    # Ex. 49
    rezultate = webtools.check_paths(url, ["/", "/robots.txt", "/sitemap.xml"])
    save_csv(rezultate)
    
    
    print("Salvat în report.csv")
    time.sleep(1)

    # Ex. 50
    print()
    
    webtools.site_report(url)


if __name__ == "__main__":
    main()
