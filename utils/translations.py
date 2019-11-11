from flask import render_template, request


def render_template_with_translations(path, **params):
    # Show templates from a language folder based on user's language choice.
    # This function can be improved with a check if the HTML file exists (and if it doesn't show for example the HTML
    # file in the English translations folder).

    lang = request.cookies.get("web-app-lang")

    if not lang:
        lang = "en"

    params["lang"] = lang
    return render_template("{0}/{1}".format(lang, path), **params)


def get_locale():
    # get the language that the user currently uses on the website
    lang = request.cookies.get("web-app-lang")

    if not lang:
        lang = "en"

    return lang
