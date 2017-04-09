#-*- coding: utf-8 -*-

#from django.test import TestCase

from django.test import TestCase
from exchange.forms import SignUpForm, LoginForm, ResetForm, SubmitKey, ChangePassForm, DeleteKey, PasswordResetForm
from exchange.models import InvitationUrls, Keys, Profil, PasswordResetUrl, html_mail
from django.contrib.auth.models import User
from django.test import Client
from django.middleware.csrf import get_token


class InvitationTestCase(TestCase):
    """ Test the invitation system, include Login"""

    def setUp(self):
        self.c = Client()
        self.c = Client()

        self.user = User.objects.create_user(username='sender',
                                             password='totototo',
                                             email="sender@theserver.net")


        InvitationUrls.objects.create(name="toto", email="toto@gmail.com", sender_user=self.user)
        self.invitation = InvitationUrls.objects.get(name="toto" )

    def test_false_url_blocked(self):

        # With False URL
        url = "	AauROunLsvm1lDuQIYTxqVp2bCWMKfHY-/"
        invitation_page = self.c.get('/exchange/sign_up/' + url)
        self.assertNotEqual(invitation_page.status_code, 200)

    def test_false_email_blocked(self):
        # With False email
        data = {"username": "toto",
                "email": "false@pirate.com",
                "password": "totototo",
                "password_": "totototo"}
        invitation_form = SignUpForm(data, invitation=self.invitation)
        self.assertFalse(invitation_form.is_valid())

    def test_user_get_sign_in(self):
        """Test if the user can be create by sign_up view, login and redirect """

        url = self.invitation.url_uuid + "-/"
        invitation_page = self.c.get('/exchange/sign_up/' + url)

        self.assertEqual(invitation_page.status_code, 200)

    def test_user_post_sign_in(self):

        url = self.invitation.url_uuid + "-/"
        self.c.post('/exchange/sign_up/' + url, {"username": "toto",
                                                 "email": "toto@gmail.com",
                                                 "password": "totototo",
                                                 "password_": "totototo"})

        self.assertTrue(self.c.login(username="toto", password="totototo"))

    def test_email_fonction(self):
        t=html_mail("Test case", " I spam you", ["theguy@othertheserver.fr"])
        self.assertEqual(t, 1)


class LoginTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username='toto',
                                             password='totototo',
                                             email="toto@theserver.net")

        if Profil.objects:
            self.invitation = InvitationUrls.objects.create(
                email="toto@gmail.com", sender_user=self.user)
            self.profil = Profil(user=self.user, spec_url=self.invitation)

        self.password_reset_url = PasswordResetUrl(email="toto@theserver.net")
        self.password_reset_url.save()
    def test_login_get(self):
        """Login page exist."""
        login_page = self.c.get("/exchange/login/")
        self.assertEqual(login_page.status_code, 200)

    def test_login_form(self):
        """Test Login form authenticate"""
        data = {"username": "toto", "password": "totototo"}
        self.c.post("/exchange/login/", data)
        self.assertIn('_auth_user_id', self.c.session)

    def test_requesting_reset_pass(self):
        data = {"email": "toto@theserver.net"}
        self.c.post("/exchange/password_reset/", data)
        try:
            password_reset_url = PasswordResetUrl.objects.get(
                email="toto@theserver.net")
        except:
            password_reset_url = False
        self.assertIsNot(password_reset_url, False)

    def test_reset_pass_form_and_login(self):
        """ Reset password now post and login user after it with new password """


        data = {"email": "toto@theserver.net",
                "new_password": "totototonew",
                "password_": "totototonew" }
        form=PasswordResetForm(data, password_url=self.password_reset_url)
        url = self.password_reset_url.url_uuid + "-/"
        r=self.c.get("/exchange/do_reset_password_now/"+url)




        self.c.post("/exchange/do_reset_password_now/"+url , data)


        self.assertTrue(self.c.login(username='toto', password="totototonew"))

    def test_block_bad_email(self):
        data = {"email": "toto@theserver.net"}
        self.c.post("/exchange/password_reset/", data)
        password_reset_url = PasswordResetUrl.objects.get(
            email="toto@theserver.net")
        data = {"email": "toto@pirate.net",
                "new_password": "totototo_new",
                "password_": "totototo_new"}
        PasswordResetForm(data, password_url=password_reset_url)
        self.c.post("/exchange/do_reset_password_now/{}-/".format(
            password_reset_url.url_uuid), data)
        self.assertFalse(self.c.login(username='toto',
                                      password="totototo_new"))
