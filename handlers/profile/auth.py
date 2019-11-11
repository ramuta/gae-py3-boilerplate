import hashlib

from models.user import User
from utils.check_environment import is_local
from utils.decorators import login_required
from flask import request, make_response, redirect, url_for


@login_required
def logout(**params):
    # logout should accept POST only (don't do logout via GET, to avoid pre-fetching issues in browsers)
    if request.method == "POST":
        # get the session token from the cookie
        session_token = request.cookies.get("my-web-app-session")

        # get the hash of the session token
        token_hash = hashlib.sha256(str.encode(session_token)).hexdigest()

        # delete the session token from the User object
        User.delete_session(user=params["user"], token_hash_five_chars=token_hash[:5])

        # prepare the response
        response = make_response(redirect(url_for("public.main.index")))

        # on localhost don't make the cookie secure and http-only (but on production it should be)
        cookie_secure_httponly = False
        if not is_local():
            cookie_secure_httponly = True

        # set the session cookie to an empty value (similar to deleting the cookie)
        response.set_cookie(key="my-web-app-session", value="", secure=cookie_secure_httponly,
                            httponly=cookie_secure_httponly)
        return response
