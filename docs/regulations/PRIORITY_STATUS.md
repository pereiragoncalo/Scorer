# Priority rules collection — 2026-10-25

The owner's scope is now Europe, Brazil, Argentina and Mexico for national
formats. All other countries use the separately implemented simplified two-tier,
three-up/three-down game model. That fallback is not a factual national model.

## Evidence gathered

- [European federation directory](europe_federations.json): all 55 UEFA association
  pages retrieved and checksummed. 53 link directly to an association website;
  Sweden/Russia did not yield a direct website link under the extraction criteria.
  This establishes publisher discovery, not a regulation review.
- [Priority retrieval log](priority_retrieval.json): 75 additional attempts,
  including 53 association website requests. Only four of those website requests
  produced retained pages (France, Germany, Italy, Spain); many individual PDF
  hosts remain blocked as documented in the existing source catalogue.
- Existing reviewed Portugal provisions and other European located documents
  remain in [the source catalogue](source_catalogue.json) and
  [review notes](REVIEW_NOTES.md).

| Priority | Current evidence | What is still missing |
| --- | --- | --- |
| Brazil | Official CBF root, competitions and regulation routes attempted; HTTP 503 on all | Current CBF regulation bodies and season-specific competition rules, including every requested tier |
| Argentina | AFA homepage retained; robots page available; its `/sitemap.xml` returned homepage HTML rather than XML | Current rule documents; guessed legacy document routes returned 404; AFA legacy/LPF destinations blocked by proxy |
| Mexico | FMF and Liga MX official destinations identified and attempted | Actual bodies; FMF/Liga MX/legacy FMF returned proxy 403; no current promotion/playoff rules certified |
| Europe | 55 UEFA association pages, 53 official publisher links; existing partial national document collection | Full current-season sporting regulations, groups/splits/playoffs, eligibility, tiebreakers, access lists and amendments for each country |

No Brazil, Argentina, Mexico or complete European country model is newly marked
verified by this follow-up. In particular, do not invent rules from memory or
assume that all South American competitions use a single round-robin format.

## Network configuration dependency

The environment draft preserves existing allowed destinations and now includes
the 53 publisher hosts linked by UEFA plus the explicitly targeted Mexican,
Argentinian, Brazilian file hosts and public search destinations. The supported
configuration tool returned `status: saved`, `requires_publish: true`.

That result saves a reviewable draft; it does not apply networking. The user must
review/save the environment settings and **Publish the environment**. No tool in
this session exposes that Publish operation. It is unrelated to publishing the
app or activating payments. Retry blocked destinations only after configuration
is applied; CBF's HTTP 503 may still require separate diagnosis at that point.

This follows the runtime skill's explicit instruction: “Configuration changes
require the environment configuration workflow and its user review.” Source:
[cloud-environment-runtime/SKILL.md](skill://plugin_connector_1p_c5b7d5df5d7081918f2c4be5a633ed5d/cloud-environment-runtime/SKILL.md).
