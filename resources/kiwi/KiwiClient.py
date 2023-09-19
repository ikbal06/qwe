import http.client
import ssl
import json
import logging
import datetime

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
        self.conn = http.client.HTTPSConnection("kiwi-test.ulakhaberlesme.com.tr", context=ssl._create_unverified_context())
        self.SessionID = None
        
    def _login(self):
        
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
        self.conn.request("POST", "/json-rpc/", request_json, headers)
        login_response = self.conn.getresponse()
        login_data_binary = login_response.read()
        login_data_string = login_data_binary.decode("utf-8")
        login_response = json.loads(login_data_string)

        if login_response:
            self.SessionID = login_response["result"]
            print("Logged in: SessionID -", self.SessionID)
        else:
            print("kullanıcı bilgilerini kontrol et")
            return None
        
    def _send_request(self, method, params):
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
        
        request_json = json.dumps(request_body)
        self.conn.request("POST", "/json-rpc/", request_json, headers)
        response = self.conn.getresponse()
        data_json = json.loads(response.read().decode("utf-8"))
        return data_json
    
    def error(response):
        if "error" in response:
            hata_mesaji = "Hata cevabı alındı: [{}] {}".format(response["code"],response["error"])
            print(hata_mesaji)
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

    def testplan_filter(self, plan_id):
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
        print("test plan filter: ", response)

        if not response:
            print("testplan_filter failed.")
            return None
        
        return response
        
    def getTestCasePlanByID(self, plan_id):
        response = self._send_request("TestCase.filter", [{"plan__id": plan_id}])
        return response
        '''
         if response:
             if "result" in response:
                 print("getTestCasePlanByID:", response)
                 return response
             else:
                 print("getTestCasePlanByID response does not have 'result' key.")
         else:
             print("getTestCasePlanByID failed.")
         return None
        '''
    
    def create_testplan(self,product, product_version, name, type):
        test_plan = {
            "product": product,
            "product_version": product_version,
            "name": name,
            "type": type
        }
        response = self._send_request("TestPlan.create", test_plan)
        print("create test plan: ", response)
        if not response:
            print("cretae test plan failed.")
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
        
    def TestRun_add_case(self, run_id, case_id):
        payload = [run_id, case_id]
        response = self._send_request("TestRun.add_case", payload)
        print("TestRun_add_case:", response)
        if response:
            print("TestRun_add_case:", response)
            return response   
        
        if not response:
            print("testplan_filter failed.")
            return None
        else:
            self.error(response) 
            

    def testrun_create(self, plan_id):
        #test_plans = self.testplan_filter(plan_id)["result"]
        test_plans = self.testplan_filter(plan_id)
        tp = test_plans["result"][0]["name"]
        print("tp: ",tp)
        if len(tp)>0:
            plan_name = tp
        values = [{
           "build": 1,    # TODO: otomatik test koşusu için bir build yaratılacak. unspecified(name)	unspecified(version)	5G CN - Çınar(ürün)
           "manager": 3,  # TODO: otomatik koşular için bir kullanıcı tanımlanacak. test yöneticisi test ortamı için user 3 - b.ikbalkirklar@gmail.com
           "plan": plan_id,
           "summary": "{} Tarihinde '{}' Planı için koşu".format(now, plan_name)
        }]
        
        response = self._send_request("TestRun.create", values)
        print("run create: ", response)
        return response
    
    def TestExecution_update(self, case_execution_id, run_id, case_id, status_id):
        case_result = [case_execution_id, {
			"run": run_id,
			"case": case_id,
			"status": status_id
		} ]
        response = self._send_request("TestExecution.update",case_result)
        return response
    #status: 
    #4 geçti, 5 başarısız 
    
    def testrun_add_tag(self, run_id, tag_name):
        tag_values = [run_id, tag_name] 
        response = self._send_request("TestRun.add_tag", tag_values)
        print("tag response ", response)
        return response 

    def get_tags(self, file):
        if file == "":
            raise Exception('Dosya geçerli değil!')
        
        # Dosyayı açıp satırları bir liste içine alıyoruz
        with open(file) as f:
            tag_list = f.read().splitlines()
            return tag_list

