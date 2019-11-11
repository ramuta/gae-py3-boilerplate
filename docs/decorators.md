# Decorators

Decorators reside in `utils/decorators.py`.

There are two types of decorators in that file:

- CSRF decorators
- Authorization decorators

## CSRF decorators

The two CSRF decorators take care of supplying a CSRF token into an HTML template with a form and then validating the 
CSRF token.

CSRF tokens are needed for all HTML templates that have forms and where users need to be logged in.

CSRF tokens are not required for publicly accessible web pages.

How to apply this decorator to a handler:

```python

@login_required
@set_csrf
def profile_page(**params):
    if request.method == "GET":
        return render_template("profile.html", **params)


@login_required
@validate_csrf
def change_password(**params):
    if request.method == "POST":
        # ... code that changes password ...

        return redirect(url_for("profile"))

```

As you can see, in order to place a CSRF token into the HTML template, you need to use the `@set_csrf` decorator. In 
order to validate the CSRF token (received from the HTML template inside the form), you need to use the `@validate_csrf` 
decorator.

**Important:** Note that both decorators must be placed **below** the authorization decorator (in this case 
`@login_required`), because they depend on the user object that the authorization decorator creates and stores in 
`params`.

## Authorization decorators

The starter template has three authorization decorators:

- `@public_handler`
- `@login_required`
- `@admin_required`

### `@public_handler`

Public handler decorator checks for whether a page visitor has a session token stored in a cookie. If it has, it tries 
to log the user in. No matter if it succeeds or fails, the website visitor will be able to see the web page in the end. 
This decorators is meant to be used on all **publicly accessible websites.**

### `@login_required`

This decorator is meant to **protect** the web pages meant only for registered users - more precisely, users that have 
verified their email address and are not marked as suspended or deleted.

Whoever does not meet the criteria, is redirected to the login page or shown an error page.

### `@admin_required`

This decorator verifies if the user is admin or not and makes sure only admins can access the web page.

### The User object in params

Note that all of the above decorators store the User object (if the user is logged in) in `params`. You can access the 
user object in every decorated handler like this:

```python

user = params["user"]

```
