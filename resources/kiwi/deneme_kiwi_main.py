import KiwiClient as KiwiClient


if __name__ == '__main__':
    kiwiClient = KiwiClient()
    plan_id=7
    status_id=4
    product_id=1
    product_version_id=1.0
    test_type=1
    
    # Test planı için bir test koşusu yaratıyoruz
    tr = kiwiClient.testrun_create(plan_id)
    tr_id = tr.get('result', {}).get('id')
    if tr_id is None:
        raise Exception('Test koşu numarası None olamaz!')
    

    # Test koşusuna ortamdaki NF'leri sürümleriyle etiket olarak giriyoruz
    file_path = 'version.txt'
    tags=kiwiClient.get_tags(file_path) or ['tag1','tag2']
    for t in tags:
        kiwiClient.testrun_add_tag(tr_id, t)
        
    # Test planındaki Test Senaryolarını -> Test koşusuna ekliyoruz
    test_cases = kiwiClient.getTestCasePlanByID(plan_id)
    for tc in test_cases["result"]:
        tc_id = tc["id"]
        #spirenttan gelen test adımları text olarak gelmeli statusleri ile birlikte
        print(tc["summary"]) 
        te = kiwiClient.TestRun_add_case(tr_id, tc_id) 
        print("te: ", te)
        te_id= te["result"][0]["id"]
        print("te_id: ", te_id)
        # Test koşusuna eklediğimiz Test Senaryolarının durumlarını giriyoruz
        a = kiwiClient.TestExecution_update(te_id, tr_id, tc_id, status_id=4)
        print("a: ", a)
      
    
    # test_cases = kiwiClient.getTestCasePlanByID(plan_id)
    # result_list = []
    # for tc in test_cases["result"]:
    #     result_list.append(tc["summary"])
    # print(result_list)

    