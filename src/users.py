import os
import json
import hashlib
from datetime import datetime

BASE = os.path.join(os.getcwd(), 'data', 'users')
os.makedirs(BASE, exist_ok=True)


def _user_file(username):
    safe = username.replace('/', '_')
    return os.path.join(BASE, f"{safe}.json")


def hash_password(password: str, salt: str = "careerforge") -> str:
    return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()


def create_user(username: str, email: str, password: str) -> bool:
    path = _user_file(username)
    if os.path.exists(path):
        return False
    data = {
        'username': username,
        'email': email,
        'password_hash': hash_password(password),
        'created_at': datetime.utcnow().isoformat(),
        'cvs': []
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True


def verify_user(username: str, password: str) -> bool:
    path = _user_file(username)
    if not os.path.exists(path):
        return False
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('password_hash') == hash_password(password)


def save_cv(username: str, resume_text: str, cover_text: str, metadata: dict = None):
    path = _user_file(username)
    if not os.path.exists(path):
        raise FileNotFoundError("User not found")
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    item = {
        'timestamp': datetime.utcnow().isoformat(),
        'resume': resume_text,
        'cover_letter': cover_text,
        'metadata': metadata or {}
    }
    data.setdefault('cvs', []).append(item)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_user_data(username: str):
    path = _user_file(username)
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
