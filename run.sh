CRON=${CRON:-"0 3 * * *"}

touch /root/cron.out

echo "${CRON} /usr/local/bin/python /app/main.py >> /root/cron.out 2>&1" | crontab -

cron && tail -f /root/cron.out
