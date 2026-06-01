

def test_hash_password_uses_scrypt_not_md5():
    import hashlib
    import re

    password = 'testpassword123'
    result = hash_password(password)

    # MD5 hex digest is always exactly 32 hex characters
    assert len(result) != 32, 'Hash length matches MD5 — likely still using MD5'

    # Ensure two calls with the same password produce different hashes (salting)
    result2 = hash_password(password)
    assert result != result2, 'Identical passwords produce identical hashes — no salt being used'

    # Ensure it is not the MD5 of the password
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    assert result != md5_hash, 'Hash matches MD5 output — vulnerability not fixed'

    # Verify the output is a valid hex string (scrypt output encoded as hex)
    assert re.fullmatch(r'[0-9a-f]+', result), 'Output is not a valid hex string'

    # scrypt with 16-byte salt + 64-byte default key = 80 bytes = 160 hex chars
    assert len(result) > 32, 'Hash is unexpectedly short for a scrypt-based output'