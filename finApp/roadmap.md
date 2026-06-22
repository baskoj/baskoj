# finApp — roadmapa

> Náčrt vize (sync Honza + Dan, viz `docs/07-architektura.md`) rozlišuje 4 kroky rolloutu:
> STEP 1 = Já + Dan · STEP 2 = Dan + klient · STEP 3 = společnosti (white-label) · STEP 4 = „unknown clients" (pasivní náhled na měsíční bázi).
> Fáze v1/v2/v3 níže na ně navazují: v1 ≈ STEP 1, v3 ≈ STEP 3, STEP 4 = nejzazší cíl.

## v1 (teď)

- Brokeři: XTB + Degiro
- Klíčová metrika: TWR
- Výstup: statický top-down přehled (ne interaktivní dashboard)
- Účel: nástroj pro poradce na schůzku s klientem

## v2

- Podpora měn (víceměnová portfolia)
- Dividendy
- Další instrumenty a brokeři

## v3

- Podpora více klientů a účtů
- Uživatelské role: proklik mezi klienty po přihlášení
- White-label: změna loga a barev podle poradenské firmy (APP1, APP2 = instance pro různé firmy)
- Pricing: retail fee ~100 Kč/měs, úrovně základní / pokročilé / profi
- Cílová forma: nativní aplikace Android / iOS (viz `docs/07-architektura.md`)

## STEP 4 (nejzazší cíl)

- „Unknown clients" — koncoví klienti mimo přímý okruh.
- Pouze **pasivní náhled** do dat na **měsíční bázi** (klient needituje data).
