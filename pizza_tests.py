import os
import pizza
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, pizza.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = flaskr.app.test_client()
        pizza.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(pizza.app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()
