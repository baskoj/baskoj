# finApp — projektová struktura: Implementační plán

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Vytvořit v repu `finApp` projektovou strukturu à la Pavel Ungr (trojice CLAUDE.md/memory.md/roadmap.md + číslované docs/ + data/), naplněnou obsahem z existujících PDF/poznámek.

**Architecture:** Markdown-only scaffolding. Repo = zdroj pravdy. Existující `App/*.pages`/PDF zůstávají jako archiv (nemažeme nic). Obsah se přelévá z PDF do `.md` 1:1, nejisté věci se značí `[ZKONTROLOVAT]`.

**Tech Stack:** Markdown, git. Žádný runtime, žádné testy v klasickém smyslu — ověření = porovnání s odpovídajícím zdrojovým PDF.

## Global Constraints

- Jazyk obsahu: **česky** (technické artefakty později anglicky).
- **Nemaž nic:** `App/` zůstává; decision log append-only; nejisté → `[ZKONTROLOVAT]`.
- `CLAUDE.md` obsahuje **jen aktuální stav**; historie patří do `roadmap.md`/`06-decision-log.md`.
- Žádná duplicita: událost/změna → decision log; trvalé pravidlo/fakt → `memory.md`.
- Commit jen na pokyn uživatele (větev z `master`). Plán commity připravuje, ale spouští je až JB.
- Číslování poznámek: 00, 01, 02, 03, 04, 05, 06, 10 (stejné jako iCloud).

---

### Task 1: Pavlova řídicí trojice (CLAUDE.md / memory.md / roadmap.md)

**Files:**
- Create: `finApp/CLAUDE.md`
- Create: `finApp/memory.md`
- Create: `finApp/roadmap.md`

**Interfaces:**
- Produces: tři kořenové řídicí soubory, na které odkazují všechny docs/.

- [ ] **Step 1: `CLAUDE.md`** — jak má Claude s projektem pracovat + AKTUÁLNÍ stav. Sekce:
  - `## Co je finApp` (1 odstavec z 00-vision)
  - `## Aktuální stav` (kde projekt je: sólo, fáze v1, priorita = vstupní data)
  - `## Jak pracovat s tímto repem` (zdroj pravdy = repo; nemaž nic; značka `[ZKONTROLOVAT]`; odkaz na docs/ a memory.md/roadmap.md)
  - `## Struktura` (stručná mapa složek)
- [ ] **Step 2: `memory.md`** — trvalá fakta a kontext. Sekce:
  - `## Trvalá fakta` (kdo: JB+Daniel; co produkt dělá; instrumenty; brokeři v1: XTB+Degiro)
  - `## Platná pravidla` (TWR = P1 metrika; měny → v2; klient needituje data)
  - `## Archiv` (slepé uličky — zatím prázdné, s vysvětlením k čemu sekce slouží)
- [ ] **Step 3: `roadmap.md`** — fáze. Obsah:
  - `## v1` — XTB + Degiro, TWR, top-down statický výstup
  - `## v2` — měny, dividendy, další instrumenty
  - `## v3` — víc klientů/účtů, uživatelské role, white-label, pricing
- [ ] **Step 4: Ověření** — otevřít všechny tři, zkontrolovat, že CLAUDE.md neobsahuje historii (jen stav) a že se memory/decision-log neprolínají.
- [ ] **Step 5: Commit (na pokyn JB)**
```bash
git add finApp/CLAUDE.md finApp/memory.md finApp/roadmap.md
git commit -m "Add finApp control trinity (CLAUDE.md, memory.md, roadmap.md)"
```

---

### Task 2: Vize a scope (docs/00, docs/01)

**Files:**
- Create: `finApp/docs/00-vision.md`
- Create: `finApp/docs/01-scope.md`

**Interfaces:**
- Consumes: `App/00 — Vision a cíl.pdf`, `App/Z1— JB - quick notes - pomoci Wispr Flow.pdf`.
- Produces: kanonická vize + scope, na které odkazuje CLAUDE.md.

