import unittest
from app import app


class Exercise05FlaskSecurityTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Exercise 05 Docker security lab", response.get_data(as_text=True))

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "healthy"})


if __name__ == "__main__":
    unittest.main()
