'''
Created on 2014-6-3

@author: devuser
'''
import urllib.request

class PFManager:
    '''
    classdocs
    '''
    def __init__(self):
        print("init")
    
    def pf_get(self, data='{"cardNo":"123456789","password":"111111111","source":"源"}', timeout=5000):
        urllib.request.urlopen("http://IP:端口/spdbcccAccountManager/services/DynamicPsw?wsdl", data, timeout)
        
    
    def ge_sdk_get(self):
        response = urllib.request.urlopen("http://api.dev.laohu.com")
        return response.read()
    

if __name__ == '__main__':
    pfManager = PFManager()
    result = pfManager.ge_sdk_get()
    print(result)
    
        