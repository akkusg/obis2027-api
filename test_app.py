import unittest

from app import app


class ApiTest(unittest.TestCase):
    def setUp(self):
        app.config.update(
            TESTING=True,
            SECRET_KEY="test-only-secret",
            API_USERNAME="student",
            API_PASSWORD="test-password",
        )
        self.client = app.test_client()

    def test_login_and_list_courses(self):
        response = self.client.post(
            "/api/login", json={"username": "student", "password": "test-password"}
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/api/list-courses")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["courses"][0]["code"], "MAT101")

    def test_courses_require_login(self):
        self.assertEqual(self.client.get("/api/list-courses").status_code, 401)

    def test_invalid_credentials(self):
        response = self.client.post(
            "/api/login", json={"username": "student", "password": "wrong"}
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(self.client.get("/api/list-courses").status_code, 401)

    def test_invalid_request(self):
        for data in (None, [], {}, {"username": "student", "password": 123}):
            with self.subTest(data=data):
                self.assertEqual(self.client.post("/api/login", json=data).status_code, 400)

    def test_missing_configuration(self):
        app.config["SECRET_KEY"] = None
        response = self.client.post(
            "/api/login", json={"username": "student", "password": "test-password"}
        )
        self.assertEqual(response.status_code, 503)


if __name__ == "__main__":
    unittest.main()
