from flask import Flask
from handlers import public, auth
from utils.check_environment import is_local

app = Flask(__name__)

# PUBLIC URLS
app.add_url_rule(rule="/", endpoint="public.index", view_func=public.index, methods=["GET"])

# AUTH URLS
app.add_url_rule(rule="/init", endpoint="auth.init", view_func=auth.init, methods=["GET", "POST"])
app.add_url_rule(rule="/registration", endpoint="auth.registration", view_func=auth.registration, methods=["GET"])

if __name__ == '__main__':
    if is_local():
        app.run(port=8080, host="localhost", debug=True)  # localhost
    else:
        app.run()  # production
