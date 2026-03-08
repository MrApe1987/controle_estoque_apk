[app]

title = Controle de Estoque

package.name = controleestoque

package.domain = org.controle

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,json,atlas

version = 0.1

requirements = python3==3.10.12, hostpython3==3.10.12, kivy, kivymd, pyjnius

orientation = portrait

fullscreen = 0

# Splash screen
presplash.filename = %(source.dir)s/splash.png
android.presplash_color = #FFFFFF

# Icone do app
icon.filename = %(source.dir)s/icon.png

# Android API
android.api = 33
android.minapi = 21
android.ndk_api = 21

# Arquiteturas
android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True

android.copy_libs = 1

# Logcat
android.logcat_filters = *:S python:D

# Debug gera APK
android.debug_artifact = apk


#
# Python for android
#

p4a.branch = master


#
# iOS (não usado mas necessário no arquivo)
#

ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

ios.codesign.allowed = false


[buildozer]

log_level = 2

warn_on_root = 1
