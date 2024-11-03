# Create your tests here.
from decimal import Decimal

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


def test_calc_더하기(client):
    res = client.post(
        "/calc",
        data={
            "input_a": "1",
            "input_b": "2",
            "operator": "+",
        },
    )

    result = res.data["result"]

    assert Decimal(result) == Decimal(3)


def test_calc_빼기(client):
    res = client.post(
        "/calc",
        data={
            "input_a": "1",
            "input_b": "2",
            "operator": "-",
        },
    )

    result = res.data["result"]

    assert Decimal(result) == Decimal(-1)


def test_calc_나누기(client):
    res = client.post(
        "/calc",
        data={
            "input_a": "18",
            "input_b": "3",
            "operator": "/",
        },
    )

    result = res.data["result"]

    assert Decimal(result) == Decimal(6)


def test_calc_곱하기(client):
    res = client.post(
        "/calc",
        data={
            "input_a": "5",
            "input_b": "4",
            "operator": "*",
        },
    )

    result = res.data["result"]

    assert Decimal(result) == Decimal(20)
