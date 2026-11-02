# Scorer World 0.9.5 — club colours without name imports

Home colours are now built into the app for all 352 real club identities in the
current two-division name pack: Portugal, England, Spain, Germany, Italy, France,
Brazil and Argentina, including each ten-club reserve. Names remain fictitious
until the optional name pack is imported. Palettes follow the stable club UID,
independent of editor aliases, canonical renames, country, tier and roster order.
This also corrects slots whose previous kit belonged to an obsolete reference
club rather than the new division-correct real-name mapping.

The four colours describe shirt, shorts, socks and the secondary shirt colour.
These are simplified representative home colours, not replicas of every annual
pattern, sponsor, licensed crest or alternate kit. Existing match clash handling
still exchanges the opponent's main/secondary shirt colours; it does not claim
to reproduce a verified away kit. Goalkeepers retain contrasting game palettes.
Other countries retain their existing palettes; this release does not claim a
verified real kit for all 10,598 catalogue slots.

Training now resolves the current club's kit even after a national-team match,
without inheriting stale match participants. Club badges that use kit colours
share the corrected palette. No name import or network connection is necessary.

Factual source URLs, Wikipedia revision IDs, extracted home fields and explicit
traditional-colour overrides are recorded in `docs/data/club_kits.provenance.json`.
`python3 tools/build_club_kits.py` reproduces the bundled offline JSON. Wikimedia
image requests returned HTTP429 and were stopped; missing images were not treated
as evidence. No third-party images are bundled.

Version: QA 0.9.5, code 1026905; public 1.0 remains unchanged. Two active divisions,
FIFO reserves, free agency, physical goal balance, saves, editor and nine UI
languages are preserved. National competition capacities and official promotion
rules researched separately are not introduced by this colour update.

Validation is recorded in `docs/BUILD_LOG.md` and the artifact metadata. Native
Android packaging/source checks do not replace a physical-phone test or Play review.
