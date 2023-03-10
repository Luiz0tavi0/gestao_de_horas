
import hashlib
import random

from flask import Blueprint, request, jsonify, redirect, url_for, make_response, current_app, render_template

from src.utils.email_holder import send_template_email


class AccountDefaultHookSet(object):

    def send_invitation_email(self, to, ctx):
        subject = render_template(
            "account/email/invite_user_subject.txt", ctx)
        message = render_template("account/email/invite_user.txt", ctx)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)

    def send_confirmation_email(self, to, ctx):
        subject = render_template(
            "account/email/email_confirmation_subject.txt", ctx)
        # remove superfluous line breaks
        subject = "".join(subject.splitlines())
        message = render_template(
            "account/email/email_confirmation_message.txt", ctx)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)

    def send_password_change_email(self, to, ctx):
        subject = render_template(
            "account/email/password_change_subject.txt", ctx)
        subject = "".join(subject.splitlines())
        message = render_template("account/email/password_change.txt", ctx)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)

    def send_password_reset_email(self, to, ctx):
        subject = render_template(
            "account/email/password_reset_subject.txt", ctx)
        subject = "".join(subject.splitlines())
        message = render_template("account/email/password_reset.txt", ctx)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)

    def generate_random_token(self, extra=None, hash_func=hashlib.sha256):
        if extra is None:
            extra = []
        bits = extra + [str(random.SystemRandom().getrandbits(512))]
        return hash_func("".join(bits).encode("utf-8")).hexdigest()

    def generate_signup_code_token(self, email=None):
        extra = []
        if email:
            extra.append(email)
        return self.generate_random_token(extra)

    def generate_email_confirmation_token(self, email):
        return self.generate_random_token([email])

    def get_user_credentials(self, form, identifier_field):
        return {
            "username": form.cleaned_data[identifier_field],
            "password": form.cleaned_data["password"],
        }


class HookProxy(object):

    def __getattr__(self, attr):
        return getattr(settings.ACCOUNT_HOOKSET, attr)


hookset = HookProxy()
