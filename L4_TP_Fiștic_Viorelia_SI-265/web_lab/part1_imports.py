# Laborator: funcții, metode și importuri pe web
# Student: Fiștic Viorelia

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import time

# Exercițiul 1. Primul import
import requests

print("Versiunea requests:", requests.__version__)

import urllib.request

# requests este o bibliotecă terță parte (third-party): nu vine cu Python,
# deci trebuie descărcată din PyPI cu `pip install requests`.
# urllib face parte din biblioteca standard, care este inclusă în
# interpretorul Python, deci este disponibilă imediat, fără instalare.

# Exercițiul 2. Două stiluri de import
print("\n--- Ex. 2 ---")
response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Stil 1 (requests.get):", response.status_code)

time.sleep(1)

from requests import get
response = get(BASE_URL, timeout=TIMEOUT)
print("Stil 2 (from requests import get):", response.status_code)

# Avantajul `import requests`: se vede mereu de unde vine funcția
#   (requests.get), deci nu apar conflicte de nume și codul e mai clar.
# Avantajul `from requests import get`: codul este mai scurt
#   (get(url) în loc de requests.get(url)).

# Exercițiul 3. Alias-uri
print("\n--- Ex. 3 ---")
time.sleep(1)

import requests as rq

response = rq.get(BASE_URL, timeout=TIMEOUT)
print("Cu alias rq:", response.status_code)

# Un alias face codul mai ușor de citit când numele este lung sau folosit
#   des și aliasul este unul consacrat de comunitate (import numpy as np,
#   import pandas as pd).
# Îl face mai greu de citit când aliasul este inventat sau criptic
#   (rq, r, x): un cititor nou nu știe ce este și trebuie să caute importul.

# Exercițiul 4. Doar biblioteca standard

print("\n--- Ex. 4 ---")
time.sleep(1)

with urllib.request.urlopen(BASE_URL, timeout=TIMEOUT) as resp:
    print("Status:", resp.status)
    corp = resp.read().decode("utf-8")  # .read() dă bytes -> decodăm în str
    print(corp[:200])




# Exercițiul 5. Priviți în interiorul unui modul

print("\n--- Ex. 5 ---")
print(dir(requests))

# requests.get       -> funcție
# requests.Session   -> clasă
# requests.exceptions -> modul (submodul al pachetului requests)


# Exercițiul 6. Citiți documentația



print("\n--- Ex. 6 ---")
help(requests.get)
# Parametrul care setează timpul maxim de așteptare este `timeout`
# (face parte din **kwargs, care ajung la requests.request).
time.sleep(1)
response = requests.get(BASE_URL, timeout=5)
print("Cerere cu timeout=5:", response.status_code)



# Exercițiul 7. Cronometrarea unei cereri


print("\n--- Ex. 7 ---")
time.sleep(1)


start = time.perf_counter()

response = requests.get(BASE_URL, timeout=TIMEOUT)
durata = time.perf_counter() - start

print(f"perf_counter: {durata:.3f} s")
print(f"response.elapsed: {response.elapsed.total_seconds():.3f} s")
# perf_counter măsoară totul: conectarea, cererea, descărcarea corpului și
# munca din requests. response.elapsed măsoară doar timpul de la trimiterea
# cererii până la sosirea antetelor răspunsului, deci este de obicei mai mic.


# Exercițiul 8. Când un import eșuează

print("\n--- Ex. 8 ---")
try:
    import bs4
    print("bs4 este instalat, versiunea", bs4.__version__)
    
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")


# Verificați-vă: modul vs pachet vs bibliotecă

# Modul    = un singur fișier .py (ex.: webtools.py).
# Pachet   = un director cu module (de obicei cu __init__.py), ex.: requests.
# Bibliotecă = termen general, nu strict tehnic: o colecție de module/pachete
#            care oferă funcționalități (ex.: biblioteca standard, requests).
