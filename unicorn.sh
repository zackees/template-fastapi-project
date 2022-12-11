uvicorn --host 0.0.0.0 --port 80 --reload --reload-dir restart --workers 8 --forwarded-allow-ips=* fastapi_template_project.app:app
