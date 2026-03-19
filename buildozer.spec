[app]

# (str) Title of your application
title = ELAZAR

# (str) Package name
package.name = elazardownloader

# (str) Package domain (needed for android packaging)
package.domain = org.elazar

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 1.1

# (list) Application requirements
# הוספנו כאן את כל מה שהקוד החדש צריך כדי לעבוד באינטרנט
requirements = python3,kivy==2.3.0,yt-dlp,requests,certifi,charset-normalizer,idna,urllib3

# (str) Custom source folders for requirements
# (list) Garden requirements
# (str) Presplash of the application
# (str) Icon of the application
# icon.filename = %(source.dir)s/icon.png

# (str) Supported orientations
orientation = portrait

# (list) Permissions
# חשוב מאוד: הרשאות אינטרנט וכתיבה לקבצים
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 31

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android SDK version to use
# android.sdk = 31

# (str) Android NDK version to use
android.ndk = 25b

# (bool) indicates if the application should be etched for the targets
# (list) Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup
android.allow_backup = True

# (str) The format used to package the app for release mode (aab or apk)
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aab)
android.debug_artifact = apk

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1
