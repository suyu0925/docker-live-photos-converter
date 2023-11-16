CRON=${CRON:-"0 * * * *"}

touch /root/cron.out

crontab -l | { cat; echo "${CRON} /usr/local/bin/python /app/main.py >> /root/cron.out 2>&1"; } | crontab -

cron && tail -f /root/cron.out
