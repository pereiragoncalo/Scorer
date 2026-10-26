# SCORER privacy policy — draft, not a hosted policy

Effective date: [DATE]. Responsible developer: [PUBLIC/LEGAL IDENTITY].
Privacy/support: [PUBLIC EMAIL]. Policy URL: [PUBLIC HTTPS URL].
Replace placeholders and review the actual hosting/processors before publication.

Scorer Free and Scorer World are separate Android applications with separate
private careers. Free has one division and advertising. World has worldwide
career/editor features and no advertising SDK. There is no SCORER account or
in-app billing/purchase-verification service in the current two-app builds.

Names, careers, custom names and backups stay in app-private device storage.
The local World names editor uses Android's document picker. Free is English-only;
World reads the primary phone locale locally for language/country suggestions and
supports manual language choice. Locale, names and career files are not uploaded.
No GPS, contact, microphone or camera permission is requested. Android backup is
disabled; uninstalling/clearing app data removes the private files.

## Optional Free usage counters

Off by default, separate from advertising consent. Players may enable/withdraw in
Privacy. Underage players should consult a parent/guardian. Counters include app
starts after the splash, careers started/loaded, training and matches completed,
player goals and selected load/save failures. No free text, event log, player or
club names, career/fixture files, email address, device/account/advertising/install
identifier, locale, location, exact session timestamp or stack trace is included.
The feature does not measure unique players, retention or identified installs.

In the unconfigured beta, counters are local only and nothing is sent by this
feature. A configured release sends only aggregate numeric counts over HTTPS to
[ACTUAL COLLECTOR DOMAIN]. A changed destination requires a new local opt-in.
Local unsent counters expire after seven days when the app next runs. Withdrawal
stops new collection and clears unsent counts. An already in-flight transmission
may complete; already combined totals have no individual record to retrieve/delete.

The receiving server necessarily sees an IP during the connection. The prepared
collector stores no IP, user agent, raw report or per-player identifier; hosting,
reverse-proxy/CDN and error logs must also be configured consistently. It immediately
combines counts into daily totals by UTC receipt date, keeping aggregate totals
for90days. Offline batches may arrive later, and uncertain network acknowledgements
can cause duplicate counts; totals are approximate. No unique-user claim is made.

The owner may receive daily aggregate summaries by email through [ACTUAL SMTP
PROVIDER]. Emails contain totals, not players' addresses or individual records;
the owner's mailbox/provider controls retention of those summaries. Email and
collector credentials live only on the server, never in the Android app. No email
is sent by the player's email account. No hosting/email service is activated by
merely preparing this source or beta APK.

## Advertising in Free

Banner on entry after the splash, interstitials between matches and optional
rewarded training ads depend on availability/consent and never interrupt a shot.
Requests remain child/under-age, general-audience and non-personalised; AD_ID and
AdServices permissions are absent. Google can process IP, approximate location
inferred from IP, app/device information, diagnostics and ad interactions. See
https://policies.google.com/privacy and in-game advertising privacy options.
The current beta uses Google test IDs and does not earn ad revenue.

World has no usage-counter collection/transport, advertising SDK or Internet
permission. Public store payment processing, if World is later sold separately,
is handled by the chosen app store; no card details enter SCORER. Public listing,
actual processors/retention/contact details and Play/Families declarations remain
to be completed against the real deployed configuration.
