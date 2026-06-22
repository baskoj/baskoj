# finApp

finApp je aplikace, která na základě vstupních dat (PDF export, webový přehled, Excel) sestaví přehled portfolia za zvolené období — měsíc, půlrok nebo rok. Cíl je mít všechny investice na jednom místě: akcie, dluhopisy, fondy, krypto, cenné kovy i forex.

## Aktuální stav

- Sólo práce: Jan Basko (JB)
- Fáze: v1
- Brokeři v1: XTB + Degiro
- Klíčová metrika: TWR (Time-Weighted Return)
- Priorita teď: vyřešit vstupní data (formáty, parsování)
- Výstup v tuto chvíli: projektová struktura + paměť projektu

## Jak pracovat s tímto repem

- Zdroj pravdy je tento git repo, ne iCloud. iCloud slouží jako mobilní zápisník — obsah se z něj přelévá sem.
- **Nemaž nic.** Složka `App/` je archiv. Decision log je append-only.
- Nejisté nebo neověřené informace označuj `[ZKONTROLOVAT]`.
- Událost nebo změna rozhodnutí → zapiš do `docs/06-decision-log.md`. Trvalé pravidlo nebo fakt → `memory.md`. Neduplikovat.
- CLAUDE.md drží jen současný stav; historie a chronologie patří do `roadmap.md` a `docs/06-decision-log.md`.

## Struktura

```
finApp/
├── CLAUDE.md          # aktuální stav projektu (tento soubor)
├── memory.md          # trvalá fakta a platná pravidla
├── roadmap.md         # fáze projektu
├── docs/              # číslované poznámky (vision, scope, data, metriky, wireframy…)
├── data/              # vzorky vstupních dat
└── App/               # archiv (.pages, PDF) — nemaže se
```