- [ ] **Step 1: `00-vision.md`** — přepsat obsah z `App/00 — Vision a cíl.pdf` 1:1 (vize, cílovka, instrumenty, dva způsoby aktualizace, pricing tiers). Zachovat poznámku „píše se jednou, skoro nemění".
- [ ] **Step 2: `01-scope.md`** — z `Z1 quick notes`: co je/není ve v1; levely 1/2/3; uživatelské role (klient1/klient2/klient3, proklik); white-label příprava; otázka interaktivity (JB: ve v1/v2 nedává smysl). Nejisté → `[ZKONTROLOVAT]`.
- [ ] **Step 3: Ověření** — porovnat oba soubory s odpovídajícími PDF, žádný bod nevynechán.
- [ ] **Step 4: Commit (na pokyn JB)**
```bash
git add finApp/docs/00-vision.md finApp/docs/01-scope.md
git commit -m "Add finApp vision and scope notes"
```

---

### Task 3: Vstupní data — PRIORITA (docs/02 + data/)

**Files:**
- Create: `finApp/docs/02-vstupni-data.md`
- Create: `finApp/data/README.md`
- Create: `finApp/data/samples/xtb/.gitkeep`
- Create: `finApp/data/samples/degiro/.gitkeep`
- Create: `finApp/data/samples/jt/.gitkeep`

**Interfaces:**
- Consumes: `App/02 — Vstupní data.pdf`, znalost J&T výpisu (skill jt-portfolio-report), `python/analyze_portfolio.py`.
- Produces: konkrétní specifikaci vstupních dat — odrazový můstek pro fázi 3 (Python).

- [ ] **Step 1: `02-vstupni-data.md`** — pro každý zdroj jeden heading se strukturou (formát z PDF 02):
  ```
  ## <Zdroj> (formát)
  - Frekvence:
  - Pole:
  - Formát:
  - Problémy:
  - Vzorek: data/samples/<zdroj>/
  ```
  Zdroje: **J&T výpis (PDF)** (frekvence měsíčně; pole datum, ISIN, počet, cena, fee; problém: nezahrnuje splity — z PDF 02), **XTB**, **Degiro**. Pole u XTB/Degiro zatím `[ZKONTROLOVAT]` (vzorky Daniel teprve sháněl).
  Nahoře sekce „Use-case otázky" z PDF 02: stav peněz na začátku; kdy/kam se přesouvalo; typy investic; kde vidím průběžné stavy.
- [ ] **Step 2: `data/README.md`** — popis: co sem patří (syrové vzorky výpisů), jak data tečou (stáhnu výpis → uložím do `samples/<broker>/` → zapíšu pole do `02-vstupni-data.md`), že syrová data se necommitují, pokud obsahují citlivé částky (přidat poznámku).
- [ ] **Step 3: `.gitkeep`** do tří sample složek (aby existovaly i prázdné).
- [ ] **Step 4: Ověření** — `02` pokrývá všechny tři brokery a všechny use-case otázky z PDF; složky `data/samples/{xtb,degiro,jt}/` existují.
- [ ] **Step 5: Commit (na pokyn JB)**
```bash
git add finApp/docs/02-vstupni-data.md finApp/data
git commit -m "Add finApp input-data spec and data/ scaffold"
```

---

### Task 4: Metriky, wireframy, výstup (docs/03, 04, 05)

**Files:**
- Create: `finApp/docs/03-metriky.md`
- Create: `finApp/docs/04-wireframy.md`
- Create: `finApp/docs/05-vystup.md`
- Create: `finApp/assets/` (přesun obrázků z App/, viz krok 3)

