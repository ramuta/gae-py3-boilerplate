from flask import request, url_for
from werkzeug.utils import redirect

from models.user import User
from utils.decorators import login_required, set_csrf, validate_csrf
from utils.translations import render_template_with_translations


@login_required
@set_csrf
def sessions_list(**params):
    if request.method == "GET":
        return render_template_with_translations("profile/sessions/sessions_list.html", **params)


@login_required
@validate_csrf
def session_delete(**params):
    if request.method == "POST":
        token_hash_five_chars = request.form.get("delete-session-token")
        User.delete_session(user=params["user"], token_hash_five_chars=token_hash_five_chars)

        return redirect(url_for("profile.sessions.sessions_list"))
