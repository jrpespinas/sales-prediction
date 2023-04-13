import json
from locust import HttpUser, task, between
from app.domain.store import StoreSchema


class PerformanceTests(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def test_predict(self):
        sample = StoreSchema(
            Store=1111,
            DayOfWeek=4,
            Date="2014-07-10",
            Customers=410,
            Open=1,
            Promo=0,
            StateHoliday="0",
            SchoolHoliday=1
        )
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.client.post(
            "predict",
            data=json.dumps(sample.dict()),
            headers=headers
        )
