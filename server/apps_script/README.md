# Google Workspace / Apps Script option — prepared, NOT connected

No Google OAuth identity or Apps Script deployment tool is available in the
current chat. No project/trigger/deployment/email has been created in the owner's
account. A Gmail/Drive connection alone is not an Apps Script deployment API.
The existing APK0.6.39 has no endpoint and rejects Apps Script URLs/redirects;
DO NOT claim that installing this script connects that APK.

## One-time account setup (owner)

1. Open https://script.google.com/home/start with your Clemir Workspace account.
   Create a project named Scorer session notices. Paste Code.gs into its editor.
   In Project Settings enable showing appsscript.json; replace it with the
   supplied manifest. This requests only email sending and trigger management,
   not reading mail or player accounts.
2. In Project Settings > Script Properties set SCORER_RECIPIENT to your chosen
   recipient (already saved privately in this development workspace) and
   SCORER_ENABLED to true when ready to receive voluntary reports. Neither value
   is a player parameter; no passwords/API secrets are embedded in this script
   or the APK. Leave SCORER_ENABLED absent/false to keep ingestion/delivery off.
3. Run installScorerTrigger once and review Google's authorization screen. It
   installs one minute-polling trigger; it does not send a test email. Deploy >
   New deployment > Web app: Execute as yourself, access Anyone (anonymous).
   Your Workspace administrator may disallow anonymous web apps; if so this
   approach is blocked and a different host is required.
4. Return the deployed https://script.google.com/macros/s/DEPLOYMENT_ID/exec URL.
   Do not send your password or OAuth token. Keep editor/project sharing private.
   The deployment URL is public in the eventual APK and is not authentication.

## Required client work AFTER receiving that URL

Add an explicitly selected Apps Script transport: validate that exact HTTPS
/macros/s/ID/exec destination, support Google's response redirect with a strict
HTTPS script.googleusercontent.com GET-only allowlist, and require the JSON
response {ok:true}. Ordinary HTTP200 is NOT enough: Apps Script also returns200
for rejected input. Test accepted/rejected/offline/redirect/consent flows on the
actual deployment, then build a destination-specific APK. Existing /v1/usage
HTTPS collector support remains unchanged. Never silently reuse old local-only
consent; destination change must require fresh opt-in. Preserve World's no-op.

## Limits and privacy

Only the existing9-counter schema is accepted; only starts/ends are retained,
combined in bounded Script Properties, never individual player records or raw
requests. Other counters are discarded. The public response exposes no totals,
recipient or other configuration. No player emails, names, IDs or paired sessions.
Google still processes network/account metadata: no claim of anonymous transport
or no provider logging. Update the actual privacy policy/Data Safety for Google
Apps Script, email and retention before production collection is activated.

The minute trigger sends only when new starts/ends have arrived, combines arrivals
in one message, and has a fixed60email/day cap plus Google's current recipient
quota. Pending counts expire after7days on subsequent execution/request; email
copies follow mailbox retention. Closed/crashed Android processes cannot guarantee
final delivery. No strict real-time/per-session mail promise. Public ingestion can
be spoofed; the mail cap bounds messages but cannot prevent Google execution-quota
exhaustion. Suitable for a limited evaluation, not guaranteed high-volume service.
Sender is the authorizing Google account, with Google-controlled display/alias
rules. If sending succeeds but state persistence fails, duplicate mail is possible.
Disable SCORER_ENABLED and remove the trigger/deployment to stop service. Already
sent emails cannot be erased through app opt-out.

## Validation

Run node tests/test_apps_script.cjs. Tests use mocked Google services and never
access an account or send real email. Validate authorization, deployment redirect,
actual received test mail and Workspace admin restrictions with the real account
before declaring the integration connected. No new APK is supplied at this stage.
