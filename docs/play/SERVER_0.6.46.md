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

The reviewed backend revision is `5108550eebd6264de7da9c4bba8e7900373e0b2d`.
The commands below CREATE a new directory on the laptop. They do not assume that
it already exists and do not overwrite your existing project/deploy directory.
Run these first as **clemir** (if currently root, return to your clemir SSH shell):

```sh
git clone --depth 1 --single-branch --branch main https://github.com/pereiragoncalo/Scorer.git /home/clemir/scorer-publicacao-0646
git -C /home/clemir/scorer-publicacao-0646 fetch --depth 1 origin 5108550eebd6264de7da9c4bba8e7900373e0b2d
git -C /home/clemir/scorer-publicacao-0646 checkout --detach 5108550eebd6264de7da9c4bba8e7900373e0b2d
cp -n /home/clemir/scorer-publicacao-0646/server/public.example.json /home/clemir/scorer-publicacao-0646-public.json
su -
```

After entering the root password, run as **root** (no sudo required):

```sh
bash /home/clemir/scorer-publicacao-0646/server/install_online.sh
systemctl status scorer-online --no-pager
systemctl status scorer-maintenance.timer --no-pager
curl --fail http://127.0.0.1:8787/health
curl --fail 'https://stats.clemir.com/v3/records?edition=free&country=Scorer&division=1'
```

If the new directory already exists, do not delete it blindly: use a different
fresh directory consistently or inspect the existing checkout first. Server
upgrade is required for the new app's public records; usage protocol is unchanged.
Do not run a second tunnel or rotate the existing administrator token.
The original private admin environment remains root-only; public policy facts
are installed separately in /opt/scorer/public.json so the scorer service can
read them without gaining access to private credentials.

## Public pages

The example includes the owner-approved name/email. Complete effective date,
reviewed legal basis, actual provider/children practices and transfer safeguards
in /home/clemir/scorer-publicacao-0646-public.json (the copy created above). These are public facts, never
passwords or tokens. Once finalized, from the reviewed checkout as root:

```sh
cd /home/clemir/scorer-publicacao-0646
python3 -m server.configure_public /home/clemir/scorer-publicacao-0646-public.json
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
