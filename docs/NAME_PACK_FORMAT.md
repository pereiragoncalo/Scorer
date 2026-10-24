# World editor — name file format

Inside the game: **World > World leagues > a division > Edit names > JSON FORMAT**.
The example uses the selected club's actual IDs. Export Template writes that
league's clubs, league title and twelve fictional player-name roles per club.

1. Export Template using Android's document picker.
2. Open the file in a text/JSON editor. Change names on the **right** only.
3. Save as UTF-8 `.json`, then Import JSON in SCORER.
4. Review the preview and Apply Names. Cancel leaves the career unchanged.

Example structure (export your own template to get the correct IDs):

```json
{
  "version": 1,
  "leagues": {"Portugal|4": "My Portuguese League"},
  "clubs": {"c0417942003268da0c3f": "Lisboa Example"},
  "players": {"c0417942003268da0c3f:0": "Joao Example"}
}
```

Keep `version` as the number 1. Club IDs are stable opaque identifiers, not display
names. League keys are `Country|tier`. Player keys are `club_id:role`, with roles
0 through 11. These are fictional squad display-name roles, not shirt numbers or
the human player profile. Rename your own career player through PLAYER instead.

Names must contain 2–56 printable characters. No links, markup, control characters,
comments or trailing commas. Maximum 256 KiB and 4096 entries per import. Omitted
sections/entries remain unchanged, so a partial pack is valid. Unknown IDs and
invalid values reject the whole import; there is no partial application.

The editor changes display names only: team UIDs, goal totals, fixtures, ratings
and reference colours remain unchanged. Custom aliases override the World defaults
and survive promotion/save/reload. Free has no names editor and its career/file is
separate. Files are local; SCORER does not download official names or upload your pack.
