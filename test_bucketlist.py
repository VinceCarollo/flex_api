import unittest
import os
import json
from app import app

class BucketlistTestCase(unittest.TestCase):

     def setUp(self):
         self.app = app
         self.client = self.app.test_client
         self.buckelist = {'name' : 'dfd'}

     def test_food_info(self):
        res = self.client().post('/food_info/cheeseburger/?size=small')
        import code; code.interact(local=dict(globals(), **locals()))
        self.assertEqual(res.status_code, 200)

if __name__ == "__main__":
    unittest.main()
