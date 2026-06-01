

def test_hash_password_not_md5_and_is_slow():
    import time
    import hashlib

    password = 'secret123'
    result = hash_password(password)

    # Must not be MD5 (MD5 hex digest is always 32 chars)
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    assert result != md5_hash, 'hash_password must not return an MD5 hash'

    # Must not be a 32-char hex string (MD5 output length)
    assert len(result) != 32, 'Output length matches MD5 — likely still using MD5'

    # Must take measurable time (key-stretching)
    start = time.time()
    hash_password(password)
    elapsed = time.time() - start
    assert elapsed > 0.001, 'hash_password completed too fast — no key stretching detected'

    # Must produce a non-empty hex-like string
    assert len(result) > 0
    int(result, 16)  # raises ValueError if not valid hex