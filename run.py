from app import create_app

app = create_app()  # dev: flask --app run run | prod: gunicorn run:app