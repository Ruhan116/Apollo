import pytest
from passlib.context import CryptContext


def test_argon2_hash_long_password():
    ctx = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
    long_pw = "P" * 300 + "aA1@"
    hashed = ctx.hash(long_pw, scheme="argon2")
    assert hashed.startswith("$argon2")
    assert ctx.verify(long_pw, hashed)


def test_needs_update_for_bcrypt_then_rehash():
    ctx = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
    # Use a sample bcrypt formatted hash string (avoid invoking bcrypt backend in test env)
    bcrypt_hash = "$2b$12$ABCDEFGHIJKLMNOPQRSTUVabcdefghijklmnopqrstuvABCD12345678"

    # Now confirm the argon2-preferred context considers it needs update
    assert ctx.needs_update(bcrypt_hash) is True

    # Rehash with argon2 and verify
    new_hash = ctx.hash("secretPW1", scheme="argon2")
    assert new_hash.startswith("$argon2")
    assert ctx.verify("secretPW1", new_hash)
