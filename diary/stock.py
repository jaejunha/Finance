from datetime import date
from python.init import *
from python.http import *

if __name__ == "__main__":	

    removeNohup()
    int_port = getPort()
    dic_account = getAccount()
    list_item = downloadItem()

    server_http = HTTPServer(("", int_port), makeHandler(dic_account, list_item))
    server_http.serve_forever()
