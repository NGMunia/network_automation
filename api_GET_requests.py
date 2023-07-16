
'''
HTTP requests methods:
  - GET    Read method that retrieves information
  - POST   create method that submits new data.
  - PUT    updates the entire resource data
  - PATCH  updates a part of the resource data.
  - DELETE deletes the resource data
'''

import requests
from rich import print as rp


'''
   GET request that retrieves device info:
'''
info_url = 'http://10.1.30.100:8000/Devices/Info/AllDevices'

results  = requests.get(info_url).json()

for output in results:
    rp('\n\n'f'[cyan]{"-"*20}{output.get("hostname")}{"-"*20}[/cyan]')
    for k,v in output.items():
        print(f'{k:>15}: {v})')


'''
   HSRP status
'''
hsrp_url = 'http://10.1.30.100:8000/Devices/Info/HSRPStatus'
result = requests.get(hsrp_url).json()
rp(result)


'''
  OSPF routes on R1_LAN
'''
ospf_url = 'http://10.1.30.100:8000/Devices/Info/routes/R1_LAN'
result = requests.get(ospf_url).json()
rp(result)
