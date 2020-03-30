from flask import redirect, url_for

from models.user import User
from utils.check_environment import is_local


def load_fake_data():
    # handler to load fake data for localhost development usage only
    if is_local():
        result, user_1, message = User.create(email_address="user_{}@my.webapp".format(1), admin=False, first_name="Jim", last_name="Jones")
        result, user_2, message = User.create(email_address="user_{}@my.webapp".format(2), admin=True, first_name="Betty", last_name="Beam")
        result, user_3, message = User.create(email_address="user_{}@my.webapp".format(3), admin=False, first_name="Cindy", last_name="Crawford")
        result, user_4, message = User.create(email_address="user_{}@my.webapp".format(4), admin=False, first_name="Damian", last_name="Dante")
        result, user_5, message = User.create(email_address="user_{}@my.webapp".format(5), admin=False, first_name="Erica", last_name="Enter")
        result, user_6, message = User.create(email_address="user_{}@my.webapp".format(6), admin=False, first_name="Fatima", last_name="Fowles")
        result, user_7, message = User.create(email_address="user_{}@my.webapp".format(7), admin=False, first_name="George", last_name="Garrett")
        result, user_8, message = User.create(email_address="user_{}@my.webapp".format(8), admin=True, first_name="Harriet", last_name="Ham")
        result, user_9, message = User.create(email_address="user_{}@my.webapp".format(9), admin=False, first_name="Ian", last_name="Ilich")
        result, user_10, message = User.create(email_address="user_{}@my.webapp".format(10), admin=False, first_name="Jane", last_name="James")
        result, user_11, message = User.create(email_address="user_{}@my.webapp".format(11), admin=False, first_name="Ken", last_name="Klingon")
        result, user_12, message = User.create(email_address="user_{}@my.webapp".format(12), admin=False, first_name="Lana", last_name="Lubbards")
        result, user_13, message = User.create(email_address="user_{}@my.webapp".format(13), admin=False, first_name="Matt", last_name="Morata")
        result, user_14, message = User.create(email_address="user_{}@my.webapp".format(14), admin=False, first_name="Nika", last_name="Norante")
        result, user_15, message = User.create(email_address="user_{}@my.webapp".format(15), admin=False, first_name="Omar", last_name="Orange")
        result, user_16, message = User.create(email_address="user_{}@my.webapp".format(16), admin=False, first_name="Peter", last_name="Pan")

        # mark most of emails as verified
        User._test_mark_email_verified(user=user_1)
        User._test_mark_email_verified(user=user_2)
        User._test_mark_email_verified(user=user_3)
        User._test_mark_email_verified(user=user_4)
        User._test_mark_email_verified(user=user_5)
        User._test_mark_email_verified(user=user_6)
        User._test_mark_email_verified(user=user_7)
        User._test_mark_email_verified(user=user_8)
        User._test_mark_email_verified(user=user_9)
        User._test_mark_email_verified(user=user_10)
        User._test_mark_email_verified(user=user_11)
        User._test_mark_email_verified(user=user_13)
        User._test_mark_email_verified(user=user_14)
        User._test_mark_email_verified(user=user_16)

        User.delete_toggle(user=user_4)  # Delete Damian Dante
        User.suspend_toggle(user=user_4)  # Suspend Damian Dante

    return redirect(url_for("public.main.index"))
