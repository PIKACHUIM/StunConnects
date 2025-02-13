flet build apk --module-name StunConnects
flet build windows --module-name StunConnects
pyinstaller -F StunConnects.py --icon=StunConnects.ico

