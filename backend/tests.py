from django.test import TestCase

from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.utils import timezone
import datetime

from django.template.loader import get_template
from django.template import Context



from mindojopolicy.settings import (
    EMAIL_HOST,
    MINDOJO_EMAIL_SENDER,
    MINDOJO_REPETITION_REVIEW_DAYS,
    MINDOJO_HANDBOOK_REVIEW_DAYS,
    BASE_DIR
)

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

class EmailTestCase(TestCase):
    def setUp(self):
        print("testsetup")

    def test_mailTemplate(self):
        print("[Test mail template]")
        plainText = get_template('testmail.txt')
        username = 'Snow white'
        d = {'username': username, "text": "How are you"}
        text_content = plainText.render(d)
        print(text_content)
    def test_email(self):
        print("test")
        try:
            subject = "Test  Email"
            plainText = get_template('testmail.html')
            username = 'Snow white'
            d = {'username': username, "text": "How are you"}
            message = plainText.render(d)
            
            msg = EmailMessage( subject, message, MINDOJO_EMAIL_SENDER, ["user['email']"])
            msg.content_subtype = "html"
            msg.send()
            print("[test]--> sent email")
        except Exception as e:
            print("[test]-->failed email")
            print("[Error]", e)

