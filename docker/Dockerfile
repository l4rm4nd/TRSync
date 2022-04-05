# Dockerfile
FROM python:3.9.12-slim

# update and install software
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    gcc \
    libc-dev \
    bsdmainutils \
    dnsutils && \
    mkdir -p /opt/mysite

# copy source, fix dependencies, permissions and openssl
COPY . /opt/mysite/
WORKDIR /opt/mysite
RUN pip install --upgrade pip && \
    pip3 install -r requirements.txt --cache-dir /opt/mysite/pip_cache && \
    pip3 install uwsgi -I --no-cache-dir && \
    chown -R www-data:www-data /opt/mysite && \
    chmod -R 770 /opt/mysite && \
    chmod +x /opt/mysite/docker/entrypoint.sh

# run container as low privileged user
USER www-data

# start uwsgi server
ENTRYPOINT ["/opt/mysite/docker/entrypoint.sh"]
EXPOSE 8000
STOPSIGNAL SIGTERM