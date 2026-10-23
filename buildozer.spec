[app]
title = Striker
package.name = striker
package.domain = com.clemir
source.dir = .
source.exclude_dirs = baseline,tests,docs,tools,.git,.buildozer,bin
source.exclude_patterns = striker_career.json,*.keystore,*.jks,*.log
source.include_exts = py,png,jpg,jpeg,kv,json,atlas,ttf
version = 0.6.1
requirements = python3,kivy==2.3.1
orientation = landscape
fullscreen = 1
android.permissions =
android.api = 36
android.minapi = 26
android.archs = arm64-v8a
android.ndk = 28c
android.ndk_api = 26
p4a.branch = master
p4a.commit = 58d21141f17c889bf8585f5665921d72028f8831
android.release_artifact = aab
android.debug_artifact = apk
android.accept_sdk_license = False
[buildozer]
log_level = 2
warn_on_root = 1
