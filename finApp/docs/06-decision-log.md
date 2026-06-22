# 06 — Decision log

Tahle poznámka je chronologická, odshora. Pravidlo: nikdy nepřepisuj staré záznamy. Pokud se rozhodnutí změní, napiš nový řádek s datem a poznámkou 'ruší YYYY-MM-DD'. Každé rozhodnutí = nový řádek.

---

## 2026-05-26 (JB)

- Založení adresáře Financial App.
- Doplnění jednotlivých Notes.
- Pozvánka odeslána Danielovi — důležité poznámky držet zde, ne v iMessage / WhatsApp.
- Začátek — doplnění vize (JB, Daniel).
- Rozhodnutí: Začínáme jen s XTB a Degiro. Ostatní brokeři až v2.

## 2026-05-27

- Daniel: doplnil vizi.
- JB: vytvoření sdíleného adresáře pro vstupní data (finApp folder).

## 2026-05-28

- TWR je P1, ne P2. Bez něj nemá výnos smysl.

## 2026-05-30 (JB)

- Obrázek pro level one — appka mezi JB a Danielem.

## 2026-06-22 (JB)

- Promítnut ruční náčrt vize ze syncu Honza + Dan do struktury.
- Zaveden `docs/07-architektura.md` s datovou pipeline: vstupní data → robot/scraper → transformace (web rozhraní) → nativní appka (Android/iOS), white-label instance APP1/APP2.
- Roadmapa doplněna o 4 kroky rolloutu (STEP 1–4) a STEP 4 = pasivní měsíční náhled pro koncové klienty.
- Otevřeno k rozhodnutí: forma výstupu — statický report (v1) vs. nativní app (cíl). Označeno `[ZKONTROLOVAT]` v `05-vystup.md`.
- **Reálné portfolio:** dodán kompletní přehled (`data/Baškovi.numbers`). Původní „XTB + Degiro" byl jen vzor — **ruší se** (ruší 2026-05-26 v této části). Reálné zdroje v1 = J&T Banka, FKI, Roboforex/Vantage, Komerční banka, kryptoměny; projekty a nemovitost manuálně.
- `02-vstupni-data.md` a `roadmap.md` přepsány na reálné zdroje; přidán `08-portfolio.md` (struktura aktiv bez částek).
- `data/samples/` srovnány: odebráno xtb/degiro, přidáno fki/roboforex/kb/krypto (jt zůstává).
- `*.numbers` přidáno do `.gitignore` — soubor obsahuje citlivé částky, necommituje se.
