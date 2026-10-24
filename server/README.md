# SCORER World verification service — server only

Prepared code, **not deployed**. No real purchases or server licences have been issued.
The app ships with billing disabled and an empty endpoint/key. Do not package this
folder or a Google credential/private key in an APK. The release source allowlist
and Buildozer exclusions enforce this separation.

Use a separately administered Python service with the pinned requirements. Configure
Application Default Credentials for a Google Cloud identity authorised via Play
Console to query/acknowledge this app's purchases. Prefer workload identity; if a
credential file is unavoidable, mount it as a deployment secret outside source.
No service account is configured in this workspace and no Cloud resource was created.

Generate and retain an RSA signing key >=2048 bits in the deployment's secret system;
set SCORER_LICENSE_PRIVATE_KEY to its mounted PEM path. Export only its public key as
X509 SubjectPublicKeyInfo DER/base64 into the app's PUBLIC release configuration.
This is an offline-licence signing key, distinct from Android's upload/app signing keys.
The server cannot recover a lost key; rotation needs an app/public-key rollout plan.
No private key, password, ADC file or purchase token belongs in Git or this conversation.

Run the WSGI callable `server.world_licensing:application`, for example with gunicorn,
behind authenticated administration and a **public HTTPS** POST endpoint at
`/v1/world/verify`. The client is a public mobile app; a shared client secret would
not authenticate it and must not be embedded. Verification depends on Google's token
lookup, not an untrusted client claim of ownership. Add deployment-level rate limits,
request-size/time limits, concurrency limits, health checks, outage alerts and abuse
controls. Do not log request bodies, purchase tokens or token-bearing upstream URLs.
Restrict Google identity permissions to this app; configure secret access/rotation,
network egress and operational retention before releasing to real customers.

The service is stateless: every request rechecks Google before issuing access. The
installation UUID is generated locally; it binds the signed licence, not an account.
Reinstall/new device gets a new ID and must restore using Play ownership. The native
client checks RSA signature, package, SKU, installation, request nonce, issuance and
expiry before committing an envelope to private preferences. Local save edits and
server error bodies never grant entitlement. Successful Google purchase acknowledgement
is required before issuing a new licence. Already acknowledged purchases can be
restored repeatedly without consuming them. Network failures do not create access.

Production rejects Google test and rewarded purchases. For an **approved** isolated
Play licence-test deployment only, set SCORER_ALLOW_TEST_PURCHASES=1. Never silently
enable this on a production service. Use the deployed test service/public key only
in the corresponding approved candidate. Repository/rehearsal builds stay disabled.

A signed licence expires in seven days. Google refund/cancellation becomes visible
on renewal/restore; offline access can survive until expiry. RTDN/webhook processing,
central entitlement accounts, instant cross-device revocation and customer support
operations are not implemented. Deploy only after accepting this bounded-offline
policy, completing live test-token tests and documenting actual data handling.

Tests inject a fake Google transport and an ephemeral RSA key; they exercise purchase
state rejection, acknowledgement, signing/tamper checks, request validation and error
redaction. **They do not verify a real Play account, endpoint or purchase.**
