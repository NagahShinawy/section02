from typing import Dict, Union
from db import db
from flask import request, url_for
import os
from libs.mailgun import Mailgun


UserJSON = Dict[str, Union[int, str]]

FROM_TITLE = "Stores Rest APi"
FROM_EMAIL = os.environ.get("FROM_EMAIL")
API_KEY = os.environ.get("API_KEY")
MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    activated = db.Column(db.Boolean, default=False)

    def json(self) -> UserJSON:
        return {"id": self.id, "username": self.username}

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def send_email_confirmation(self):
        # http://127.0.0.1:PORT + url_for ===>  http://127.0.0.1:PORT/user_confirm/1
        # userconfirm: is resource name
        link = request.url_root[:-1] + url_for("userconfirm", user_id=self.id)
        # hyper_link = f"<a href='{link}'>click to confirm</a>"
        with open("templates/confirmation_email_body.html", "r") as html:
            body = html.read().format(
                confirmation_endpoint=link, confirmation_text="Click to Confirm"
            )
        # html = f'<html><a href="{link}">Confirm you email</a></html>'
        html = f"<html>Please click the link to confirm your registration: <a href={link}>link</a></html>"
        Mailgun.send_email(
            emails=[self.email],
            subject="Email Confirmation",
            text="Please Confirm your email",
            html=html,
        )
