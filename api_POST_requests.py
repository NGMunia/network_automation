
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
  When writing a POST request:
    - We create a dictionary (data) that contains the data to be sent in the request body. 
      We use the json parameter of the requests.post() method to automatically encode the payload 
      as JSON.

    - After sending the request, we check the response status code. 
      If it's 201 (resource data created), we print the response code print the return statement. 
      Otherwise, we print an error message along with the actual status code returned by the API.
'''

'''
   Configuring HSRP on R1-Edge:
'''
hsrp_url = 'http://10.1.30.100:8000/Devices/Configure/HSRP'

data =  { 
            'host_IP':'10.1.25.2',
            'virtual_IP':'10.1.25.254',
            'group_ID':25,
            'HSRP_intf': 'e0/0.25',
            'priority': 110    
        }

result = requests.post(hsrp_url,json=data)
if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' HSRP not configured!')



'''
   Configuring HSRP on R2-Edge:
'''
hsrp_url  = 'http://10.1.30.100:8000/Devices/Configure/HSRP'

hsrp_data =  { 
              'host_IP':'10.1.25.3',
              'virtual_IP':'10.1.25.254',
              'group_ID':25,
              'HSRP_intf': 'e0/0.25',
              'priority': 100    
             }

result = requests.post(hsrp_url,json=hsrp_data)
if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' HSRP not configured!')



'''
   Configuring DHCP on R2-VPN
'''
rp(f'[cyan]{("-"*10)}Configuring DHCP{("-"*10)}[/cyan]')
dhcp_url  = 'http://10.1.30.100:8000/Devices/Configure/DHCP'

dhcp_data =  {
              'host_IP': '10.1.31.1',
              'network_and_mask': '10.1.31.0 255.255.255.0',
              'lowest_excluded_address': '10.1.31.1',
              'highest_excluded_address': '10.1.31.10',
              'gateway_IP': '10.1.31.1',
              'DHCP_pool_name':'BRANCH_LAN_DHCP'
             }
result = requests.post(dhcp_url, json=dhcp_data)
if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' DHCP not configured!')



'''
   Configuring Syslog on devices.
'''
syslog_url = 'http://10.1.30.100:8000/Devices/Configure/Syslog'

syslog_data = {'server_ip':'10.1.30.100'}
result = requests.post(syslog_url, json=syslog_data)

if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' Syslog not configured!')



'''
    NTP configuration.
'''
ntp_url  = 'http://10.1.30.100:8000/Devices/Configure/NTP'

ntp_data = {
             'Device_IP':'10.1.31.1',
             'ntp_server': '10.1.25.254'
           }
result   = requests.post(ntp_url, json=ntp_data)

if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' NTP not configured!')



'''
   QoS configuration
'''
qos_url = 'http://10.1.30.100:8000/Devices/Configure/QoS'

QoS_data = {
            'Host_IP':'10.1.30.1',
            'Policy_name': 'NETWORK_POLICY',
            'Service_intf': 'e0/1.25',
            'Voice' : 10,
            'Realtime_video' : 20,
            'Critical_data' : 20,
            'Scavenger' : 1
           }
result = requests.post(qos_url, json=QoS_data)
if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' QoS not configured!')
