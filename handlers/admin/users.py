import json
from flask import request
from google.cloud.ndb import Cursor
from models.user import User
from utils.decorators import admin_required
from utils.translations import render_template_with_translations


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
def user_details(user_id, **params):
    params["selected_user"] = User.get_user_by_id(user_id)
    return render_template_with_translations("admin/users/details.html", **params)
