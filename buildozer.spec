[app]
title = Scorer
package.name = striker
package.domain = com.clemir
source.dir = .
source.exclude_dirs = baseline,tests,ui_tests,docs,tools,.git,.buildozer,bin
source.exclude_patterns = striker_career*.json,*.keystore,*.jks,*.log
source.include_exts = py,png,jpg,jpeg,kv,json,atlas,ttf
version = 0.6.5
requirements = python3,kivy==2.3.1,chardet==5.2.0
orientation = landscape
fullscreen = 1
presplash.filename = assets/splash.png
icon.filename = assets/icon.png
android.presplash_color = #06191f
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
