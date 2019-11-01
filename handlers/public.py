from utils.decorators import public_handler
from utils.translations import render_template_with_translations


@public_handler
def index(**params):
    return render_template_with_translations("public/index.html", **params)
