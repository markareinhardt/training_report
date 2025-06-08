# training_report
Simple training report for RunGap exports (zip format) on Mac

## Purpose
This program produces an html 'training report' from a directory containing RunGap export files (zip format). RunGap is an iOS app that can read training sessions from many different sources, and can export to many destinations including file export. The export depends on the purchase of the RunGap "swag bag" which I find is well worth the cost.

Why this simple training log? I wanted to learn python, and I use RunGap to export my training sessions to a folder in my iCloud drive, which is synced to my Mac. This program could be adapted to import FIT files, but I found the RunGap zip export contained everything I wanted for now, and processes much faster than cycling through FIT files every time it ran.

There are lots of improvements that could be made - this is ultimately a very simple program.

## Dependencies
Homebrew python3: https://formulae.brew.sh/formula/python@3.13  
Homebrew nginx: https://formulae.brew.sh/formula/nginx  
Create a directory called training_report in nginx www directory  
Copy log.css into training_report directory  

## Generating report
You can generate the report by just calling "python3 generate.py" with an optional year parameter. The report will be generated on your local Mac machine. I write it to the nginx folder and view the report locally only. I haven't bothered to export the html files to something that exposes the report outside the local machine.

## Viewing report on local machine
http://localhost:8080/training_report/Log-2025.html (replace year as appropriate)

## Running generator every hour
I use cron to run the report 'hourly' (which works when the Mac is awake - so isn't really 'hourly'). Cron prompted for permission for Python to access files the first time.

Cron to run hourly:
0 * * * * /opt/homebrew/bin/python3 /Users/{yourname}/{path_to_source}/generate.py >> /Users/{yourname}/cron_log.txt 2>&1
