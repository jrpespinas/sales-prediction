from fastapi.testclient import TestClient

from ...router.predict import router

client = TestClient(router)


def test_predict():
    response = client.post(
        "/predict",
        headers={"Content-Type": "application/json"},
        json={
            "Store":1111,
            "DayOfWeek":4,
            "Date":"2014-07-10",
            "Customers":410,
            "Open":1,
            "Promo":0,
            "StateHoliday":"0",
            "SchoolHoliday":1
        },
    )
    assert response.status_code == 200