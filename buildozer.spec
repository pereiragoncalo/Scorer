[app]
title = SCORER Free
package.name = striker
package.domain = com.clemir
source.dir = .
source.exclude_dirs = server,baseline,tests,ui_tests,docs,tools,android,release,.git,.buildozer,bin
source.exclude_patterns = striker_*.json,scorer_language.json,*.keystore,*.jks,*.log,*.pem,*.p12,release.local.json
source.include_exts = py,png,jpg,jpeg,kv,json,atlas,ttf,otf,license
version = 0.6.29
requirements = python3,kivy==2.3.1,chardet==5.2.0
orientation = landscape
fullscreen = 1
presplash.filename = assets/splash.png
icon.filename = assets/icon.png
android.presplash_color = #06191f
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.enable_androidx = True
android.gradle_dependencies = com.google.android.gms:play-services-ads:25.5.0,com.google.android.ump:user-messaging-platform:4.0.0,com.android.billingclient:billing:8.0.0
android.add_src = android/src,android/worldsrc
android.extra_manifest_xml = android/manifest-extra.xml
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713
android.allow_backup = False
android.extra_manifest_application_arguments = android/application-args.xml
android.numeric_version = 1026629
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
