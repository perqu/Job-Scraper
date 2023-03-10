Job Scraper
=======
# Analizator potrzeb rynku

## Autor - Paweł Perenc


<!-- Zawartość -->
<details open="open">
  <summary>Zawartość</summary>
  <ol>
    <li>
      <a href="#opis-projektu">Opis Projektu</a>
      <ul>
        <li><a href="#użyte-technologie">Użyte technologie</a></li>
      </ul>
    </li>
    <li>
      <a href="#instalacja">Instalacja</a>
    </li>
    <li><a href="#użycie">Użycie</a></li>
    <li><a href="#przykład">Przykład</a></li>
    <li><a href="#licencja">Licencja</a></li>
    <li><a href="#kontakt">Kontakt</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## Opis Projektu

Projekt zostal stworzony, żeby w krótkim czasie z branży IT wydobyć najbardziej porzadane umiejętności dla konkretnego zawodu.

### Użyte technologie

* [Python](https://www.python.org/)
* [Selenium](https://selenium-python.readthedocs.io/)
* [Postgresql](https://www.postgresql.org/)

## Instalacja

1. Skopiowanie repozytorium
  ```sh
  git clone https://github.com/perqu/Rijndael-Cipher.git
  ``` 
2. Instalacja wymaganych bibliotek
  ```sh
  pip install -r requirements.txt
  ``` 
  
  
## Użycie
  1. W pliku main należy uzupełnić interesujace nas linki ze stron: bulldogjob, nofluffjobs i justjoinit. Przygotowac na kazdej ze stron interesujace nas wyszukiwanie, np w slowach kluczowych wpisac 'python developer', czy interesuja nas ogloszenia z podanymi zarobkami itp.Nastepnie tak przygotowane linki wkleic w pliku main.

  2. W pliku .env.example nalezy usunac rozszerzenie example i uzupełnic URL do bazy danych postresql.

  3. Uruchomic program w pliku main, po skonczeniu dzialania wszystkie ogloszenia zostana spisane do bazy danych.

  4. Przykladowa analiza danych znajduje sie w pliku show_results.py

## Przykład

![alt text](imgs\wykres.png)

## Licencja

Rozpowszechnione pod licencją MIT License.

## Kontakt
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/pawe%C5%82-perenc-51b39315a/
[product-screenshot]: images/screenshot.png
