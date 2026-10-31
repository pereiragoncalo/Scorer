# Laptop update — Scorer0.6.46 safety backend

The operator account is active/verified; this does not install server changes.
No SSH connector or laptop filesystem is available here. The existing tunnel,
admin token, clemir-social and local career files must stay unchanged.

## What changes

- /v3/records: terms_version1, pending moderation, opaque public IDs.
- /v3/reports, local client blocking; /v1/moderation authenticated with existing
  administrator bearer. UI in /admin now loads reviews/reports and actions.
- Older v1/v2 upload routes return426 rather than bypass terms/review. v2 reads
  return only approved/current-terms records; withdrawals stay compatible.
- Existing records become pending until a new explicit current-terms submission.
  No automatic publication, no conversion of partial seasons.
- /privacy, /terms, /delete public pages prepared. Missing factual/legal public
  config returns503 rather than publishing placeholders as a final policy.
- Hourly collector cleanup even without new posts, daily systemd maintenance;
  aggregate-only backups7days. Installer retires the old raw backup file; active
  database is not erased. Names are deliberately not included in new backups.

## Install from reviewed source

Use a fresh clean checkout of the final revision, not an older deploy directory.
As clemir, fetch origin/main and prepare a clean worktree at the reviewed commit.
Then in normal SSH use `su -` (this Debian machine has no sudo):

```sh
bash /home/clemir/REVIEWED-CHECKOUT/server/install_online.sh
systemctl status scorer-online --no-pager
systemctl status scorer-maintenance.timer --no-pager
curl --fail http://127.0.0.1:8787/health
curl --fail 'https://stats.clemir.com/v3/records?edition=free&country=Scorer&division=1'
```

REVIEWED-CHECKOUT is intentionally a placeholder, not a claim that a directory was
created on the laptop. The final release report gives the source commit. Server
upgrade is required for the new app's public records; usage protocol is unchanged.
Do not run a second tunnel or rotate the existing administrator token.

## Public pages

The example includes the owner-approved name/email. Complete effective date,
reviewed legal basis, actual provider/children practices and transfer safeguards
in a separate copy of server/public.example.json. These are public facts, never
passwords or tokens. Once finalized, from the reviewed checkout as root:

```sh
python3 -m server.configure_public /path/to/completed-public.json
curl --fail https://stats.clemir.com/privacy
curl --fail https://stats.clemir.com/terms
curl --fail https://stats.clemir.com/delete
```

Do not mark a policy live until it actually returns its final content publicly.
Review Cloudflare logs/retention/processor terms in the owner's account.

## Moderation and operational acceptance

Open /admin, load moderation with the existing administrator token. The token
stays private; do not paste it into chat, screenshots or Play app-access forms.
New records are hidden until approved. Review player/team for contacts, names,
school info, abuse, impersonation and spam. Reject unsafe content; ban persistent
abusers, resolve reports and answer goncalo@clemir.com. All actions use explicit
confirmation; no automated approval service is implied.

Test an agreed record end-to-end: upload pending, approve, display exact division,
report/block, withdraw, check it disappears. The cloud tests use localhost only;
none of these new operations has been claimed deployed against the laptop.
Keep laptop awake/online, validate reboot/tunnel recovery, schedule updates and
check maintenance. Managed backups restore totals only; users may have to Share
again after a full restore. Keep canonical public IDs stable and never restore
an old raw database containing withdrawn personal records without reconciliation.
