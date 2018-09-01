release: flask db upgrade; python deploytasks.py
web: flask db migrate; flask db upgrade; gunicorn partnersApp:app