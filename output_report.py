import constants
import datetime

def open_year_file(log):
    """ Open annual report html file and start html """
    htmlfile = constants.OUTPUT_FOLDER+'Log-'+log['year']+'.html'
    hf = open(htmlfile, 'w')
    hf.write(f"<!DOCTYPE html><html lang='en'>\n"
             "<head>\n"
             "<meta name='viewport' content='width=device-width, initial-scale=1'>\n"
             "<title>Training Log %s</title>\n"
             "<link rel='stylesheet' href='log.css'>\n"
             "</head>\n"
             "<body>\n"
             "<header>\n"
             "<h1>Training Log %s</h1>\n"
             "</header><main>\n" % (log['year'], log['year']))
    return(hf)

def open_week_file(log, week):
    """ Open weekly report html file and start html """
    htmlfile = constants.OUTPUT_FOLDER+'Log-'+log['year']+'-'+f"%02d"%(week)+'.html'
    hf = open(htmlfile, 'w')
    hf.write(f"<!DOCTYPE html><html lang='en'>\n"
             "<head>\n"
             "<meta name='viewport' content='width=device-width, initial-scale=1'>\n"
             "<title>Training Log %s Week %s</title>\n"
             "<link rel='stylesheet' href='log.css'>\n"
             "</head>\n"
             "<body>\n"
             "<header>\n"
             "<h1>Training Log %s Week %s</h1>\n"
             "</header><main>\n" % (log['year'], week, log['year'], week))
    return(hf)

def close_file(hf):
    """ Close an html file """
    hf.write('</main></body></html>')
    hf.close()

def start_week(hf, year, week_num, link, weekly_activities, weekly_time, weekly_load):
    """ Output weekly header information """
    hf.write("<section>\n")
    hf.write("<div class='week'>\n")
    # The link parameter indicates if hte week number should be a link to the weekly file,
    # which is true for the annual file
    if (link):
        weekFormatted = (f"%02d"%(week_num))
        hf.write(f"<p class='week_num'><a href='Log-{year}-{weekFormatted}.html'>Week {week_num}</a></p>\n")
    else:
        hf.write(f"<p class='week_num'>Week {week_num}</p>\n")
    hf.write("<div class='weekly_header'>")
    hf.write("<div class='weekly_header_element'>%d activities</div>\n" % (weekly_activities))
    hf.write("<div class='weekly_header_element'>%d:%02d hours</div>\n" % (weekly_time/60//60, weekly_time/60%60))
    hf.write("<div class='weekly_header_element'>%s calories</div>\n" % (f"{weekly_load:,.0f}"))
    hf.write("</div>\n")

def close_week(hf):
    # Close html for a week
    hf.write("</div>")
    hf.write("</section>")
    return

def output_week(hf, week):
    # Loop through a week and output activities, and if none found, output rest day
    for j in range(7):
        hf.write("<p class='day_header'>%s</p>\n" % (week['isoday'][j]['date'].strftime("%a %b %d %Y")))
        if week['isoday'][j]['day_total_activities'] > 0:
            for activity in week['isoday'][j]['activity']:
                output_activity(hf, activity)
        else:
            output_restday(hf, week['isoday'][j]['date'])

def output_restday(hf, date):
    # If the rest day is a past day, output rest, otherwise may just not have an activity for current day
    today = datetime.datetime.today()
    if date < today.date():
        hf.write("<div class='activity_box'>\n")
        hf.write("<div class='activity_box_element'>Rest day</div>\n")
        hf.write("</div>")

def output_activity(hf, activity):
    # Check for attributes and skip if they don't exist
    if all(key in activity for key in ['start_time', 'sport', 'total_timer_time', 'load']):

        # Start activity
        hf.write("<div class='activity_box'>\n")

        # Write start time in local time zone
        hf.write("<div class='activity_box_element'>Start Time<br/>%s</div>\n" %
                    (activity['start_time'].astimezone().strftime("%I:%M %p")))
        
        # Write sport name
        hf.write(f"<div class='activity_box_element'>Type<br/>{activity['sport']}</div>\n")
        
        # Write total time with appropriate punctuation
        if activity['total_timer_time'] > 60*60:
            hf.write("<div class='activity_box_element'>Duration<br/>%d:%02d:%02d</div>\n" %
                        (activity['total_timer_time']//(60*60),
                        activity['total_timer_time']/60%60,
                        activity['total_timer_time']%60))
        else:
            hf.write("<div class='activity_box_element'>Duration<br/>%d:%02d</div>\n" %
                        (activity['total_timer_time']//60,
                        activity['total_timer_time']%60))
        
        # Write load
        hf.write("<div class='activity_box_element'>Calories<br/>%s</div>\n" % (f"{activity['load']:,.0f}"))

        # Write workout name if it exists
        if activity['wkt_name'] is not None and \
            activity['wkt_name'].casefold() != activity['sport'].casefold():
            hf.write("<div class='activity_box_element'>%s</div>\n" %
                        (activity['wkt_name']))

        hf.write("</div>")    

def output_report(log):
    """ Output the training log annual and weekly html files """

    # Open annua file
    hf = open_year_file(log)

    # Loop through weeks
    for i in range(53):
        if log['isoweek'][i]['week_total_activities'] > 0:
            # If a week has activities, open weekly file, and output sessions to weekly file
            wf = open_week_file(log, i+1)
            start_week(wf, log['year'], i+1, False,
                        log['isoweek'][i]['week_total_activities'],
                        log['isoweek'][i]['week_total_time'],
                        log['isoweek'][i]['week_total_load'])
            output_week(wf, log['isoweek'][i])
            close_week(wf)
            close_file(wf)
            
            # Ouput sessions to annual file
            start_week(hf, log['year'], i+1, True,
                        log['isoweek'][i]['week_total_activities'],
                        log['isoweek'][i]['week_total_time'],
                        log['isoweek'][i]['week_total_load'])
            close_week(hf)
    
    # Close annual file after week loop
    close_file(hf)

    return