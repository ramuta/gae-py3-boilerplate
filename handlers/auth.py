from flask import redirect, url_for, request

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
        return render_template_with_translations("auth/init.html", **params)
    elif request.method == "POST":
        pass


@public_handler
def registration(**params):
    params["app_settings"] = AppSettings.get()
    return render_template_with_translations("auth/registration.html", **params)
