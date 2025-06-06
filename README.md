# training_report
Simple training report

Homebrew python3
Homebrew nginx
Cron to run hourly:
0 * * * * /opt/homebrew/bin/python3 /Users/{yourname}/{path_to_source}/generate.py >> /Users/{yourname}/cron_log.txt 2>&1