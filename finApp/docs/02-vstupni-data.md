# 02 — Vstupní data

> Pro každý zdroj jeden Heading + popis + odkaz na vzorek v `data/samples/`.
> Zdroje odpovídají **reálnému portfoliu** (viz `08-portfolio.md`). Dřívější XTB/Degiro byly jen vzor — odstraněno (rozhodnutí 2026-06-22).

---

## Use-case otázky

- Vstupní data na jednom místě (sdílený adresář = tento repo, hotovo).
- Informace o stavu peněz na začátku.
- Kdy se kam která částka přesouvala / zainvestovala.
- Typy investic → shrnutí investičního portfolia.
- Kde a jak uvidím průběžné stavy pro danou investici? (web, PDF atd.) `[ZKONTROLOVAT]`

### Co k cíli (period summary + TWR) chybí napříč všemi zdroji

- **Časová řada** — máme jen snímek k jednomu dni, ne historii hodnot v čase.
- **Datované transakce / cashflow** — vklady/výběry s daty (TWR je potřebuje).
- **Datum ocenění** — k jakému dni hodnoty platí.

---

## J&T Banka — aktivní správa majetku (PDF)

- **Frekvence:** měsíčně
- **Pole:** datum, ISIN, počet, cena, fee
- **Formát:** PDF výpis
- **Zdroj:** měsíční PDF report (✓ už umíme parsovat — skill `jt-portfolio-report`)
- **Problémy:** nezahrnuje splity
- **Vzorek:** `data/samples/jt/`

## FKI — fondy kvalifikovaných investorů (J&T Arch, Realia Group, Atris, The Julius Fund)

- **Frekvence:** `[ZKONTROLOVAT]`
- **Pole:** `[ZKONTROLOVAT]` (hodnota podílu, počet podílů, vklad)
- **Formát:** výpis / report od správce fondu `[ZKONTROLOVAT]`
- **Zdroj:** `[ZKONTROLOVAT]` (správce fondu — web/PDF?)
- **Problémy:** oceňování často kvartálně, ne denně `[ZKONTROLOVAT]`
- **Vzorek:** `data/samples/fki/`

## Roboforex / Vantage — Enigma Wise (Enigma Profi, Profi 2.0)

- **Frekvence:** `[ZKONTROLOVAT]`
- **Pole:** `[ZKONTROLOVAT]` (stav účtu, equity, vklad, P&L)
- **Formát:** `[ZKONTROLOVAT]` (obchodní platforma — MT4/MT5? export?)
- **Zdroj:** web / login do platformy `[ZKONTROLOVAT]`
- **Problémy:** `[ZKONTROLOVAT]`
- **Vzorek:** `data/samples/roboforex/`

## Komerční banka — uzavřené fondy

- **Frekvence:** `[ZKONTROLOVAT]`
- **Pole:** `[ZKONTROLOVAT]`
- **Formát:** výpis `[ZKONTROLOVAT]`
- **Zdroj:** `[ZKONTROLOVAT]` (internetové bankovnictví / PDF?)
- **Problémy:** část s ukončením 2029 (4 % p.a.) je budoucí projekce, ne aktuální hodnota
- **Vzorek:** `data/samples/kb/`

## Kryptoměny (ETH, plánované BTC)

- **Frekvence:** real-time (trh)
- **Pole:** množství, kurz, hodnota
- **Formát:** `[ZKONTROLOVAT]`
- **Zdroj:** burza / on-chain peněženka `[ZKONTROLOVAT]` (kurz lze brát z veřejných dat / API)
- **Problémy:** vysoká volatilita; nutné datum/čas ocenění
- **Vzorek:** `data/samples/krypto/`

## Projekty — soukromé investice (Greels Capital a.s.)

- **Frekvence:** nepravidelně / dle událostí
- **Pole:** vklad, současná hodnota, datum ukončení
- **Formát:** bez výpisu — **manuální** `[ZKONTROLOVAT]`
- **Zdroj:** ruční zadání
- **Problémy:** ocenění je odhad, ne tržní cena
- **Vzorek:** —

## Nemovitost — zahraničí (Dubai)

- **Frekvence:** nepravidelně
- **Pole:** pořizovací hodnota, měna
- **Formát:** **manuální** `[ZKONTROLOVAT]`
- **Zdroj:** ruční zadání
- **Problémy:** cizí měna (AED/USD?) — řešení měn až **v2**
- **Vzorek:** —

---

> **Poznámka ke scope v1:** reálné zdroje v1 = J&T Banka, FKI, Roboforex/Vantage, Komerční banka, kryptoměny. Projekty a nemovitost zatím manuálně. Měny (Dubai) odloženy do v2. (rozhodnutí 2026-06-22 — nahrazuje původní XTB+Degiro z 2026-05-26)
