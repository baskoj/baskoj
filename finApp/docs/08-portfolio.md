# 08 — Struktura portfolia

> Reálná struktura portfolia (zdroj: `data/Baškovi.numbers`, snímek ~2026-06-02).
> **Bez konkrétních částek** — citlivé hodnoty zůstávají jen v `.numbers` souboru (necommituje se, viz `data/README.md`).
> Tento soubor je „mapa" aktiv a jejich zdrojů, na kterou navazuje `02-vstupni-data.md`.

## Současná aktiva (skupiny a přibližný podíl)

| Skupina | Podíl | Typ | Zdroj dat |
|---|--:|---|---|
| J&T Banka — aktivní správa | ~42 % | správa majetku | měsíční PDF report (✓ parsujeme) |
| Roboforex / Vantage (Enigma Wise) | ~24 % | obchodní účty (Profi, Profi 2.0) | platforma web/login `[ZKONTROLOVAT]` |
| FKI — fondy kval. investorů (J&T Arch ad.) | ~13 % | fondy | výpis správce `[ZKONTROLOVAT]` |
| Komerční banka — uzavřené fondy | ~11 % | fondy | výpis `[ZKONTROLOVAT]` |
| Kryptoměny (ETH) | ~6 % | krypto | burza / on-chain `[ZKONTROLOVAT]` |
| Projekty (Greels Capital a.s.) | ~4 % | soukromá investice | manuální |

U skupin J&T, Roboforex a FKI eviduje zdroj i **vklad** a **kumulativní zisk** — užitečné pro pozdější výnos/TWR.

## Plánované / budoucí (mimo aktuální součet majetku)

- Komerční banka — ukončení 2029 (4 % p.a.) — budoucí projekce
- Nemovitost — zahraničí, Dubai (2029–2030) — pořizovací hodnota, cizí měna (→ v2)
- Projekty — ukončení 2026 (Greels Capital) — projektovaná výstupní hodnota
- Kryptoměny — plánované (BTC)
- Plánované roční zhodnocení (p.a.): J&T 10 %, Roboforex 20 %, FKI 8 %

## Otevřené / chybí pro cíl (period summary + TWR)

- `[ZKONTROLOVAT]` **Datum ocenění** současných hodnot.
- `[ZKONTROLOVAT]` **Historie hodnot v čase** (měsíční snímky) nebo **datovaný cashflow** (vklady/výběry) — bez toho nelze spočítat TWR ani „co se dělo za období".
- `[ZKONTROLOVAT]` Detail po jednotlivých instrumentech (ISIN/počet/cena) u fondů — teď je to agregát po skupinách.
- `[ZKONTROLOVAT]` Měny u ne-CZK aktiv (Dubai).
