from server.core.crypt import get_crypt


def test_hash_password_ok():
    # GIVEN
    pw = "123456"
    # WHEN
    crypt = get_crypt()
    pw_hash = crypt.hash_password(pw)
    # THEN
    assert pw_hash


def test_check_password_ok():
    crypt = get_crypt()

    # GIVEN
    pw = "123456"
    pw_hash = crypt.hash_password(pw)

    # WHEN
    res = crypt.check_password(pw, pw_hash)

    # THEN
    assert res is True


def test_check_password_false():
    crypt = get_crypt()

    # GIVEN
    pw = "123456"
    pw_hash = crypt.hash_password(pw)
    pw_ne = "987654"

    # WHEN
    res = crypt.check_password(pw_ne, pw_hash)

    # THEN
    assert res is False
