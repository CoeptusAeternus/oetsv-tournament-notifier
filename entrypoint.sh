#!/bin/sh

# Make environment variables available to cron jobs
printenv | grep -v "no_proxy" >> /etc/environment

# Validate config and seed existing tournaments so startup is safe
python /app/startup.py
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
	exit $EXIT_CODE
fi

# Start cron in foreground
exec cron -f
