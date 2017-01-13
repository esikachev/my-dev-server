from my_dev_server.server import exceptions

MINIMAL_PASSWORD_LEN = 5
MINIMAL_USERNAME_LEN = 2
MINIMAL_EMAIL_LEN = 4


def check_user_correct(username, email, password):

    if username and (len(username) <= MINIMAL_USERNAME_LEN):
        err_message = "Username len required > %s" % MINIMAL_USERNAME_LEN
        raise exceptions.LengthRequired(err_message)

    if email and (len(email) <= MINIMAL_EMAIL_LEN):
        err_message = "Email len required > %s" % MINIMAL_EMAIL_LEN
        raise exceptions.LengthRequired(err_message)

    if password and (len(password) <= MINIMAL_PASSWORD_LEN):
        err_message = "Password len required > %s" % MINIMAL_PASSWORD_LEN
        raise exceptions.LengthRequired(err_message)
