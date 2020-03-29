import json
from flask import request, redirect, url_for
from google.cloud.ndb import Cursor
from models.user import User
from utils.decorators import admin_required, set_csrf, validate_csrf
from utils.translations import render_template_with_translations


@admin_required
@validate_csrf
def user_delete(user_id, **params):
    selected_user = User.get_user_by_id(user_id)
    User.delete(user=selected_user)

    return redirect(url_for("admin.users.users_list"))


@admin_required
@set_csrf
def user_details(user_id, **params):
    params["selected_user"] = User.get_user_by_id(user_id)
    return render_template_with_translations("admin/users/details.html", **params)


@admin_required
@set_csrf
def user_edit_get(user_id, **params):
    params["selected_user"] = User.get_user_by_id(user_id)
    return render_template_with_translations("admin/users/edit.html", **params)


@admin_required
@validate_csrf
def user_edit_post(user_id, **params):
    selected_user = User.get_user_by_id(user_id)

    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")

    User.edit(user=selected_user, first_name=first_name, last_name=last_name)

    return redirect(url_for("admin.users.user_details", user_id=selected_user.get_id))


@admin_required
def users_list(**params):
    cursor_arg = request.args.get('cursor')

    if cursor_arg:
        cursor = Cursor(urlsafe=cursor_arg.encode())
    else:
        cursor = None

    params["users"], params["next_cursor"], params["more"] = User.fetch(limit=10, cursor=cursor)

    if not cursor_arg:
        # normal browser get request
        return render_template_with_translations("admin/users/list.html", **params)
    else:
        # get request via JavaScript script: admin-load-more-users.js
        users_dicts = []
        for user in params["users"]:
            users_dicts.append({"get_id": user.get_id, "email_address": user.email_address, "created": user.created,
                                "first_name": user.first_name, "last_name": user.last_name, "admin": user.admin})

        return json.dumps({"users": users_dicts, "next_cursor": params["next_cursor"], "more": params["more"]},
                          default=str)  # default=str helps to avoid issues with datetime (converts datetime to str)


@admin_required
def users_list_deleted(**params):
    cursor_arg = request.args.get('cursor')

    if cursor_arg:
        cursor = Cursor(urlsafe=cursor_arg.encode())
    else:
        cursor = None

    params["users"], params["next_cursor"], params["more"] = User.fetch(limit=10, cursor=cursor, deleted=True)

    if not cursor_arg:
        # normal browser get request
        return render_template_with_translations("admin/users/list_deleted.html", **params)
    else:
        # get request via JavaScript script: admin-load-more-users.js
        users_dicts = []
        for user in params["users"]:
            users_dicts.append({"get_id": user.get_id, "email_address": user.email_address, "created": user.created,
                                "first_name": user.first_name, "last_name": user.last_name, "admin": user.admin})

        return json.dumps({"users": users_dicts, "next_cursor": params["next_cursor"], "more": params["more"]},
                          default=str)  # default=str helps to avoid issues with datetime (converts datetime to str)
