# Scorer World 0.9.24 — complete club colour coverage

Vitória BA was one of26 identities added by the current names pack whose colours
had not been added to the older352-club catalogue. Those UIDs fell through to a
generic name-hashed kit, explaining the white/blue appearance. All378 current
real-name identities now have explicit home palettes, even without importing
names. No career reset or names reimport is required after updating the APK.

Vitória has a red shirt and black secondary colour; the referenced home kit has
white shorts/socks. Colours remain representative in the existing simplified mesh,
without exact seasonal patterns, sponsors or logos. Added all26 missing entries:
Spain6, Italy4, Brazil16. Also restored the secondary colour in8 older monochrome
palettes: Casa Pia, Académico de Viseu, Amarante, Heidenheim, Le Mans, Athletic,
Figueirense and Barra. Fresh source/revision checks cover these34 changed rows;
other344 retain their earlier reviewed values. Full UID/name/colour completeness
and identity consistency were checked across378 clubs.

The offline colour builder now rejects missing or mismatched entries against the
current names pack. Palettes remain attached to stable UIDs, surviving edited or
fictional names, reserve rotation, transfers and existing-career reloads.

Validation:18 core/name-pack/edition tests and10 real Kivy kit/finishing tests
passed. Native coverage includes Vitória home/away scenes and training after an
international match, loading an existing save, and no names reimport. All378
names/provenance/colour keys match. A real native training preview was inspected.
No rendering geometry, text layout, save schema or gameplay change; the previous
layout matrix was not rerun for this palette-only change.

World DEBUG QA upgrade with the existing package/certificate. Public1.0 unchanged;
physical Android installation/playtesting remains pending.

Actual APK checks passed for exact modules/data/font/image bytes, all378 built-in
colour palettes including Vitória, competition/progression/save/safety smoke
checks, existing DEBUG upgrade certificate, API36/arm64 and118 ELF/ZIP16KB
alignment. The first verification hit a temporary container disk-space error;
removed only generated scratch archives from completed0.9.22/0.9.23 tasks and
reran all candidate checks successfully. Versioned source, evidence and local
deliverable APKs were retained.
