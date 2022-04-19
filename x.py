from unittest import result
from datetime import date, datetime
import pyTigerGraph as tg

TG_HOST = "https://refugiados-unidos.i.tgcloud.io/"
TG_USERNAME = "tigergraph"
TG_PASSWORD = "Abcd1234!"
TG_GRAPHNAME = "RefugiadosUnidos"

conn = tg.TigerGraphConnection(TG_HOST, TG_GRAPHNAME, TG_USERNAME, TG_PASSWORD)
token = conn.getToken("i3u0jpebhih97seb3kgu1omg9dptcpvs")
nu = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
ls = conn.gsql("ls", options=[])
print(token)

#data = {"email": "burhhhanc@gmail.com", "password": "Canboz11", "firstname": "Burhan", "surname": "Canbaz", "latitude": 0, "longtitude": 0, "country": "Poland", "userroleID": 0, "registrationDate": str(nu), "endDate": str(nu)}
#conn.runInstalledQuery("Registration", data)
users = conn.runInstalledQuery("showUsers")
print(users)

#queries = conn.gsql('''
#    use graph RefugiadosUnidos
#    show query *
#''', options=[])

#print(queries)

#result = conn.runInstalledQuery("helloWorld")

#print(result)
#print(result[0]["Hello World!"])

#lol = {"ID": str(2), "naam": "Medicine"}

#conn.runInstalledQuery("test", lol)
#conn.runInstalledQuery("test2")
#x = conn.runInstalledQuery("test2")
#print(x)