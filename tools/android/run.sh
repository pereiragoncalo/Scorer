#!/bin/bash
set -euo pipefail
exec env -u DOCKER_HOST -u DOCKER_CONTEXT -u DOCKER_TLS -u DOCKER_TLS_VERIFY -u DOCKER_CERT_PATH docker --host=unix:///var/run/docker.sock run --rm --user 1000:1000 \
 --mount type=bind,src=/workspace/Scorer,dst=/work/source \
 --mount type=bind,src=/workspace/striker-android-build/cache,dst=/work/cache \
 --mount type=bind,src=/workspace/striker-android-build,dst=/work/toolchain \
 --mount type=bind,src=/etc/ssl/certs/ca-certificates.crt,dst=/run/ca-bundle.crt,readonly \
 --mount "type=bind,src=$CODEX_PROXY_CERT,dst=/run/proxy-ca.pem,readonly" \
 -e PATH=/work/cache/python-user/bin:/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin \
 -e PYTHONUSERBASE=/work/cache/python-user \
 -e SSL_CERT_FILE=/run/ca-bundle.crt -e REQUESTS_CA_BUNDLE=/run/ca-bundle.crt \
 -e GIT_SSL_CAINFO=/run/ca-bundle.crt -e CURL_CA_BUNDLE=/run/ca-bundle.crt \
 -e PIP_CERT=/run/ca-bundle.crt -e STRIKER_BUILD_CACHE=/work/cache/buildozer \
 -e APP_ANDROID_SKIP_UPDATE=1 \
 -e APP_ANDROID_SDK_PATH=/work/toolchain/android-sdk \
 -e APP_ANDROID_NDK_PATH=/work/toolchain/android-sdk/ndk/28.2.13676358 \
 -e JAVA_TOOL_OPTIONS=-Djavax.net.ssl.trustStore=/work/cache/java-cacerts \
 striker-android-build:phase1 "$@"
