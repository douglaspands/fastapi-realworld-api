import pytest

from app.infra.types import validate_specific_dsn


def test_validate_specific_dsn_ok():
    # EXPECTED
    result_expected = "sqlite+aiosqlite:///test.db"

    # GIVEN
    uri = result_expected
    # WHEN
    result = validate_specific_dsn(uri)
    # THEN
    assert result_expected == result


def test_validate_specific_dsn_scheme_invalid():
    # GIVEN
    uri = "https://test.db"
    # WHEN
    with pytest.raises(ValueError) as exc_info:
        result = validate_specific_dsn(uri)

    # THEN
    assert "Unsupported database scheme" in str(exc_info.value)


def test_validate_specific_dsn_path_invalid():
    # GIVEN
    uri = "sqlite+aiosqlite:"
    # WHEN
    with pytest.raises(ValueError) as exc_info:
        result = validate_specific_dsn(uri)

    # THEN
    assert "Unsupported database host" in str(exc_info.value)