**Interfaces:**
- Consumes: `App/04 — Wireframy a náčrty.pdf`, `App/typ jak by mohl vypadat vystup.pdf`, `App/Screenshot 2026-06-21...png`, `App/vize - sync Honza a Dan posledni schuka.JPG`, meeting notes (TWR P1, dividendy otevřené).
- Produces: tři obsahové poznámky + assets/ s obrázky.

- [ ] **Step 1: `03-metriky.md`** — kostra metrik: `## TWR (P1)` s `[ZKONTROLOVAT]` na přesný vzorec (poznámka 03 dosud neexistovala); `## P&L`; `## Dividendy` označit `[ZKONTROLOVAT]` (otevřená otázka z meeting notes 2026-06-02).
- [ ] **Step 2: `05-vystup.md`** — popsat referenční výstup z `typ jak by mohl vypadat vystup.pdf` (app typu Portfolios/Delta: Total Worth graf, časové rozsahy, holdings). Zachytit JB rozhodnutí: výstup statický top-down, ne interaktivní ve v1; nástroj pro poradce na schůzku, drží ho poradce ne klient.
- [ ] **Step 3: Přesun obrázků** — zkopírovat (ne smazat originál) náhledy do `assets/`:
```bash
mkdir -p finApp/assets
cp "finApp/App/Screenshot 2026-06-21 at 19.29.04.png" finApp/assets/
cp "finApp/App/vize - sync Honza a Dan posledni schuka.JPG" finApp/assets/
```
- [ ] **Step 4: `04-wireframy.md`** — odkázat na obrázky v `assets/` + přepsat textový obsah z `App/04 — Wireframy a náčrty.pdf`.
- [ ] **Step 5: Ověření** — všechny tři docs existují, obrázky v assets/, originály v App/ netknuté.
- [ ] **Step 6: Commit (na pokyn JB)**
```bash
git add finApp/docs/03-metriky.md finApp/docs/04-wireframy.md finApp/docs/05-vystup.md finApp/assets
git commit -m "Add finApp metrics, wireframes, output notes + assets"
```

---

### Task 5: Decision log a meeting notes (docs/06, docs/10)

**Files:**
- Create: `finApp/docs/06-decision-log.md`
- Create: `finApp/docs/10-meeting-notes.md`

**Interfaces:**
- Consumes: `App/06 — Decision log.pdf`, `App/10 — Meeting notes : sync log.pdf`.
- Produces: chronologický append-only log + sync log.

- [ ] **Step 1: `06-decision-log.md`** — přepsat z PDF 06 chronologicky (2026-05-26, -27, -28, -30). Nahoře pravidlo: „nikdy nepřepisuj staré záznamy; změna → nový řádek s datem a `ruší YYYY-MM-DD`". Zachovat zápisy: start XTB+Degiro (v2 ostatní), TWR = P1, založení adresáře, atd.
- [ ] **Step 2: `10-meeting-notes.md`** — přepsat z PDF 10: sync 2026-06-02 (účastníci, co probrali, rozhodnutí → odkaz na 06, akční body, otevřené: dividendy) + kick-off 2026-05-26.
- [ ] **Step 3: Ověření** — decision log chronologický a kompletní; meeting notes odkazují na decision log; akční body zachovány.
- [ ] **Step 4: Commit (na pokyn JB)**
```bash
git add finApp/docs/06-decision-log.md finApp/docs/10-meeting-notes.md
git commit -m "Add finApp decision log and meeting notes"
```

---

## Self-Review

**Spec coverage:** Všech 8 docs poznámek (00,01,02,03,04,05,06,10) + trojice + data/ + archiv App/ → pokryto Tasky 1–5. Mapování obsahu ze spec tabulky → každý řádek má task.

**Placeholder scan:** `[ZKONTROLOVAT]` použito jen tam, kde jsou reálné otevřené otázky (TWR vzorec, dividendy, XTB/Degiro pole) — to je záměrná konvence „nemaž nic", ne nedodělek plánu.

**Type consistency:** N/A (markdown). Názvy souborů/cest konzistentní napříč tasky a se spec.
