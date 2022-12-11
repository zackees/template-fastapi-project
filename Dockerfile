# FROM ubuntu:22.04
FROM python:3.10.5-bullseye
# Might be necessary.
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
# All the useful binary commands.
RUN apt-get update && apt-get install -y --force-yes --no-install-recommends \
    apt-transport-https \
    ca-certificates
WORKDIR /app
RUN pip install --upgrade pip
# for sending files to other devices
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN python -m pip install -e .
# Expose the port and then launch the app.
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "80", "fastapi_template_project.app:app"]
