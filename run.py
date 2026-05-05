"""
run.py
───────
Entry point de la aplicación.
- Desarrollo: python run.py
- Producción: gunicorn run:app  (ver Procfile)
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
