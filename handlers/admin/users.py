from models.user import User
from utils.decorators import admin_required
from utils.translations import render_template_with_translations


@admin_required
def users_list(**params):
    params["users"] = User.fetch()
    return render_template_with_translations("admin/users/list.html", **params)


@admin_required
def user_details(user_id, **params):
    params["selected_user"] = User.get_user_by_id(user_id)
    return render_template_with_translations("admin/users/details.html", **params)
