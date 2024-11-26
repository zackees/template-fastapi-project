FROM python:3.10.5-bullseye
# Might be necessary.
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# declare debian not interactive
ENV DEBIAN_FRONTEND=noninteractive

# This takes a long time so let's get it out of the way first
RUN apt-get update

# All the useful binary commands.
RUN apt-get install -y --force-yes --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*



RUN apt-get update && apt-get install -y --force-yes --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip
# for sending files to other devices
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN dos2unix entry_point.sh
RUN python -m pip install --no-cache-dir -e .
# Expose the port and then launch the app.
EXPOSE 80
CMD ["/bin/bash", "entry_point.sh"]
