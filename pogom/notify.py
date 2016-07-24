import email
import smtplib
import time

import staticmap


class PokeNotifier(object):
    def __init__(self, credentials):
        self.pokeset = set()
        self.credentials = credentials

    def notify(self, pokemon):
        pokehash = str(pokemon['id']) + str(pokemon['lat']) + str(pokemon['lng'])

        if pokehash in self.pokeset:
            print('[!] Notification already sent for this Pokemon! Skipping...')
            return

        self.pokeset.add(pokehash)

        username, password = self.credentials['gmail_account']['username'], \
                             self.credentials['gmail_account']['password']

        fromaddr = username
        toaddrs = ['YOUR_EMAIL_ADDRESS']

        for toaddr in toaddrs:
            msg = email.MIMEMultipart.MIMEMultipart()

            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "[Pokebot] Pokemon Located! - %s" % pokemon['name']

            disappear_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(pokemon['disappear_time']))
            body = '\r\n'.join(("Pokemon Name: %s" % pokemon['name'],
                                "Disappears at: %s" % disappear_datetime,
                                "", ""))

            msg.attach(email.MIMEText.MIMEText(body, 'plain'))

            filename = "pokemap.png"
            attachment = staticmap.getStaticMap(pokemon['lat'], pokemon['lng'])

            part = email.MIMEBase.MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            email.encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            msg.attach(part)

            try:
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                server.login(username, password)
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                print("[!] PokeNotifier successfully sent notification email")
            except smtplib.SMTPException:
                print("[!] Error: PokeNotifier unable to send notification email")
