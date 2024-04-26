import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time
import os
r = requests.get('https://www.tiobe.com/tiobe-index/')
soup = BeautifulSoup(r.text, 'html.parser')
tabelajezykow = soup.table
lista = []

LINKIDOSTRON = [ #GDY JEST BLAD 429
'https://en.wikipedia.org/wiki/Python_(programming_language)'
'https://en.wikipedia.org/wiki/C_(programming_language)'
'https://en.wikipedia.org/wiki/C%2B%2B'
'https://en.wikipedia.org/wiki/Java_(programming_language)'
'https://en.wikipedia.org/wiki/C_Sharp_(programming_language)'
'https://en.wikipedia.org/wiki/JavaScript'
'https://en.wikipedia.org/wiki/SQL'
'https://en.wikipedia.org/wiki/Go_(programming_language)'
'https://en.wikipedia.org/wiki/Visual_Basic_(.NET)'
'https://en.wikipedia.org/wiki/PHP'
'https://en.wikipedia.org/wiki/Fortran'
'https://en.wikipedia.org/wiki/Delphi_(software)'
'https://en.wikipedia.org/wiki/MATLAB'
'https://en.wikipedia.org/wiki/Assembly_language'
'https://en.wikipedia.org/wiki/Scratch_(programming_language)'
'https://en.wikipedia.org/wiki/Swift_(programming_language)'
'https://en.wikipedia.org/wiki/Kotlin_(programming_language)'
'https://en.wikipedia.org/wiki/Rust_(programming_language)'
'https://en.wikipedia.org/wiki/COBOL'
'https://en.wikipedia.org/wiki/Ruby_(programming_language)'
]

lista_jezykow = []

# Pobierz ścieżkę do folderu, w którym znajduje się bieżący plik .py
folder_biezacego_pliku = os.path.dirname(os.path.abspath(__file__))

# Tworzenie nowego folderu w tym samym miejscu
sciezka_do_folderu = os.path.join(folder_biezacego_pliku, "assets")

# Utworzenie nowego folderu
os.makedirs(sciezka_do_folderu, exist_ok=True)

rows = tabelajezykow.find_all('tr')
i = 0
for row in rows:
    cells = row.find_all(['td', 'th'])
    row_data = ""
    j = 0
    para = []
    nazwa_pliku_lokalnego3 = ""
    for cell in cells:
        if i != 0:
            if j == 4:
                para.append("[" + cell.text + "](" + "/stronaglowna/stronazlista/" + nazwa_pliku_lokalnego3 +")")
            if j == 3: #pobieramy plik obrazkowy
                para.append(str(i) + '.')
                url = "https://www.tiobe.com" + cell.img['src']
                nazwa_pliku_lokalnego =""
                linkjakotablica = list(url)

                k = len(linkjakotablica) - 1
                while linkjakotablica[k] != '/':
                    nazwa_pliku_lokalnego = linkjakotablica[k] + nazwa_pliku_lokalnego
                    k = k - 1


                nazwa_pliku_lokalnego2 = ""

                n = 0
                while(nazwa_pliku_lokalnego[n] != '.'):
                    nazwa_pliku_lokalnego2 = nazwa_pliku_lokalnego2 + nazwa_pliku_lokalnego[n]
                    n = n + 1
                nazwa_pliku_lokalnego3 = nazwa_pliku_lokalnego2
                nazwa_pliku_lokalnego2 = nazwa_pliku_lokalnego2 + ".md"
                lista_jezykow.append(nazwa_pliku_lokalnego3)

                nazwa_pliku_lokalnego = "/assets/" + nazwa_pliku_lokalnego


                response = requests.get(url)

                with open(nazwa_pliku_lokalnego, 'wb') as f:
                    f.write(response.content)
                para.append("!["+nazwa_pliku_lokalnego +"]("+nazwa_pliku_lokalnego+")")
            j = j + 1
    lista.append(para)
    i = i + 1 

nazwa_pliku = "jezykiprogramowania.md"

with open(nazwa_pliku, "w") as plik:
    plik.write("---\n")
    plik.write("layout: page\n")
    plik.write("title: stronazlista\n")
    plik.write("permalink: /stronaglowna/stronazlista \n")
    plik.write("---\n")
    for jezyk in lista:
        linia = ", ".join(map(str, jezyk))
        plik.write("- " + linia + "\n")



for jezyki in lista_jezykow:
    nazwa_pliku = jezyki
    szukanafraza = "site: wikipedia.org/wiki/" + jezyki + " (programming language)"
    nazwa_pliku = nazwa_pliku + ".md"
    time.sleep(10)

    results = search(szukanafraza, stop = 1, lang='en')
    for wynikwyszukiwania in results:
        odp = requests.get(wynikwyszukiwania)
        print(wynikwyszukiwania)
        zupa = BeautifulSoup(odp.text, 'html.parser')
        first_table = zupa.find('table', class_='infobox vevent')
        if first_table is not None:
            next_paragraph = first_table.find_next_sibling('p')
        else:
            next_paragraph = zupa.find('p')
        with open(nazwa_pliku, "w", encoding = "utf-8") as pierwszyakapit:
            pierwszyakapit.write("---\n")
            pierwszyakapit.write("layout: page\n")
            pierwszyakapit.write("title: " + jezyki +"\n")
            pierwszyakapit.write("permalink: /stronaglowna/stronazlista/" + jezyki +"\n")
            pierwszyakapit.write("---" + "\n")
            pierwszyakapit.write(next_paragraph.text.strip())

nazwa_pliku = "stronaglowna.md"
req = requests.get("https://en.wikipedia.org/wiki/TIOBE_index")
soup2 = BeautifulSoup(req.text, 'html.parser')
odnosnik = soup2.find('figure', class_= "mw-default-size")
zawartosc = odnosnik.find_next_sibling('p')
with open(nazwa_pliku, "w", encoding = "utf-8") as strgl:
    strgl.write("---\n")
    strgl.write("layout: page\n")
    strgl.write("title: stronaglowna\n")
    strgl.write("permalink: /stronaglowna/\n")
    strgl.write("---\n")
    strgl.write(zawartosc.text.strip() + "\n")
    strgl.write("[stronazlista](/stronaglowna/stronazlista)")