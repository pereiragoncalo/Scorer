# World 1.0 replacement: fictional club identities (1030001)

The first production AAB (1030000) incorrectly shipped a reference presentation
catalogue with real/local club labels and real club profiles. Checking that the
catalogue matched the source did not establish fictional identities. The owner
reported this after the first internal Play release. That candidate is superseded;
owner should pause the internal track and replace it, not promote it to production.
This workspace has no Play Console control; track suspension is not asserted.

All Play staging, rehearsal and production now transforms the bundled club data:
- 10598 stable catalogue UIDs use their canonical fictional names.
- Existing custom editor aliases remain explicit, local user choices.
- Profile rows retain only fictional club labels, venue capacity and shirt pattern.
  Real founding dates, stadium/supporter names, historical titles and reference
  URLs are excluded. Obsolete reference-only profile UIDs are dropped.
- Rating rows keep numerical game strength and season statistics with fictional
  club names, stripping historical season name labels; stale reference-only UIDs
  are excluded. No change to the simulation formula or physical shot solver.
- UID-bound home palettes, plain/striped patterns and stadium geometry survive.
- New-career favourite selection uses the actual display name, respecting aliases.

Release verification compares all three identity datasets with the sanitized
expected data and rejects the ACTUAL previous AAB. Reference datasets under source
control are inputs for build tooling; they are not the shipping catalogue.

The same replacement widens the creation form and measures full country, favourite
and action captions. Portrait layouts stack the country/favourite controls when
space allows; landscape remains horizontal. Country captions separate heading and
value. Minimum 48dp touch targets remain. No hub rearrangement or gameplay change.

Validation:
- 25 focused release/catalogue/kit tests passed.
- 5 real Kivy creation tests passed on the clean indexed source: existing country
  selection/commit/save and new full-caption measurements at 5 density/size pairs
  in English, Portuguese and German (90 individual button measurements).
- Real rendered screenshot inspected at 1280x640, density1.6, English.
- Staged runtime: 8888 active clubs show canonical fictional names; initial aliases
  empty; save/load and explicit local editor alias survive.
- Actual rebuilt AAB inspection and owner signing/Play install recorded separately.

Version name stays 1.0; new version code is1030001. Upload key remains exclusively
on owner bastion. Never overwrite or regenerate that key. Existing 1030000 uploads
cannot be replaced in place; use a new internal release containing only1030001.
