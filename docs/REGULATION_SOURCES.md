# Competition regulations: source audit

Checked on 2026-10-24. This is research evidence, not a statement that the
corresponding rules have been implemented or that every country is verified.

## Network check

The inherited HTTPS proxy returned HTTP 200 for all four official entry points:

- https://www.efl.com/governance/regulations/
- https://www.ligaportugal.pt/pages/estatutos-regulamentos
- https://documents.uefa.com/
- https://inside.fifa.com/legal/documents

This supersedes the earlier proxy-403 observation. Runtime configuration status
still reports policy state `unknown`; actual requests establish current access to
these destinations, not unrestricted Internet access.

## Portugal, 2026/27: primary document downloaded and read

[Competition regulations, linked by Liga Portugal](https://www.ligaportugal.pt/backoffice/assets/20260701_RC_2026_27_f53785bcd4.pdf).

- PDF: 2,440,200 bytes.
- SHA-256: `6ff749baf9a3da7698983e097d25cb573f4c029ce65e7fca1e52c02be3e8a550`.
- Local research copy: `/workspace/striker-runtime/regulations/portugal-competition-2026-27.pdf`.
- Text extracted with `pdftotext -layout`; this PDF is not bundled in the game.

Verified provisions:

- Articles 21 and 25: each professional division has 18 teams.
- Article 22: the top two eligible Liga 2 clubs go up directly; the bottom two
  Liga 1 clubs go down directly. An additional place is decided by playoff.
- Article 31: Liga 1's 16th faces the highest eligible Liga 2 side outside the
  direct promotion places, excluding B teams. Two legs, draw for venue order,
  aggregate goals, then 30 minutes of extra time and penalties if necessary.
  There is no away-goals tiebreaker in this provision.
- Article 26: two Liga 3 clubs go up directly; the bottom two Liga 2 clubs go
  down. A further promotion/relegation place is decided by the Liga 3 playoff.
- Article 31(5): that playoff pairs Liga 2's 16th with the Liga 3 participant
  indicated by the FPF; the FPF rules and inter-organiser agreement also apply.

Pending before claiming a complete Portuguese model: FPF Liga 3 and Campeonato
de Portugal formats, B-team eligibility across tiers, league tiebreakers,
licensing exceptions, cups, continental access and full season calendars.

## Other sources located, not yet audited

- EFL playoff rules: https://www.efl.com/documents/play-off-rules
- EFL constitution: https://www.efl.com/documents/constitution
- UEFA regulations portal and FIFA legal portal above require retrieval and
  review of individual competition/season documents. HTTP 200 on a portal alone
  does not verify a competition format.

The existing generic World division model must not be described as an exact
reproduction of these regulations. Each future rules profile needs a season,
primary source, article references, eligibility/tiebreaker rules and tests for
the resulting progression before it is marked verified.
