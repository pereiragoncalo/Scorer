#!/bin/bash
set -euo pipefail
cd /workspace/Scorer
mkdir -p /workspace/striker-android-build/cache/user /workspace/striker-android-build/cache/python-user/lib/python3.12/site-packages
python3 tools/android/configure_pip_trust.py
BUILDX_CONFIG=/workspace/striker-android-build/buildx \
 env -u DOCKER_HOST -u DOCKER_CONTEXT -u DOCKER_TLS -u DOCKER_TLS_VERIFY -u DOCKER_CERT_PATH \
 docker --host=unix:///var/run/docker.sock build \
 --secret id=ca_bundle,src=/etc/ssl/certs/ca-certificates.crt \
 -t striker-android-build:phase1 tools/android
bash tools/android/run.sh bash -c 'set -e; cp /usr/lib/jvm/java-17-openjdk-amd64/lib/security/cacerts /work/cache/java-cacerts; keytool -importcert -noprompt -alias codex-session-proxy -file /run/proxy-ca.pem -keystore /work/cache/java-cacerts -storepass changeit; javac -version; python -m unittest discover -s tests -v'
bash tools/android/install_sdk.sh
