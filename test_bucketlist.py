import unittest
import os
import json
from IPython import embed

class BucketlistTestCase(unittest.TestCase):

     def setUp(self):
         self.app = create_app(config_name="testing")
         self.client = self.app.test_client
         self.buckelist = {'name' : 'dfd'}

     def test_food_info(arg):
        res = self.client().post('/food_info/cheeseburger?size=small')
        embed()
