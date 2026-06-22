# 07 — Architektura

Zdroj: ruční náčrt ze syncu Honza + Dan (`../assets/vize - sync Honza a Dan posledni schuka.JPG`).

## Datová pipeline (hlavní tok)

```
DATA VSTUPNÍ (PDF, J&T, WEB, „cokoli")
        │  → ROBOT / scraper (automatický sběr z veřejných dat)
        ▼
TRANSFORMACE / WEB ROZHRANÍ        ← mezivrstva (výpočty: stav portfolia v čase, TWR)
        ▼
APPKA (Android / iOS)              → APP1, APP2 (white-label instance)
```

## Vrstvy

- **Vstup** — výpisy a data z více zdrojů: PDF (J&T), web, „cokoli". Dva způsoby aktualizace: manuální přepis + automatický sběr robotem/scraperem.
- **Transformace / web rozhraní** — mezivrstva, která syrová data převede na shrnutí portfolia a spočítá metriky (TWR, P&L). Tady navazuje fáze 3 (Python, `python/analyze_portfolio.py`).
- **Appka** — cílová forma: nativní aplikace pro **Android a iOS**. White-label instance (APP1, APP2) pro různé poradenské firmy (logo/barvy podle firmy).

## Mapování na rollout (viz roadmap)

Náčrt rozlišuje 4 kroky:
- STEP 1 — Já + Dan (naše peníze)
- STEP 2 — Dan + klient
- STEP 3 — společnosti (white-label)
- STEP 4 — „unknown clients": pouze **pasivní náhled** do dat na **měsíční bázi** (klient needituje)

## Otevřené

- `[ZKONTROLOVAT]` Vztah „statický report (v1)" vs. „nativní Android/iOS app" — viz `05-vystup.md`. Pravděpodobně v1 = statický report jako důkaz konceptu, nativní app je cílová forma. Nerozhodnuto.
- `[ZKONTROLOVAT]` Náčrt nahoře: `VSTUP A = JB / ÚSPĚCH B = MS` — pravděpodobně rozdělení odpovědnosti, ale není potvrzeno.
- `[ZKONTROLOVAT]` Konkrétní technologie scraperu / web rozhraní / app frameworku.
