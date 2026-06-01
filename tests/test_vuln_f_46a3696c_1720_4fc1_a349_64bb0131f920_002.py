

def test_hash_password_not_md5_and_has_salt():
    import re
    h1 = hash_password('secret123')
    h2 = hash_password('secret123')
    # MD5 hex digest is exactly 32 chars; scrypt output will be longer
    assert len(h1) != 32, 'Hash should not be MD5 length (32 hex chars)'
    # Two hashes of the same password must differ due to random salt
    assert h1 != h2, 'Hashes of the same password must differ (salted)'
    # Known MD5 of 'secret123' must not appear
    md5_of_secret123 = '5a4f9e7b18d2e1c3a6b0d8f7e2c4a1b9'
    actual_md5 = hashlib.md5('secret123'.encode()).hexdigest()
    assert h1 != actual_md5, 'Hash must not be a plain MD5'
    assert h2 != actual_md5, 'Hash must not be a plain MD5'
    # Output should be a valid hex string
    assert re.fullmatch(r'[0-9a-f]+', h1), 'Output should be a hex string'
