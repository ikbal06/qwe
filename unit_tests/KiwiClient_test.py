import unittest   # The test framework
from resources.kiwi.KiwiClient import KiwiClient
from resources.common.Logger import log
import datetime
import time
import json

now = datetime.datetime.now()


class TestKiwiClient(unittest.TestCase):

    def test_TestRun_create(self):
        """
        Test that it can sum a list of integers
        """
        kc = KiwiClient()
        response = kc.TestRun_create(7)
        self.assertGreater(response['result']['id'], 0)

    def test_case_id(kiwi_plan_id=9, spirent_test_id='KT_CN_001'):
        cases = KiwiClient.get_TestCase_by_plan_id(kiwi_plan_id).get('result', [])
        found_cases = [tc for tc in cases if tc['summary'] == spirent_test_id]
        tc = found_cases[0]
        tc_id = tc['id']
        return tc_id
