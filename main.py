from flask import Flask
from handlers.public import main, auth
from utils.check_environment import is_local

app = Flask(__name__)

# PUBLIC URLS
app.add_url_rule(rule="/", endpoint="public.main.index", view_func=main.index, methods=["GET"])

# AUTH URLS
app.add_url_rule(rule="/init", endpoint="public.auth.init", view_func=auth.init, methods=["GET", "POST"])
app.add_url_rule(rule="/registration", endpoint="public.auth.registration", view_func=auth.registration, methods=["GET"])

if __name__ == '__main__':
    if is_local():
        app.run(port=8080, host="localhost", debug=True)  # localhost
    else:
        app.run()  # production
