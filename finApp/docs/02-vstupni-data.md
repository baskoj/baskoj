# 02 — Vstupní data

> Pro každý zdroj jeden Heading + popis + odkaz na vzorek v `data/samples/`.

---

## Use-case otázky

- Vstupní data na jednom místě (sdílený adresář = tento repo, hotovo).
- Informace o stavu peněz na začátku.
- Kdy se kam která částka přesouvala / zainvestovala.
- Typy investic → shrnutí investičního portfolia.
- Kde a jak uvidím průběžné stavy pro danou investici? (web, PDF atd.) `[ZKONTROLOVAT]`

---

## J&T výpis (PDF)

- **Frekvence:** měsíčně
- **Pole:** datum, ISIN, počet, cena, fee
- **Formát:** PDF
- **Problémy:** nezahrnuje splity
- **Vzorek:** `data/samples/jt/`

## XTB (`[ZKONTROLOVAT]`)

- **Frekvence:** `[ZKONTROLOVAT]`
- **Pole:** `[ZKONTROLOVAT]` (Daniel teprve sháněl vzorky)
- **Formát:** `[ZKONTROLOVAT]`
- **Problémy:** `[ZKONTROLOVAT]`
- **Vzorek:** `data/samples/xtb/`

## Degiro (`[ZKONTROLOVAT]`)

- **Frekvence:** `[ZKONTROLOVAT]`
- **Pole:** `[ZKONTROLOVAT]`
- **Formát:** `[ZKONTROLOVAT]`
- **Problémy:** `[ZKONTROLOVAT]`
- **Vzorek:** `data/samples/degiro/`

---

> **Poznámka:** Ve v1 začínáme jen XTB a Degiro (rozhodnutí 2026-05-26). J&T je referenční formát (existuje hotový report). Měny odloženy do v2.
