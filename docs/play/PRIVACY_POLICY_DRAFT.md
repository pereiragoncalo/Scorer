# SCORER privacy policy — draft, not yet publicly hosted

Effective date: [DATE]. Developer/legal controller: [OWNER IDENTITY].
Contact: [OWNER-APPROVED PUBLIC SUPPORT EMAIL]. Public policy URL: [HTTPS URL].
Owner must fill these before publication; do not infer a private mailbox's public use.

Scorer and Scorer World are separate applications with independent private careers.
This0.6.43 release has no advertising SDK, adverts, rewarded videos, commercial
stadium panels or in-app billing. World purchases, if offered by an app store, are
handled by that store; no live payment activation is performed by this code.

The game works offline. Player names, careers, fixture history and editor files
normally stay on-device. World uses phone locale locally to suggest a language
and start country. There is no location permission or whole-career cloud upload.
Private backups remain on-device; Android cloud backup is disabled. SAF exports
use the document provider the player selects. Uninstall/clear data removes local
files; removing local data does not itself withdraw existing public records.

## Optional usage statistics

Disabled until enabled in Privacy, independently of leaderboard sharing. All three
editions may send nine allowlisted numeric counts over HTTPS to
https://stats.clemir.com/v1/usage: session starts/normal ends, new/loaded careers,
completed training/matches, goals and selected save/load failures. No name, career
file, free text, location, contacts, device/advertising/install/session identifier,
exact event timestamp or stack trace is included. Counts do not measure unique
players. Forced termination may omit a session end; offline batches can arrive
late, and ambiguous acknowledgements can duplicate totals.

Own collector stores only combined counts by UTC receipt-day/event, retained90days.
Local unsent counts expire after7days on next use. Disable and Erase stops new
collection and removes unsent data; an in-flight request may finish. Already
combined totals cannot be identified as an individual's contribution for deletion.

## Optional public season records

Viewing ranking does not publish a record. Separate Share confirmation authorizes
publishing the chosen player name, finishing team, completed season, matches,
goals, country and division to https://stats.clemir.com. Use a nickname; never enter
real full names, contact or school information. Scores are reported by games, not
verified anti-cheat results. World boards are separated by country/division; Free
has one board. Best completed records are stored until withdrawal. In-progress
goals are not published in the new version. Previous alias-only live records are
not relabelled as completed seasons.

A randomly generated secret in app-private storage authorizes submissions/removal;
the server stores its hash and never returns it publicly. Stop Sharing & Remove
requests deletion of the user's public records and stops new uploads. Offline
removal remains pending until it can reach the server. Keep the app/data until
removal completes; losing the credential can prevent automatic ownership proof.
Contact [PUBLIC SUPPORT] for deletion/help, with no passwords or secret tokens.

## Transport, children and processors

HTTPS validates host/certificates. Cloudflare Tunnel/CDN processes connection
information including IP addresses; the laptop collector does not store IPs,
user agents or raw request logs. The owner must confirm current provider logging,
controller/processors, security, lawful basis and retention before publishing.
No automated email service is active. No administrator credentials are in the app.

The intended audience includes minors. The present nickname safety reminder is
NOT verified parental authorization. Before Play publication the owner must settle
age groups, Families/social-feature requirements and appropriate adult controls;
no compliance claim is made by this draft. Published user-chosen names also need
appropriate moderation/reporting arrangements. Players/guardians can disable
optional sharing and counters independently. Do not require optional sharing to play.
