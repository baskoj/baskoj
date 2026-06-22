# data/

## Co sem patří

Syrové vzorky výpisů z brokerů (PDF/CSV), roztříděné do `samples/<broker>/`.

## Jak data tečou dovnitř

1. Stáhnu výpis z brokera.
2. Uložím do `samples/<broker>/`.
3. Zapíšu pole / formát / problémy do `docs/02-vstupni-data.md`.

## Bezpečnost

Pokud výpis obsahuje citlivé částky nebo osobní údaje, **NEcommitovat ho do gitu** — přidej do `.gitignore` nebo drž lokálně. Vzorky pro vývoj raději anonymizovat. `[ZKONTROLOVAT]`
