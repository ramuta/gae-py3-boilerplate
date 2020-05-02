from flask import request, redirect, url_for, abort

from models.user import User
from utils.decorators import login_required, set_csrf, validate_csrf
from utils.translations import render_template_with_translations


@login_required
def my_details(**params):
    if request.method == "GET":
        return render_template_with_translations("profile/main/my_details.html", **params)


@login_required
@set_csrf
def edit_profile_get(**params):
    return render_template_with_translations("profile/main/edit_profile.html", **params)


@login_required
@validate_csrf
def edit_profile_post(**params):
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")

    user = params["user"]

    success, result = User.edit(user=user, first_name=first_name, last_name=last_name)

    if success:
        return redirect(url_for("profile.main.my_details"))
    else:
        return abort(403, description=result)


@login_required
def change_email_get(**params):
    if request.method == "GET":
        return render_template_with_translations("profile/main/my_details.html", **params)
