# Public policy independent of bastion

The owner cannot access bastion from the current location. Final privacy, community
and removal HTML were prepared on the public `gh-pages` branch with only public
content. No game credentials, databases, counters or records are in this site.

Canonical URLs for the updated candidate and Play Console:

- https://pereiragoncalo.github.io/Scorer/privacy/
- https://pereiragoncalo.github.io/Scorer/terms/
- https://pereiragoncalo.github.io/Scorer/delete/

The policy discloses GitHub Pages request/IP processing separately from gameplay
traffic to stats.clemir.com/Cloudflare. Static pages contain no analytics scripts,
advertising, form submission or embedded third-party images.

The integration's initial Pages-enablement call returned403. Subsequent API reads
confirmed Pages was enabled with gh-pages/root and HTTPS enforcement. Initial
legacy dynamic deployment failed with no jobs/logs, then its retry failed too.
A minimal custom workflow was added on gh-pages, with contents:read, pages:write
and id-token:write, staging only the5public files. It uses the existing Pages
site and the existing environment's gh-pages-only branch rule. It does not remove
protection rules, approve a gated deployment or request additional credentials.

Do not claim the site live until anonymous HTTPS and browser checks succeed.
Deployment evidence and final URLs will be recorded after those checks. The
server and its old policy are unchanged without bastion access. Updating static
legal pages does not update the v4 leaderboard service or run human moderation.
The0.9.41 candidate changes the policy destination only;0.9.40 optional-usage and
safety behavior is retained. Existing0.9.40 still opens the old server URL.

## Confirmed deployment

Custom Pages workflow42673061046 succeeded at18:20UTC on9November2026. Pages
reports built. Anonymous HTTPS on all3canonical URLs returned200 with English
HTML, public identity, no draft banner and the published marker. Source hashes
and response evidence are in docs/data/policy_0.9.41/live.json.

The direct Chromium check encountered the managed proxy's untrusted CA, while
stdlib HTTPS verification succeeded with the supplied trust bundle. Browser layout
and navigation are checked against the exact live HTML fetched over verified HTTPS
and served locally; this is explicitly not a direct Chromium HTTPS certificate
validation. No certificate checks were disabled.

The old stats.clemir.com policy remains unchanged. Use the canonical Pages privacy
URL in Console and the0.9.41 APK. There is no need for bastion access to publish or
read these public legal documents. Backend v4 deployment and ongoing moderation
remain separate operational requirements. No publication review flags were faked.
