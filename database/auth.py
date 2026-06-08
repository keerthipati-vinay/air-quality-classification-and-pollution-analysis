from datetime import (
    datetime,
    timedelta
)

from jose import (
    JWTError,
    jwt
)

from passlib.context import (
    CryptContext
)

from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    OAuth2PasswordBearer
)

# PASSWORD HASHING

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# JWT SETTINGS

SECRET_KEY = (
    "air_quality_project_secret_key"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAUTH2

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

# HASH PASSWORD

def get_password_hash(
    password: str
):

    return pwd_context.hash(
        password
    )

# VERIFY PASSWORD

def verify_password(
    plain_password: str,
    hashed_password: str
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )

# CREATE JWT TOKEN

def create_access_token(
    data: dict
):

    to_encode = data.copy()

    expire = (
        datetime.utcnow()
        + timedelta(
            minutes=
            ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update(
        {
            "exp": expire
        }
    )

    encoded_jwt = jwt.encode(

        to_encode,

        SECRET_KEY,

        algorithm=ALGORITHM
    )

    return encoded_jwt

# VERIFY TOKEN

def verify_token(
    token: str
):

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[
                ALGORITHM
            ]
        )

        username = payload.get(
            "sub"
        )

        if username is None:

            raise HTTPException(

                status_code=
                status.HTTP_401_UNAUTHORIZED,

                detail=
                "Invalid Token"
            )

        return username

    except JWTError:

        raise HTTPException(

            status_code=
            status.HTTP_401_UNAUTHORIZED,

            detail=
            "Token Verification Failed"
        )

# CURRENT USER

def get_current_user(

    token: str = Depends(
        oauth2_scheme
    )
):

    return verify_token(
        token
    )
