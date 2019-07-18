import sys
import json
import unittest
from app import app

class BucketlistTestCase(unittest.TestCase):

     def setup(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

     def test_food_info(self):
        with app.test_request_context():
            out = output('error', 'Test Error', 'local_host')

        response = [
                  {
                         'type': 'error',
                         'message': 'Test Error',
                         'download_link': 'local_host'
                   }
                ]
        data = json.loads(out.get_data(as_text=True))
        
if __name__ == "__main__":
    unittest.main()
