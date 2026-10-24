#!/bin/bash
# Sign an already validated AAB outside Buildozer. Never activate or upload anything.
set -euo pipefail
if [ "$#" -ne 2 ]; then
    echo 'Usage: sign_aab.sh INPUT_UNSIGNED.aab OUTPUT_SIGNED.aab' >&2
    exit 2
fi
if ! command -v jarsigner >/dev/null; then
    echo "A full JDK with jarsigner is required; a Java runtime alone is insufficient." >&2
    exit 2
fi
: "${SCORER_UPLOAD_KEYSTORE:?Set the protected upload-keystore path}"
: "${SCORER_UPLOAD_ALIAS:?Set the upload-key alias}"
: "${SCORER_UPLOAD_STORE_PASSWORD:?Inject the password through a secure environment}"
: "${SCORER_UPLOAD_KEY_PASSWORD:?Inject the key password through a secure environment}"
if [ ! -f "$1" ] || [ -e "$2" ]; then
    echo 'Input must exist and output must be a fresh path.' >&2
    exit 2
fi
# Passwords are resolved by the JDK, never expanded into argv. Do not use shell tracing.
jarsigner -keystore "$SCORER_UPLOAD_KEYSTORE" -storepass:env SCORER_UPLOAD_STORE_PASSWORD \
    -keypass:env SCORER_UPLOAD_KEY_PASSWORD -sigalg SHA256withRSA -digestalg SHA-256 \
    -signedjar "$2" "$1" "$SCORER_UPLOAD_ALIAS"
jarsigner -verify "$2"
echo 'Signed locally. Verify certificate against Play Console; no upload performed.'
