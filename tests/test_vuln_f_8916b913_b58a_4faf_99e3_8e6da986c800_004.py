

def test_hash_password_security():
    import re

    # Test that hash_password_with_salt uses scrypt (output is not 32 hex chars of MD5)
    h1 = hash_password_with_salt('secret123')
    h2 = hash_password_with_salt('secret123')

    # MD5 hex digest is exactly 32 chars; scrypt output with salt prefix will be much longer
    assert len(h1) > 32, 'Hash is too short — likely still MD5'

    # Two hashes of the same password must differ (salt is random)
    assert h1 != h2, 'Same password produced identical hashes — salting is broken'

    # Must NOT be a plain MD5 hash
    md5_of_secret = hashlib.md5('secret123'.encode()).hexdigest()
    assert md5_of_secret not in h1, 'MD5 hash found in stored value'
    assert md5_of_secret not in h2, 'MD5 hash found in stored value'

    # Verify correct password matches
    stored = hash_password_with_salt('mypassword')
    assert verify_password('mypassword', stored), 'Correct password should verify'

    # Verify wrong password does not match
    assert not verify_password('wrongpassword', stored), 'Wrong password should not verify'