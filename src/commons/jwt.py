import datetime

import jwt
from django.conf import settings

JWT_KEY = getattr(settings, "JWT_KEY")
JWT_EXP = getattr(settings, "JWT_EXP")


class Jwt:
    @staticmethod
    def generate(key, algorithm="HS256", exp=None, **claims):
        """
        Generate a jwt token based on provided claims.

        Args:
            key (str, required): secret key.
            algorithm (str, required): algorithm.
            exp (int, optional): seconds to expire token.

        Returns:
            str
        """
        now = datetime.datetime.utcnow()
        claims["iat"] = now

        if exp is not None:
            claims["exp"] = now + datetime.timedelta(seconds=exp)
        return jwt.encode(claims, key, algorithm)

    @staticmethod
    def verify(token, key, algorithm="HS256"):
        try:
            claims = jwt.decode(token, key, algorithms=[algorithm])

        except (jwt.DecodeError, jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
            return None

        else:
            return claims
