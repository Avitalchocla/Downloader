[app]
title = ELAZAR
package.name = elazardownloader
package.domain = org.elazar
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.4
requirements = python3,kivy==2.3.0,yt-dlp,requests,certifi,charset-normalizer,idna,urllib3
orientation = portrait
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
