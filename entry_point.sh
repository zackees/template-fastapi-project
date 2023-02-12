#! /bin/bash
uvicorn --host 0.0.0.0 --port 80 --workers 8 --forwarded-allow-ips=* fastapi_template_project.app:app
