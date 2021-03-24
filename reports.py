import csv, os
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


def create_logs(rows):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'Reports/logs.csv')
    if os.path.isfile(filename):
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file, delimiter='|', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
            writer.writerows(rows)
        print('The logs.csv file was updated. ' + str(len(rows)) + ' entries have been added.')
    else:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='|', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(['DATE', 'FILE_PATH', 'HASH_FILE', 'INTEGRITY_VERIFICATION'])
            writer.writerows(rows)
        print('The logs.csv file was created. ' + str(len(rows)) + ' entries have been added.')


def create_report(logs_file):
    dirname = os.path.dirname(__file__)
    now = datetime.now()
    limit = now + relativedelta(months=-1)
    filename = os.path.join(dirname, 'Reports/report_' + now.strftime('%m-%y') + '.html')
    logs = pd.read_csv(logs_file, sep='|', quotechar="'", quoting=csv.QUOTE_NONNUMERIC)
    logs['DATE'] = pd.to_datetime(logs['DATE'])
    filtered_logs = logs.loc[
        (logs['DATE'] >= limit.strftime('%d/%m/%Y %H:%M:%S')) & (logs['DATE'] <= now.strftime('%d/%m/%Y %H:%M:%S'))]
    false, true = filtered_logs['INTEGRITY_VERIFICATION'].value_counts()
    html = filtered_logs.to_html()
    html_file = open(filename, "w")
    html_file.write('<h1> Monthly report </h1>')
    html_file.write('<h4> From ' + limit.strftime('%d/%m/%Y') + ' to ' + now.strftime('%d/%m/%Y') + '</h4>')
    html_file.write('<h3> Integrity rate: ' + str(round(true / len(filtered_logs) * 100, 2)) + '%</h3>')
    html_file.write(html)
    html_file.close()

    print("The report was created in the 'Reports' folder and the email was sent")
