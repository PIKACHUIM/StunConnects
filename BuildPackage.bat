flet build apk --module-name StunConnects
flet build windows --module-name StunConnects
pyinstaller StunConnects.spec
flet run --web --port 1680 StunConnects.py
