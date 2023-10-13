import http.client
import ssl
import json
import time
from resources.common.Logger import log
import datetime
import json

now = datetime.datetime.now()

# TODO: Log çıktısını verebilmeli
# https://realpython.com/python-logging/
# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
# logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class KiwiClient:
    ''' 
        # >>> id Bilgisi hatalı istek:
        # {
        # 	"jsonrpc":"2.0",
        # 	"method":"TestPlan.filter", 
        # 	"params":[{"is_active":true, "id":"a130"}],
        # 	"id":"jsonrpc"
        # }
        #
        # >>> Hatalı isteğin cevabı:
        # {
        # 	"id": "jsonrpc",
        # 	"jsonrpc": "2.0",
        # 	"error": {
        # 		"code": -32603,
        # 		"message": "Internal error: Field 'id' expected a number but got 'a130'."
        # 	}
        # }   
     '''

    def __init__(self):
        self.url = "https://kiwi-test.ulakhaberlesme.com.tr/json_rpc/"
        self.conn = None
        self.SessionID = None

    def _connect(self):
        self.conn = http.client.HTTPSConnection("kiwi-test.ulakhaberlesme.com.tr",
                                                context=ssl._create_unverified_context())

    def _login(self):
        if not self.conn:
            self._connect()

        request_body = {
            "jsonrpc": "2.0",
            "method": "Auth.login",
            "params": {
                "username": "admin.test",
                "password": "Test123456789"
            },
            "id": "jsonrpc"
        }

        headers = {
            'Content-Type': 'application/json'
        }
        request_json = json.dumps(request_body)
        try:
            self.conn.request("POST", "/json-rpc/", request_json, headers)
            login_response = self.conn.getresponse()
            login_data_binary = login_response.read()
            login_data_string = login_data_binary.decode("utf-8")
            login_response = json.loads(login_data_string)

            if login_response:
                self.SessionID = login_response["result"]
                log.debug("Logged in: SessionID -", self.SessionID)
            else:
                log.debug("kullanıcı bilgilerini kontrol et")
                return None
        except Exception as e:
            log.error('http isteğinde hata oldu', e)

    def _send_request(self, method, params):
        if not self.conn:
            self._connect()

        if self.SessionID is None:
            self._login()

        request_body = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": "jsonrpc"
        }

        headers = {
            'Content-Type': 'application/json',
            'Cookie': "sessionid=" + self.SessionID
        }
        try:
            b = self.conn.connect()
            request_json = json.dumps(request_body)
            a = self.conn.request("POST", "/json-rpc/", request_json, headers)
            time.sleep(1)
            response = self.conn.getresponse()
            if response.status == 200:
                response_content = response.read().decode("utf-8")
                data_json = json.loads(response_content)
                return data_json
            if response is None:
                log.error('http istek hatası kodu da: ', response.status)
        except Exception as e:
            print("HTTP Request Error:", e)
            return None

    def error(response):
        if "error" in response:
            hata_mesaji = "Hata cevabı alındı: [{}] {}".format(response["code"], response["error"])
            log.debug(hata_mesaji)
            return None

        return response

    '''
    --- Sıfırdan ----------------
    Test Planı yarat
    Test Case ekle
    Test Koşusu yarat
    Test Case ekle
    Test Execution güncelle
    -----------------------------
    -----------------------------

    --- Varolan planı koş (plan_id=137) -------
    Test planı için Test Koşusu yarat
    Test Planına ait case'leri çek
    execution_id = Her case'i koşuya ekle 
    Her execution_id için test case'in sonucu güncelle
    --- AYRINTISI ---------------
    https://kiwitcms.readthedocs.io/en/latest/modules/tcms.rpc.api.testrun.html
      >>> values = {
           'build': 384,
           'manager': 137,
           'plan': 137,
           'summary': 'Redmine#24 için test koşusu',
       }
       >>> TestRun.create(values)
    
     ----- Form üstünden verinin girişi -----
     csrfmiddlewaretoken: 5QULTorfhcX8alw55X5gjizt4JjEssqaRldEjiZd4nQvz72Hs8f5PdbxEI2NguH3
     summary: cem koşu redmine 36
     manager: b.ikbalkirklar@gmail.com
     default_tester: b.ikbalkirklar@gmail.com
     product: 1                    << 5G CN - ÇINAR
     plan: 4
     build: 1                      << unspecified
     planned_start: 2023-09-13
     planned_stop: 2023-09-14
     start_date: 
     stop_date: 
     notes: Bu test koşusu notları olacak
    
     -----------------------------
    '''

    def TestPlan_filter(self, plan_id):
        '''
        # planın ayrıntılarını dön
        # >>> istek:
        # {
        # 	"jsonrpc":"2.0",
        # 	"method":"TestPlan.filter", 
        # 	"params":[{"is_active":true, "id":3}],
        # 	"id":"jsonrpc"
        # }
        #
        # >>> cevap:
        # {
        # 	"id": "jsonrpc",
        # 	"jsonrpc": "2.0",
        # 	"result": [
        # 		{
        # 			"id": 3,
        # 			"name": "redmine#24",
        # 			"text": "",
        # 			"create_date": "2023-09-08T12:11:07.731",
        # 			"is_active": true,
        # 			"extra_link": null,
        # 			"product_version": 5,
        # 			"product_version__value": "unspecified",
        # 			"product": 3,
        # 			"product__name": "6G",
        # 			"author": 3,
        # 			"author__username": "ikbal",
        # 			"type": 5,
        # 			"type__name": "Acceptance",
        # 			"parent": null,
        # 			"children__count": 0
        # 		}
        # 	]
        # }
        '''

        response = self._send_request("TestPlan.filter", [{"id": plan_id}])
        log.debug(f"test plan filter: {response}")

        if not response:
            log.debug("testplan_filter failed.")
            return None

        return response

    def get_TestCase_by_plan_id(self, plan_id):
        try:
            response = self._send_request("TestCase.filter", [{"plan__id": plan_id}])
            return response
        except Exception as e:
            log.debug('test case leri filtrelerken hata çıkmış olmalı')
        '''
         if response:
             if "result" in response:
                 log.debug("getTestCasePlanByID:", response)
                 return response
             else:
                 log.debug("getTestCasePlanByID response does not have 'result' key.")
         else:
             log.debug("getTestCasePlanByID failed.")
         return None
        '''

    def TestPlan_create(self, product, product_version, name, type):
        test_plan = {
            "product": product,
            "product_version": product_version,
            "name": name,
            "type": type
        }
        response = self._send_request("TestPlan.create", test_plan)
        log.debug(f"create test plan response: {response}")
        if not response:
            log.warning("cretae test plan failed.")
            return None
        else:
            self.error(response)
    '''
        #types:  - geri kalan her şey den buraya gelince ekleme yapılabiliyor    
        # 1	Unit	
        # 2	Integration	
        # 3	Function	
        # 4	System	
        # 5	Acceptance	
        # 6	Installation	
        # 7	Performance	
        # 8	Product	
        # 9	Interoperability	
        # 10	Smoke	
        # 11	Regression
        
        #products (test ortamı için)
        # ID Name Classification Description
        # 1	5G CN - Çınar	5G CN	
        # 3	6G	CN	
        # 2	ÇINAR_5G_CN	5G CN'''

    def TestRun_create(self, plan_id):
        # test_plans = self.testplan_filter(plan_id)["result"]
        log.debug(f"Test plan will be found for : {plan_id}")
        # test_plans = self.TestPlan_filter(plan_id).get('result', [])
        # TODO : result boş gelebilir kontrol yapılacak

        test_plans = self.TestPlan_filter(plan_id)
        result = test_plans.get('result', [])

        if not result:
            log.debug('test planı ile ilgili result boş geldi')

        if len(result) != 1:
            log.warning("Test plan could not be found")
            return None

        tp = result[0]
        log.debug(f"Found Test Plan: {tp}")
        plan_name = tp["name"]
        values = [{
            # TODO: otomatik test koşusu için bir build yaratılacak. unspecified(name)	unspecified(version) product-1:	5G CN - Çınar(ürün)
            "build": 2,
            "manager": 3,  # TODO: otomatik koşular için bir kullanıcı tanımlanacak. test yöneticisi test ortamı için user 3 - b.ikbalkirklar@gmail.com
            "plan": plan_id,
            "summary": f"{now} Tarihinde '{plan_name}' Planı için koşu"
        }]

        response = self._send_request("TestRun.create", values)
        log.debug(f'Test Run create response: {response}')
        return response

    def TestRun_add_case(self, run_id, case_id):
        '''
        bir test koşusuna test senaryosunu ekler. ekleme sonucunda test execution nesnesini içeren http cevabını döner.
        '''
        payload = [run_id, case_id]

        log.debug(f"payload: {payload}")
        try:
            response = self._send_request("TestRun.add_case", payload)
        except Exception as e:
            log.error(f'Error={e}')
            raise e

        log.debug(f"TestRun_add_case: {response}")

        if not response:
            log.error(f"TestRun_add_case sonucu bos geldi: {response}")
            return None

        if len(response['result']) == 0:
            log.warning("Adding test case into test plan failed.")
            return None

        log.info(f"TestRun_add_case: {response}")
        return response

    def TestExecution_update(self, case_execution_id, run_id, case_id, status_id):
        case_result = [case_execution_id, {
            "run": run_id,
            "case": case_id,
            "status": status_id
        }]
        response = self._send_request("TestExecution.update", case_result)
        return response
    # status:
    # 4 geçti, 5 başarısız

    def TestRun_add_tag(self, run_id, tag_name):
        tag_values = [run_id, tag_name]
        response = self._send_request("TestRun.add_tag", tag_values)
        log.debug(f"tag response : {response}")
        return response

    def TestExecution_add_comment(self, execution_id, comment):
        # we always create only one comment
        add_comment = [execution_id, comment]
        response = self._send_request("TestExecution.add_comment", add_comment)
        return response
