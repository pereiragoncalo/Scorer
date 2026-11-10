# Scorer1.0/code1030003 — city and colour

Owner explicitly chose city/colour aliases based on real club identity, not
invented clubs or nickname aliases. New names use real cities/established districts
and colour labels: Benfica→Lisboa Vermelho, SportingCP→Lisboa Verde, Porto→Porto Azul,
Flamengo→Rio de Janeiro Vermelho-Preto, VitóriaBA→Salvador Vermelho-Preto.
Reserve teams keep B; same-city collisions use secondary colours/football prefixes.

Current eight-country378club identities are authoritative. club_city_reference.json
binds geography to those exact UIDs/names/source revisions. Home palettes are
checked byte-for-byte against existing factual club_kits.provenance.json and the
current names pack. No kit RGB, pattern, venue geometry or gameplay formula changed.
This avoids133obsolete identity correspondences in the original city/reference
overlay. Example: current FamalicãoUID had an oldGDChavesreference. Dark navy is
classified as blue, not black (Millwall); identical club names across countries
remain separate (ArsenalLondon vs ArsenalSarandí).

Coverage is intentionally explicit:
-378current supported real-club identities have documented city/home-kit matches
 (Portugal, England, Spain, Germany, Italy, France, Brazil, Argentina; game first/
 second divisions and selected reserves).
-40extra archival rows have existing sourced representative palettes.
-10318other registry rows use geographic names and existing game palettes, with
 NO claim of complete real-club/home-kit verification. They are NOT silently marked
 factual. Expanding that coverage needs further source work.

All10736registryUIDs remain covered. Canonical keys, saves, custom editor aliases
and all existing kit assets/palettes survive. Public shipping datasets contain city/
colour aliases, not official real-club name packs/history. YOUR SEASON centring and
new-career caption fixes remain. Version name1.0, new versionCode1030003.

Validation:
-33focused release/catalogue/current-identity/city-colour/kit checks pass.
-6previous native creation/centred-season tests pass; new native test checks four
 actual club labels and their matching palettes, passing after acknowledging the
 weekly coach meeting in the fixture setup (first run was redirected to coach).
-Source-only audit uses revision-pinned sources already cached in this workspace;
 no new network colour facts fabricated. Registry builder deterministic.
-Unsigned Android AAB genuinely built; final inspection/download/owner signing
 status recorded in build log. Owner key never received; Play acceptance separate.
