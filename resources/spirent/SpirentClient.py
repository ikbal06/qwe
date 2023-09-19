from globalProperties import *
from common.HttpClient import HttpClient


class SpirentClient(HttpClient):

    def __init__(self):

        super().__init__(
            SPIRENT_IP,
            SPIRENT_PORT,
            SPIRENT_USER,
            SPIRENT_PASSWORD,
            SPIRENT_API_PATH,
            SPIRENT_PROTOCOL
          )

    def get_libraries(self):
        path = 'libraryIds'
        return self.get(path)
    
    def get_test_servers(self):
        path = 'testServers'
        return self.get(path)
    
    def get_suts(self):
        path = 'suts'
        return self.get(path)
    
    def create_suts(self,data):
        path = 'suts'
        return self.post(path,data)
    
    def update_suts(self,sut_id_in,data):
        path = 'suts/{}'.format(sut_id_in)
        return self.post(path,data)

    def run_test(self, data):
        path = 'runningTests'
        return self.post(path, data)

    def get_running_test(self, test_run_id):
        path = 'runningTests/{}'.format(test_run_id)
        return self.get(path)

    def get_test_results(self, test_run_id):
        path = 'runningTests/{}/criteria'.format(test_run_id)
        return self.get(path)
    
    def update_test_session(self, library_id_in,test_session_name_in,data):
        path = 'libraries/{}/testSessions/{}?action=overrideAndSaveAs'.format(library_id_in,test_session_name_in)
        return self.post(path,data)

    def delete_test_run(self, test_run_id):
        path = 'runningTests/{}'.format(test_run_id)
        return self.delete(path)

