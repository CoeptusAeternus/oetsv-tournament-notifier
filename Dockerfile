FROM python:3.12-slim-bookworm

# Install cron and clean up cache to reduce image size
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all necessary files
COPY . /app

# Set correct permissions
RUN chmod +x /app/new_tournament.py \
    /app/nennschluss.py \
    /app/startup.py \
    /app/entrypoint.sh

# Set up crontab
COPY cronfile /etc/cron.d/container_cron
RUN chmod 0644 /etc/cron.d/container_cron && crontab /etc/cron.d/container_cron

# Use the entrypoint script
CMD ["/app/entrypoint.sh"]
