import os
import pizza
import unittest
import tempfile

class PizzaViewTestCases(unittest.TestCase):
    def setUp(self):
        self.db_fd, pizza.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = pizza.app.test_client()
        pizza.check_database()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(pizza.app.config['DATABASE'])

    def test_welcome_view(self):
        rv = self.app.get("/", follow_redirects=True)
        assert "Start Pizza Session" in rv.data
        assert "Join Session" in rv.data

if __name__ == "__main__":
    unittest.main()
