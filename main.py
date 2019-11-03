from flask import Flask

from handlers.admin import users
from handlers.public import main as public_main, auth
from handlers.profile import main as profile_main
from utils.check_environment import is_local

app = Flask(__name__)

# PUBLIC URLS
app.add_url_rule(rule="/", endpoint="public.main.index", view_func=public_main.index, methods=["GET"])

# PUBLIC auth
app.add_url_rule(rule="/init", endpoint="public.auth.init", view_func=auth.init, methods=["GET", "POST"])
app.add_url_rule(rule="/register", endpoint="public.auth.register", view_func=auth.register, methods=["GET", "POST"])
app.add_url_rule(rule="/login", endpoint="public.auth.login", view_func=auth.login, methods=["GET", "POST"])
app.add_url_rule(rule="/magic-login-token/<token>", view_func=auth.validate_magic_login_link, methods=["GET"])
app.add_url_rule(rule="/login-password", endpoint="public.auth.login_password", view_func=auth.login,
                 methods=["GET", "POST"])


# PROFILE URLS
app.add_url_rule(rule="/profile", endpoint="profile.main.sessions_list", view_func=profile_main.sessions_list,
                 methods=["GET"])
app.add_url_rule(rule="/profile/session/delete", endpoint="profile.main.session_delete",
                 view_func=profile_main.session_delete, methods=["POST"])


# ADMIN URLS
app.add_url_rule(rule="/admin/users", endpoint="admin.users.users_list", view_func=users.users_list, methods=["GET"])
app.add_url_rule(rule="/admin/user/<user_id>", endpoint="admin.users.user_details", view_func=users.user_details,
                 methods=["GET"])

if __name__ == '__main__':
    if is_local():
        app.run(port=8080, host="localhost", debug=True)  # localhost
    else:
        app.run(debug=False)  # production
