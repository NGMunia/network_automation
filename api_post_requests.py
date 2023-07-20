
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
hsrp_url = 'http://10.1.30.100:8000/Devices/10.1.25.2/Configure/HSRP'
data =  { 
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
   Configuring DHCP on R2-VPN
'''
dhcp_url  = 'http://10.1.30.100:8000/Devices/10.1.31.1/Configure/DHCP'
dhcp_data =  {
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
   Configuring Syslog on R1-LAN.
'''
syslog_url = 'http://10.1.30.100:8000/Devices/10.1.30.1/Configure/Syslog'
syslog_data = {'server_ip':'10.1.30.254'}
result = requests.post(syslog_url, json=syslog_data)

if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' Syslog not configured!')



'''
    NTP configuration.
'''
ntp_url  = 'http://10.1.30.100:8000/Devices/10.1.25.2/Configure/NTP'
ntp_data = {'ntp_server': '10.1.25.254'}
result   = requests.post(ntp_url, json=ntp_data)
if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' NTP not configured!')



'''
   QoS configuration
'''
qos_url = 'http://10.1.30.100:8000/Devices/10.1.30.1/Configure/QoS'

QoS_data = {
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


'''
   NetFlow configuration on R2-VPN Router
'''
flow_url = 'http://10.1.30.100:8000/Devices/10.1.31.1/Configure/NetFlow'
flow_data = {
             'flow_intf' : 'e0/0',
             'udp_port'  : 9996,
             'dest_ip'   : '10.1.30.254'
            }
result = requests.post(flow_url, json=flow_data)
if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' NetFlow not configured!')


'''
  Configuring SNMP
'''
snmp_url = 'http://10.1.30.100:8000/Devices/10.1.25.2/Configure/SNMP'
snmp_data = {
             'snmp_server_host': '10.1.30.254',
             'snmp_password': 'device_snmp'}
result = requests.post(snmp_url, json=snmp_data)
if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' SNMP not configured!')


'''
  Configuring an Interface on R2-Edge
'''
intf_url = 'http://10.1.30.100:8000/Devices/10.1.25.2/Configure/Interface'

intf_data = {
              'interface_type' : 'e0/0.99',
              'Description' : 'Link-to-DMZ-Network',
              'ip_address' : '10.1.99.3',
              'subnet_mask' : '255.255.255.0'
            }
result = requests.post(intf_url, json=intf_data)
if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' Interface not configured!')


'''
   Configuring HSRP on R2-Edge:
'''
hsrp_url  = 'http://10.1.30.100:8000/Devices/10.1.25.3/Configure/HSRP'
hsrp_data =  { 
              'virtual_IP':'10.1.99.254',
              'group_ID':99,
              'HSRP_intf':'e0/0.99',
              'priority': 110    
             }
result = requests.post(hsrp_url,json=hsrp_data)
if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' HSRP not configured!')



'''
  API GET request
'''
intf_url = 'http://10.1.30.100:8000/GET/Devices/10.1.25.2/interfaces'
result = requests.get(intf_url).json()
rp(type(result))
