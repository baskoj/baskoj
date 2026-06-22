# finApp — projektová struktura (design)

**Datum:** 2026-06-22
**Autor:** Jan Basko (JB), s asistencí Claude
**Stav:** schváleno k implementaci

---

## Kontext

`finApp` je produktový projekt, který JB staví s Danielem (zmíněn i Peťa). Cíl produktu: aplikace,
která klientovi / investičnímu poradci na základě vstupních dat (PDF export, web, Excel) shrne, co se
s portfoliem dělo za měsíc / půlrok / rok. Jeden přehled všech investic na jednom místě
(akcie, dluhopisy, fondy, krypto, cenné kovy, forex).

Projekt už používá metodiku **číslovaných poznámek Pavla Ungra** v iCloud Notes
(00 Vision, 02 Vstupní data, 04 Wireframy, 06 Decision log, 10 Meeting notes, Z1 quick notes).

**Tento dokument NEŘEŠÍ samotnou aplikaci.** Řeší jen *projektovou strukturu* v git repu `finApp` —
aby se s projektem dalo konzistentně pracovat v Claude a aby byla připravená půda pro pozdější
Python skripty / reporty.

## Rozhodnutí (vstupní)

| Rozhodnutí | Hodnota |
|---|---|
| Zdroj pravdy | **Git repo `finApp`**. iCloud zůstává mobilní zápisník, ze kterého se obsah přelévá sem. |
| Spolupráce | Zatím **sólo (JB)**. Struktura ale nemá bránit pozdějšímu zapojení Daniela přes git. |
| Jazyk poznámek | **Česky** (obsah je česky). Technické artefakty/kód později anglicky. |
| Aktuální výstup | Jen **struktura + paměť** (řídicí vrstva pro práci v Claude). |
| Priorita | **Vyřešit vstupní data** (`02-vstupni-data.md` + `data/samples/`). |
| Dlouhodobě | Python skripty / generované reporty (fáze 3). |

## Cíl této struktury (success criteria)

1. Existuje jednoznačný kanonický zdroj projektových poznámek v repu.
2. Pavlova trojice `CLAUDE.md` / `memory.md` / `roadmap.md` odděluje *aktuální stav* od *historie* a *trvalých faktů*.
3. „Vstupní data" přestávají být mlhavá — pro každý zdroj (XTB, Degiro, J&T) je černé na bílém,
   jaká pole potřebujeme, v jakém formátu chodí, jaké jsou problémy a kde leží vzorek.
4. Nic se nemaže — původní `.pages`/PDF zůstávají jako archiv, decision log je append-only.

## Vybraný přístup

**A) Plná Pavlova trojice + číslované poznámky v repu.**

Zamítnuté alternativy:
- **B) Odlehčená** (bez `memory.md`/`roadmap.md`) — projekt už má historii i fáze, oddělení stavu/archivu se vyplatí.
- **C) Doslovný klon vč. `*-template.md`** — šablony dávají smysl při desítkách klientských projektů, ne pro sólo. YAGNI.

### Jemnost: memory.md vs. decision log (žádná duplicita)
- `docs/06-decision-log.md` = **chronologický append-only** log rozhodnutí („ruší YYYY-MM-DD").
- `memory.md` = **trvalá fakta a kontext** projektu (co projekt je, klíčová platná pravidla, archiv slepých uliček).
- Pravidlo: událost/změna → decision log; trvale platné pravidlo nebo fakt → memory.

## Cílová struktura adresáře

```
finApp/
├── CLAUDE.md                  # jak má Claude s projektem pracovat + AKTUÁLNÍ stav (jen současnost)
├── memory.md                  # trvalá fakta, klíčová pravidla, Archiv (slepé uličky) — "nemaž nic"
├── roadmap.md                 # fáze: v1 (XTB+Degiro, TWR) → v2 (měny, dividendy) → v3 (klienti, white-label)
├── docs/
│   ├── 00-vision.md           # vize & cíl (píše se jednou, skoro nemění)
│   ├── 01-scope.md            # co je/není ve v1; levely 1/2/3; uživatelské role (ze Z1 notes)
│   ├── 02-vstupni-data.md     # PRIORITA: pro každý zdroj heading + pole + formát + problémy + odkaz na vzorek
│   ├── 03-metriky.md          # TWR (P1), P&L, dividendy (otevřené) — vzorce
│   ├── 04-wireframy.md        # náčrty + odkazy na obrázky v assets/
│   ├── 05-vystup.md           # jak má vypadat výstup/report
│   ├── 06-decision-log.md     # chronologický, append-only, "ruší YYYY-MM-DD"
│   └── 10-meeting-notes.md    # sync log s Danielem
├── data/
│   ├── README.md              # popis: jaká data, odkud, jak tečou dovnitř, schéma
│   └── samples/
│       ├── xtb/
│       ├── degiro/
│       └── jt/                # syrové vzorky výpisů (PDF/CSV)
└── App/                       # PŮVODNÍ .pages + PDF — archiv, nemažeme nic
```

## Mapování stávajícího obsahu → repo

| Existující (iCloud / App/) | Cíl v repu |
|---|---|
| 00 — Vision a cíl | `docs/00-vision.md` |
| (Z1 quick notes — scope, levely, role) | `docs/01-scope.md` |
| 02 — Vstupní data | `docs/02-vstupni-data.md` |
| (zmínka „poznámka 03" — TWR vzorce) | `docs/03-metriky.md` (kostra + `[ZKONTROLOVAT]`) |
| 04 — Wireframy a náčrty | `docs/04-wireframy.md` + obrázky |
| typ jak by mohl vypadat výstup (screenshoty) | `docs/05-vystup.md` |
| 06 — Decision log | `docs/06-decision-log.md` |
| 10 — Meeting notes / sync log | `docs/10-meeting-notes.md` |
| `App/*.pages`, `App/*.pdf` | ponecháno v `App/` jako archiv |

## Zachované principy Pavla Ungra

- **CLAUDE.md = jen aktuální stav.** Historie putuje do `roadmap.md` / decision logu.
- **Nemaž nic.** `App/` zůstává; decision log je append-only; nejisté označit `[ZKONTROLOVAT]`.
- **Číslování poznámek** = stejná konvence jako v iCloudu (00, 01, 02, 03, 04, 05, 06, 10).

## Otevřené otázky (mimo scope této struktury, k řešení později)

- `[ZKONTROLOVAT]` Jak řešit dividendy (z meeting notes 2026-06-02).
- `[ZKONTROLOVAT]` Přesné vzorce TWR (poznámka 03 zatím neexistovala).
- Měny — odloženo do v2.
- Volba formátu vstupních dat (PDF parsing vs. CSV vs. ruční) — `data/02` to zmapuje, rozhodnutí padne pak.

## Mimo scope

- Samotná aplikace / UI / backend.
- Python skripty na analýzu (fáze 3, navazuje na `python/analyze_portfolio.py`).
- Uživatelské role, white-label, pricing (v2/v3).
