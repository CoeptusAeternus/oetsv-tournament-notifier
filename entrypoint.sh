#!/bin/sh

# set container environment variables for cron
printenv | grep -v "no_proxy" >> /etc/environment

# Execute entrypoint.py and capture its exit code
/app/entrypoint.py
EXIT_CODE=$?

# If entrypoint.py fails, exit with the same code
if [ $EXIT_CODE -ne 0 ]; then
    echo "entrypoint.py failed with exit code $EXIT_CODE"
    exit $EXIT_CODE
fi

# Start cron in the foreground
echo "Starting cron"
exec cron -f
