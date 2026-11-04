# Scorer World 0.9.7 — domestic schedules and split tables

New World careers now use the sourced regular league capacities and executable
round/split structures in38 countries (76 divisions). For example Spain has20/22
clubs, Italy20/20 and Brazil20/20. Three- and four-round leagues play their actual
number of meetings instead of always using a double round robin.

Supported countries: Austria, Azerbaijan, Bahrain, Brazil, Chile, China, Croatia,
Cyprus, Denmark, England, Estonia, Finland, France, Germany, Hungary, Iraq, Italy,
Japan, Kenya, Netherlands, Northern Ireland, Norway, Poland, Portugal, Republic
of Ireland, Saudi Arabia, Scotland, Slovakia, Slovenia, South Africa, Spain,
Sweden, Switzerland, Tanzania, Thailand, Turkey and Vietnam.

## Phases that now run in the game

- Championship/survival groups freeze from the completed first-phase standings.
  Groups play only their own opponents and remain separately ranked afterwards.
- Austria halves points once. Saving/loading cannot halve them a second time.
  Denmark, Scotland, Switzerland, Northern Ireland and Slovakia carry points.
- Finland’s top group plays32 league games and the lower group27. Cyprus’s first
  division has36/33 games. A player in the shorter group proceeds to the remaining
  cup/international/playoff calendar without receiving phantom league fixtures.
- Finland’s second division has27 league games; the upper half gets five home
  games in the final nine-game round and the lower half four.
- Undrawn phase dates remain visible with unknown opponents; previewing the
  calendar cannot draw groups from an unfinished table. Tables use A/B markers.
- Sweden’s new access route plays the second-tier3v4 eliminator before the
  cross-tier tie against the first division’s14th. South Africa uses a played
  three-club home/away promotion competition, not a two-team elimination tie.
- China/Vietnam use two direct exchanges in these new careers. Existing played
  access brackets, national selection and physical shooting remain in place.

## Upgrade and saved careers

Save and Exit, then install over the previous Scorer World QA app. Package and
existing DEBUG upgrade certificate are unchanged. **Load Game keeps the existing
career’s saved league model, fixtures, clubs, aliases, scores and history.**
Start **New Game** to use the new capacities/splits; the normal confirmation and
private backup apply when replacing an existing career. No automatic career reset.

All previous canonical club identities remain known, including clubs archived
when a new starting league is smaller. Imported names/colours remain attached to
UIDs. Clubs added to expand a league use fictional defaults; an older names JSON
remains importable but does not contain aliases for these extra identities.

## Scope and verification

The owner paused further country research to update the APK. This release
integrates regular capacities and the supported splits; it does not certify full
national regulations or implement every researched competition. Access,
licensing, exact tie-breakers, seasonal transitions and complex group/period
formats still have recorded limits. Countries outside the38 retain the previous
career model. Argentina’s two-zone/averaging model remains outside this regular-
schedule integration. Dated source structures are game baselines, not automatic
updates to all future seasons or replicas of every real fixture date.

Actual APK/source/data, compiled career behaviour, upgrade signature, package,
API36/26 and16KB native alignment checks are recorded in the artifact metadata.
No physical-phone test, production signing, Play upload or live-server update is
claimed. World remains free, ad-free and includes the local names editor and nine
UI languages. Public launch version remains1.0; this is QA0.9.7/code1026907.
