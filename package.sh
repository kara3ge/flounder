pyinstaller --onefile \
  --add-data "flask/templates:templates" \
  --add-data "flask/static:static" \
  --add-data "config.py:." \
  flask/app.py