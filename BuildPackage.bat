flet build apk --module-name StunConnects
flet build windows --module-name StunConnects
pyinstaller StunConnects.spec
pyinstaller StunServices.spec
