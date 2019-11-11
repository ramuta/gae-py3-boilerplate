# How to create and use handlers

> Some people call handlers "controllers" or even "views". Here, we'll refer to them as handlers.

Even though Flask is used in this starter template, the way the handlers (and also routes) are created is not usual 
in the Flask world.

Usually, a Flask handler looks like this:

```python

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return render_template("hello.html", name=name)

```

But in this template we separate routes from the handler functions. We keep URL routes in the `main.py` file and they 
look something like this:

```python

app.add_url_rule(rule="/", endpoint="hello", view_func=hello, methods=["GET"])

```

In addition, we wrap our handler functions with one of these decorators (defined in `utils/decorators.py`):

- `@public_handler`
- `@login_required`
- `@admin_required`

All of these handlers prepare a dictionary called `params` that holds all the variables sent from the backedn Python 
code to the HTML templates. A very common such variable is called `now` and it sends the current datetime info into 
all HTML files (this can be used, for example in the footer to get the current year).

Because the way `params` are used, we have to create handler functions like this:

```python
@public_handler
def hello(**params):
    params["name"] = "World"
    return render_template("hello.html", **params)
```

> You've probably noticed that `render_template_with_translations()` is used instead of `render_template()`. This is 
so we can enable [translations](/docs/translations.md), but if you don't want to use the translation system, you can 
use `render_template()` instead.

## Links:

- [Index](/README.md#documentation)
