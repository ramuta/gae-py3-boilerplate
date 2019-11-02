from flask import redirect, url_for, request, abort

from models.app_settings import AppSettings
from models.user import User
from utils.decorators import public_handler
from utils.translations import render_template_with_translations


@public_handler
def init(**params):
    """Initialize the web app if there's no admin user yet. This is only needed once."""

    # find a user with admin privileges - if such user exists, the web app is already initialized
    if User.is_there_any_admin():
        return "The web app has already been initialized. <a href='/'>Return back to index</a>."

    # else proceed with initialization
    if request.method == "GET":
        params["app_settings"] = AppSettings.get()
        return render_template_with_translations("public/auth/init.html", **params)

    elif request.method == "POST":
        sendgrid_api_key = request.form.get("init-sendgrid")
        username = request.form.get("init-username")
        email_address = request.form.get("init-email")
        password = request.form.get("init-password")
        repeat = request.form.get("init-repeat")

        if username and password and password == repeat:
            User.create(username=username, email_address=email_address, password=password, admin=True)

            if sendgrid_api_key:
                AppSettings.update(sendgrid_api_key=sendgrid_api_key)

            return render_template_with_translations("public/auth/init_success.html", **params)
        else:
            return abort(403, description="There was something wrong. Maybe your passwords didn't match.")


@public_handler
def registration(**params):
    params["app_settings"] = AppSettings.get()
    return render_template_with_translations("public/auth/registration.html", **params)
