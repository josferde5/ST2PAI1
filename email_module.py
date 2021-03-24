from __future__ import print_function

import base64
import datetime
import mimetypes
import os.path
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import config

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def init_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    return service


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    encoded_msg = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': encoded_msg.decode()}


def create_file_message(sender, to, subject, message_text, file):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(file, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(file, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(file, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(file, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)
    encoded_msg = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': encoded_msg.decode()}


def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Sent with Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def send_alert_email(filepath, alert_type):
    c = config.Config()
    dt_string = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    email_sender = 'HIDS ST2 Service'
    email_to = c.contact_email
    email_subject = 'ALERTA: Detectado fallo de integridad'

    if alert_type == 0:
        email_body = 'Durante la verificación del sistema de archivos en vigilancia con fecha y hora ' + dt_string + ', se ha detectado que el fichero ' + filepath + ' presenta un fallo de integridad ya que el hash enviado por el cliente no es igual al almacenado en el servidor.'
    elif alert_type == 1:
        email_body = 'Durante la verificación del sistema de archivos en vigilancia con fecha y hora ' + dt_string + ', se ha detectado que el fichero ' + filepath + ' presenta un fallo de integridad ya que el MAC obtenido en el cliente no es igual al obtenido en el servidor.'
    else:
        email_body = 'Durante la verificación del sistema de archivos en vigilancia con fecha y hora ' + dt_string + ', se ha detectado que el fichero ' + filepath + ' presenta un fallo de integridad ya que ha sido eliminado o no se encuentra.'

    raw_message = create_message(email_sender, email_to, email_subject, email_body)
    send_message(init_service(), "me", raw_message)


def send_report_email(report_path):
    c = config.Config()
    email_sender = 'HIDS ST2 Service'
    email_to = c.contact_email
    email_subject = 'INFORMACIÓN: Informe de integridad mensual'
    email_body = 'A través de este email se pone a su disposición un reporte de las verificaciones de integridad del sistema de archivos del último mes. A partir de este momento se cierra el ciclo de verificación y se comienza el siguiente. Podrá encontrar el reporte en los archivos adjuntos de este email.'

    raw_message = create_file_message(email_sender, email_to, email_subject, email_body, report_path)
    send_message(init_service(), "me", raw_message)
