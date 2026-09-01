from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext

# ఇది secret key — production లో environment variable లో పెట్టాలి, ఇక్కడ demo కోసం direct గా పెడుతున్నాం
SECRET_KEY = "phantomweave-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """యూజర్ ఇచ్చిన password, database లో save అయిన hashed password తో match అవుతుందో చెక్ చేస్తుంది."""
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Plain text password ని hash చేస్తుంది — ఎప్పుడూ plain password database లో save చేయకూడదు."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Login సక్సెస్ అయ్యాక, ఈ JWT token క్రియేట్ చేసి యూజర్‌కి ఇస్తాం."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    """Token సరైనదో, expire అవ్వలేదో చెక్ చేస్తుంది."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None