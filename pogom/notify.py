import email
import smtplib
import pytz
import time
from tzlocal import get_localzone

import staticmap


class PokeNotifier(object):
    def __init__(self, username, password):
        self.pokeset = set()
        self.username = username
        self.password = password

    def notify(self, pokemon, pokename, disappear_time):
        pokehash = str(pokemon['pokemon_data']['pokemon_id']) + str(pokemon['latitude']) + str(pokemon['longitude'])

        if pokehash in self.pokeset:
            print('[!] Notification already sent for this Pokemon! Skipping...')
            return

        self.pokeset.add(pokehash)

        username, password = self.username, self.password

        fromaddr = username
        toaddrs = ['YOUR_EMAIL_ADDRESS']

        for toaddr in toaddrs:
            msg = email.MIMEMultipart.MIMEMultipart()

            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "[Pokebot] Pokemon Located! - %s" % pokename

            disappear_time = disappear_time.replace(tzinfo=pytz.utc).astimezone(get_localzone())
            disappear_time_string = time.strftime('%Y-%m-%d %H:%M:%S', disappear_time.timetuple())

            body = '\r\n'.join(("Pokemon Name: %s" % pokename,
                                "Disappears at: %s" % disappear_time_string,
                                "", ""))

            msg.attach(email.MIMEText.MIMEText(body, 'plain'))

            filename = "pokemap.png"
            attachment = staticmap.getStaticMap(pokemon['latitude'], pokemon['longitude'])

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
