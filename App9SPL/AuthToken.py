import jwt
from App9SPL.models import SystemUser
from django.conf import settings


def DecodeToken(token):

    Bearer = str(token)
    jwt_token = Bearer.replace("Bearer ", "")

    payload = jwt.decode(jwt_token, settings.SECRET_KEY,
                         algorithms="HS256")

    UserId = SystemUser.objects.get(id=payload["user_id"]).id

    return UserId
