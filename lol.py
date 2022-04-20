import pyodbc
import requests
 
#response = requests.get("http://www.condast.com:8080/churuatas/rest/support/find?latitude=52.25991932491945&longitude=6.152503532173467")
response = requests.get("http://www.condast.com:8080/churuatas/rest/support/show")
print(response.json())