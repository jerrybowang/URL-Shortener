import hashlib
import base64
import datetime
from sqlalchemy.orm import Session

from app.DB.models import URL


def hash_64(string: str) -> str:
    """
    Return a 64 characters of sha256 hexdigest string
    """
    return hashlib.sha256(string.encode()).hexdigest()


def generate_key(url: str, salt: str = "") -> str:
    # Combine salt and URL
    raw = (salt + url).encode("utf-8")

    # Cryptographic hash
    h = hashlib.sha256(raw).digest()

    # Take first few bytes, encode to short, URL-safe form
    short = base64.urlsafe_b64encode(h[:8]).decode("utf-8").rstrip("=")
    return short


def add_entry_to_db(long_url: str, db: Session, slat: str = "") -> str:
    """
    Add an URL entry to DB with auto generated hashed key
    """
    long_url_hash = hash_64(long_url)
    key = generate_key(long_url)

    while db.query(URL).filter(URL.short_key == key).first():
        slat += "_"
        key = generate_key(long_url, slat)

    # add this entry to db
    new_entry = URL(short_key=key, long_url_hash=long_url_hash, long_url=long_url)
    db.add(new_entry)
    db.commit()

    return key


def set_entry_to_db(
    long_url: str, db: Session, key: str, user_id: str, overwrite: bool
):
    """
    Add or update an entry to DB by the key given
    """
    if overwrite:
        entry = db.query(URL).filter(URL.short_key == key).first()
        if not entry:
            raise ValueError("entry not found when overwrite set to true")
        entry.long_url = long_url
        entry.long_url_hash = hash_64(long_url)
        entry.created_at = datetime.datetime.now(datetime.timezone.utc)

        db.commit()
        db.refresh(entry)
    else:
        new_entry = URL(
            short_key=key,
            long_url_hash=hash_64(long_url),
            long_url=long_url,
            user=user_id,
        )
        db.add(new_entry)
        db.commit()
