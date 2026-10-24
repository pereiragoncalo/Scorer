# Data inventory for Play Console — draft, not final declarations

Review the actual production SDK versions, service deployment and Google definitions
before submitting the form. Having no AD_ID permission does **not** mean no data is
collected. This one application contains ads in Free and optional World purchases;
declare its full behaviour, not only the ad-free ownership state.

| Data / flow | Actual or planned treatment | Console review |
| --- | --- | --- |
| Player name, career, tables, custom names | App-private local JSON; no game upload; names files chosen via Android document picker | Not collected by the developer under the implemented game flow |
| Locale region | Read locally only for World contracts; Free has no country selector, no GPS/IP geolocation | Not transmitted by SCORER |
| Google advertising SDK | Free can send IP, app/device information, diagnostics and ad interactions to Google; UMP gates requests; no personalised advertising; all requests child/under-age, G | Review current SDK disclosure for approximate location, app activity, identifiers, diagnostics/performance, collection/sharing, purposes, optionality and ephemerality |
| Google Play billing | Google account/payment processing belongs to Play; app sees SKU, purchase state/token and formatted price, never card details | Review SDK/store treatment of purchase history and financial information; do not state that SCORER sees card data |
| Purchase verification service | HTTPS sends purchase token, package/SKU, random installation UUID and nonce; Google API verifies token; signed licence returned and held locally | Potential purchase history and app/other IDs, app functionality and fraud prevention; optional for Free; assess ephemeral processing and infrastructure logs accurately |
| Networking | Advertising/verification servers receive IP as part of connections | Document actual server logging/retention/processors and applicable data categories |
| Name-file editor | SAF read/write of a chosen JSON, bounded validation and explicit apply; no broad storage permission | Users control exports to a document provider; explain that provider's handling is separate |
| Private backups | Local previous-game, upgrade and editor backups; Android cloud backup disabled | Uninstall/clear app storage removes local data; exports outside app remain until user deletes them |

There is no SCORER account creation, chat, social login, contact collection, camera,
microphone, precise location or hidden gameplay analytics. Google Play ownership is
not a SCORER account. Determine whether the Play account-deletion requirement applies
to any later account feature; do not invent a deletion website for a nonexistent account.

Transport to the purchase verifier is HTTPS only, redirects refused. Client licence
verification uses RSA SHA256 and installation/nonce/expiry bounds. Backend source and
private keys/ADC credentials are excluded from the bundle. Purchase bodies and token
URLs must not be logged. Offline entitlement lasts at most seven days before renewal.

Outstanding declarations: public responsible party/support address, hosted non-PDF
privacy policy, actual service infrastructure/processors/retention, SDK Data Safety
mapping, audience/Families self-certified SDK eligibility, IARC, price/product setup,
app-ads.txt/store linkage where required. Do not submit placeholders or “no data
collected” for an advertising/billing-enabled production app.
