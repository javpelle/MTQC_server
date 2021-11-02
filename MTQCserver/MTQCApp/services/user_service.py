import logging
from random import randrange

from MTQCApp.commprotocol.server_response import AUTHORIZATION_DENIED, ERROR_SERVER, SUCCESS, USER_ALREADY_EXISTS, USER_ALREADY_VERIFIED, USER_NOT_VERIFIED, USER_PASS_INCORRECT, WRONG_JSON
from MTQCApp.models import User, Verification
from MTQCApp.serializers import UserSerializer
from MTQCApp.settings.settings import EMAIL_VERIFICATION_ENABLED
from . import security_service

logger = logging.getLogger(__name__)


def login(login_data):
    user_serializer = UserSerializer(data=login_data)
    if not user_serializer.is_valid():
        return {"status": WRONG_JSON}
    try:
        user = User.objects.get(
            email=login_data['email'], password=login_data['password'])
    except User.DoesNotExist:
        return {"status": USER_PASS_INCORRECT}

    if not user.verified:
        return {"status": USER_NOT_VERIFIED}

    # If we have reached this point, the login is correct
    user.token = security_service.generate_token(user.password)
    logger.debug('User id: {0}. Token: {1}'.format(user.id, user.token))
    user.save()
    return {"status": SUCCESS, "token": user.token}


def guest_login():
    token = security_service.generate_token(str(randrange(100000, 999999)))

    user = User(token=token)
    user.save()
    return {"status": SUCCESS, "token": token}


def verify_account(token: str):
    try:
        verification = Verification.objects.get(token=token)
    except Verification.DoesNotExist:
        return {"status": ERROR_SERVER}

    if verification.verified:
        return {"status": USER_ALREADY_VERIFIED}

    verification.user.verified = True
    verification.verified = True
    verification.user.save()
    verification.save()
    return {"status": SUCCESS}


def register(register_data):
    register_data["verified"] = not EMAIL_VERIFICATION_ENABLED
    user_serializer = UserSerializer(data=register_data)
    if not user_serializer.is_valid():
        return {"status": WRONG_JSON}

    user_exists = True
    try:
        User.objects.get(email=register_data['email'])
    except User.DoesNotExist:
        user_exists = False

    if user_exists:
        return {"status": USER_ALREADY_EXISTS}

    user = user_serializer.save()

    if EMAIL_VERIFICATION_ENABLED:
        # Verification token + send email
        token = security_service.generate_token(str(randrange(100000, 999999)))
        verification = Verification(token=token, user=user)
        verification.save()

        # send email

    return {"status": SUCCESS, "verified": not EMAIL_VERIFICATION_ENABLED}


def change_password(pass_data, user_token):
    try:
        current_pass = pass_data["current_password"]
        new_pass = pass_data["new_password"]
    except KeyError:
        return {"status": WRONG_JSON}

    try:
        user = User.objects.get(
            token=user_token)
    except User.DoesNotExist:
        return {"status": AUTHORIZATION_DENIED}

    if user.password != current_pass:
        return {"status": USER_PASS_INCORRECT}

    user.password = new_pass
    user.token = security_service.generate_token(user.password)
    user.save()
    return {"status": SUCCESS, "token": user.token}


def get_user_from_auth(auth: str):
    try:
        user = User.objects.get(
            token=auth)
    except User.DoesNotExist:
        return {"status": AUTHORIZATION_DENIED}

    return {"status": SUCCESS, "user": user}
