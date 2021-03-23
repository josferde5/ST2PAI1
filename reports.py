import csv, os
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import main

def create_logs(rows):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'Reports/logs.csv')
    if os.path.isfile(filename):
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file, delimiter = '|', quotechar = "'", quoting = csv.QUOTE_NONNUMERIC)
            writer.writerows(rows)
        print ('The logs.csv file was updated. ' + str(len(rows)) + ' entries have been added.')
    else:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file, delimiter = '|', quotechar = "'", quoting = csv.QUOTE_NONNUMERIC)
            writer.writerow(['DATE', 'FILE_PATH', 'HASH_FILE', 'INTEGRITY_VERIFICATION'])
            writer.writerows(rows)
        print('The logs.csv file was created. ' + str(len(rows)) + ' entries have been added.')


def create_report(logs_file):
    dirname = os.path.dirname(__file__)
    now = datetime.now()
    limit = now + relativedelta(months = -1)
    filename = os.path.join(dirname, 'Reports/report_' + now.strftime('%m-%y') + '.html')
    logs = pd.read_csv(logs_file, sep= '|', quotechar= "'", quoting= csv.QUOTE_NONNUMERIC)
    logs['DATE'] = pd.to_datetime(logs['DATE'])
    filtered_logs = logs.loc[(logs['DATE'] >= limit.strftime('%d/%m/%Y %H:%M:%S')) & (logs['DATE'] <= now.strftime('%d/%m/%Y %H:%M:%S'))]
    false, true = filtered_logs['INTEGRITY_VERIFICATION'].value_counts()
    html = filtered_logs.to_html()
    Html_file= open(filename, "w")
    Html_file.write('<h1> Monthly report </h1>')
    Html_file.write('<h4> From ' + limit.strftime('%d/%m/%Y') + ' to ' + now.strftime('%d/%m/%Y')  + '</h4>')
    Html_file.write('<h3> Integrity rate: ' + str(round(true / len(filtered_logs) * 100, 2)) + '%</h3>')
    Html_file.write(html)
    Html_file.close()
    
    main.send_email()
    print("The report was created in the 'Reports' folder and the email was sent")

    
rows = (['22/03/2021 17:19:11', 'C:/Prueba', 'asdgkfgfasgdfasgdfjasgdfj', True],
        ['22/03/2021 17:19:11', 'C:/Prueba', 'asdgkfgfasgdfasgdfjasgdfj', False],
        ['22/04/2021 17:19:11', 'C:/Prueba', 'asdgkfgfasgdfasgdfjasgdfj', True],
        ['22/04/2021 17:19:11', 'C:/Prueba', 'asdgkfgfasgdfasgdfjasgdfj', True],
        ['22/03/2021 17:19:11', 'C:/Prueba', 'asdgkfgfasgdfasgdfjasgdfj', False],
        ['19/03/2021 17:19:11', 'C:/Prueba', 'asdgkfgfasgdfasgdfjasgdfj', False],
        ['18/03/2021 17:19:11', 'C:/Prueba', 'asdgkfgfasgdfasgdfjasgdfj', False])    

config_log(rows)
create_report('Reports/logs.csv')