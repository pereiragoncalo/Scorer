# Official competition rules research

Collection date: 2026-10-24. Research only; this batch makes no gameplay changes.

**2026-10-25 follow-up:** [priority status](PRIORITY_STATUS.md),
[55 European federation records](europe_federations.json), and
[75 additional retrieval attempts](priority_retrieval.json). Current priority is
Europe, Brazil, Argentina and Mexico; the coverage matrix records the owner's
simplified fallback for other countries. Implementation/validation of that
fallback is described [separately](../DOMESTIC_RULES_DEVELOPMENT.md).

- [Source catalogue](source_catalogue.json): 31 selected source records, each with
  edition, review status, URL and checksum where a full response was retained.
- [Reviewed provisions](REVIEW_NOTES.md): facts read from primary sources, with
  section references and remaining limitations.
- [Retrieval log](retrieval_log.json): 100 HTTP attempts, including failures,
  redirects, navigation shells and incomplete responses. Attempt count is not a
  document or verified-competition count.
- [Country coverage](country_coverage.json): all 212 regions currently listed by
  the game. No complete country model is marked verified in this batch.

Ten complete PDFs are retained outside the application at
`/workspace/striker-runtime/regulations/`, together with cached pages and extracted
text. Full third-party documents are not committed or bundled in the app. The
catalogue stores primary URLs and SHA-256 digests for repeatable verification.

## Reading the status fields

`reviewed_sections` verifies only the provisions explicitly described in the
review notes. It does not certify the complete competition or its implementation.
`reviewed_calendar_only` covers the official season guide's dates, not regulatory
articles, access lists or draw restrictions. Historical and amendment-pending
documents must not automatically become current-season rules.

`located_download_blocked` identifies a concrete document linked by its official
publisher whose file host returned a proxy 403. `navigation_only`, `portal_only`
and `javascript_shell_only` never count as regulation text, even with HTTP 200.
The RFEF competition PDF was not fully retained: its first response exceeded the
initial bounded download limit and a subsequent request returned 403.

## Network follow-up

The environment draft now includes the file hosts `assets.dfb.de`, `media.fff.fr`,
`assets.laliga.com`, `resources.premierleague.pulselive.com`,
`images.concacaf.com`, `assets1.afa.com.ar` and `files.figc.it`. Existing domain
entries and presets were preserved. Saving the draft does not apply it; the
configuration tool reports `requires_publish: true`. Review/save the environment
settings and Publish the environment to apply them. This is separate from game
or Play Store publication.

Remaining research includes the full EFL text, Portugal's FPF formats, current
Spanish competition bases, French/German/Italian document bodies, CONMEBOL and
AFC rules, FIFA competition and player eligibility rules, and the other domestic
countries. The source catalogue deliberately exposes these gaps.
