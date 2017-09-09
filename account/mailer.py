# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import Encoders
import smtplib
import django
from django.utils.html import escape


def mail(to, subject, text, attach):
    print to
    msg = MIMEMultipart()
    msg['From'] = 'no_reply@dari-specheli.com'
    msg['To'] = ', '.join(to)
    msg['Subject'] = subject
    # text = email_template.text.format(name)
    msg.attach(MIMEText(text, 'html'))

    if attach:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % os.path.basename(attach))
        msg.attach(part)

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    try:
        mailServer.login("", "1qazZAQ!")
        # sender, recipients
        mailServer.sendmail('', to, msg.as_string())
        # Should be mailServer.quit(), but that crashes...
        mailServer.close()
    except Exception, e:
        print "Unable to login", e


# if __name__ == "__main__":
#     subject = "Thanks for sign up"

    # recipient_list = ['divya.madaan94@gmail.com']
    # mail(recipient_list, subject, 'divya', "")
