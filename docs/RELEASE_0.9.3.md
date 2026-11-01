# Scorer World 0.9.3 QA

- No Privacy button on start, regular or compact hub. Help → Settings retains career transfer and public-record settings.
- No Global button on Top Scorers. The hub Leaderboard remains the direct entry.
- Leaderboard reads the public scoped records table without enabling sharing or opening adult/legal screens. Explanatory usage text removed from the table screen. Sharing a record retains the separate adult/share confirmation. Report/block remains available to public viewers; removal still works with sharing locked. Empty data is not replaced with invented records.
- Uncompressed names JSON is a GitHub Release attachment with Content-Disposition attachment,113122bytes; download hash matches the editor pack. Europe/Brazil/Argentina July2026 snapshot.

Validation:232 unique core tests and116 unique native Kivy tests passed. The initial core run exposed an existing nondeterministic domestic-rollover fixture: completing unplayed matches could overturn its narrow artificial point gaps. The fixture now uses an insurmountable intended rank; all8 domestic tests passed. The initial UI run expected11 main buttons; after the requested removal this is10, and the six viewport checks passed after updating that assertion. Two additional access tests prove real asynchronous fetch-to-table rendering with sharing locked and a GET-only request, no legal screen, retained report access, removed main/Global buttons and Help/Settings transfer routing.

Actual APK: exact compiled source, agreement/Portuguese labels and usage gate, competition/save-reload, package/code/debug certificate,118 ELF/16KB and zip alignment verified. Live GET for World/England/Division4 returned HTTP200/schema3/zero published records using the app headers. No uploads or invented leaderboard data were sent. No handset/Play validation or server deployment claimed. Package com.clemir.scorerworld, versionCode1026903; existing World careers/names preserved. Public launch remains1.0.
