
from typing import Any
from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_to_rub


@pytest.fixture
def usd_transaction() -> dict[str, Any]:
    return {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"},
        }
    }


def test_convert_rub_without_api_request() -> None:
    transaction = {
        "operationAmount": {
            "amount": "1500.50",
            "currency": {"code": "RUB"},
        }
    }

    with patch("src.external_api.requests.get") as mock_get:
        result = convert_to_rub(transaction)

    assert result == 1500.50
    mock_get.assert_not_called()


def test_convert_usd_to_rub(usd_transaction: dict[str, Any]) -> None:
    mock_response = Mock()
    mock_response.json.return_value = {"result": 9000.0}
    mock_response.raise_for_status.return_value = None

    with (
        patch("src.external_api.API_KEY", "test-api-key"),
        patch(
            "src.external_api.requests.get",
            return_value=mock_response,
        ) as mock_get,
    ):
        result = convert_to_rub(usd_transaction)

    assert result == 9000.0
    mock_get.assert_called_once()

    call_kwargs = mock_get.call_args.kwargs
    assert call_kwargs["params"] == {
        "from": "USD",
        "to": "RUB",
        "amount": 100.0,
    }
    assert call_kwargs["headers"] == {"apikey": "test-api-key"}


def test_convert_without_api_key(
    usd_transaction: dict[str, Any],
) -> None:
    with patch("src.external_api.API_KEY", None):
        with pytest.raises(ValueError, match="EXCHANGE_RATES_API_KEY"):
            convert_to_rub(usd_transaction)


def test_convert_api_error(
    usd_transaction: dict[str, Any],
) -> None:
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = (
        __import__("requests").HTTPError("API error")
    )

    with (
        patch("src.external_api.API_KEY", "test-api-key"),
        patch(
            "src.external_api.requests.get",
            return_value=mock_response,
        ),
        pytest.raises(__import__("requests").HTTPError),
    ):
        convert_to_rub(usd_transaction)
