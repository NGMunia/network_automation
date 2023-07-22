'''
   APIs are created for the following services.
    - NTP
    - SNMP
    - NetFlow
    - Syslog
    - HSRP
    - DHCP
    - QoS
    - Interface configuration
    - Tunnel configuration
    - Control Plane Policing
    - Embedded event manager
'''

from Devices.Device_list import Routers
from fastapi import FastAPI, status, HTTPException
from netmiko import ConnectHandler
from pydantic import BaseModel
import ntc_templates
from Models import models


app = FastAPI()


'''
    NTP POST:
     - Configures NTP server.
     - Updates login and debug timestamps to NTP server time.
'''
@app.post('/Devices/{Device_ID}/Configure/NTP', status_code = status.HTTP_201_CREATED)
def ntp_config(post: models.NTPClass, Device_ID: str):
    device = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()
    commands = [
                'ip domain lookup',
                'ip name-server 8.8.8.8',
                'ntp server '+post.ntp_server,
                'ntp update-calendar',
                'clock timezone GMT +3',
                'service timestamps log datetime localtime year',
                'service timestamps debug datetime localtime year'
               ]
    result = conn.send_config_set(commands)
    conn.save_config()
    return result.splitlines(), f'NTP on Host_{Device_ID} configured successfully'

'''
    SNMP POST:
      - Configures SNMP on all devices
'''
@app.post('/Devices/{Device_ID}/Configure/SNMP', status_code = status.HTTP_201_CREATED)
def snmpconf(post: models.SNMPClass, Device_ID:str):
    device   = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()
    configs = ['ip access-list standard SNMP',
                'permit host '+post.snmp_server_host,
                'snmp-server community '+post.snmp_password+' ro SNMP',
                'snmp-server system-shutdown',
                'snmp-server enable traps config',
                'snmp-server host '+post.snmp_server_host+' traps version 2c '
                +post.snmp_password]
    result = conn.send_config_set(configs)
    conn.save_config()
    return result.splitlines(), f'SNMP on Host_{Device_ID} configured successfully'
     
    
'''
    NetFlow POST:
      - Configures traditional NetFlow
      - Configures Top-talkers
      - Activates NBAR
'''
@app.post('/Devices/{Device_ID}/Configure/NetFlow', status_code = status.HTTP_201_CREATED)
def netflowconf(post: models.Netflow_Class, Device_ID:str):
    device   = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()
    commands = ['ip flow-export version 9',
                'ip flow-export destination '+post.dest_ip+' '+str(post.udp_port),
                'int '+post.flow_intf,
                'ip nbar protocol-discovery',
                'ip flow ingress',
                'ip flow egress',
                'ip flow-top-talkers',
                'top 5',
                'sort-by bytes',
                'ip flow-cache timeout active 1']
    result= conn.send_config_set(commands)
    conn.save_config()
    return result.splitlines(), f'NetFlow on {Device_ID} configured successfully'

'''
    SYSLOG POST:
      - Configures Syslog on all network devices.
'''
@app.post('/Devices/{Device_ID}/Configure/Syslog', status_code = status.HTTP_201_CREATED)
def syslog_conf(post: models.Syslog_class, Device_ID: str):
    device   = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()
    commands = ['logging monitor informational',
                'logging host '+post.server_ip,
                'logging trap']
    result = conn.send_config_set(commands)
    conn.save_config()
    return result.splitlines(), f'Syslog on Host_{Device_ID} configured successfully'
        

'''
    HSRP POST:
      - Configuring HSRP
'''
@app.post('/Devices/{Device_ID}/Configure/HSRP', status_code = status.HTTP_201_CREATED)
def HSRP_Config(post: models.HSRP_class, Device_ID: str):
    device   = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()
    commands = [
                'int '+post.HSRP_intf,
                'standby version 2',
                'standby '+str(post.group_ID)+ ' ip '+post.virtual_IP,
                'standby '+str(post.group_ID)+ ' preempt',
                'standby '+str(post.group_ID)+ ' priority '+str(post.priority)
               ]
    result = conn.send_config_set(commands)
    conn.save_config()
    return result.splitlines(), f'HSRP on Host_{Device_ID} configured successfully'


'''
    DHCP POST
      - Configures DHCP
'''
@app.post('/Devices/{Device_ID}/Configure/DHCP', status_code = status.HTTP_201_CREATED)
def DHCP_Conf(post: models.DHCP_class, Device_ID: str):
    device   = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()
    commands = [
                'ip dhcp excluded-address '+post.lowest_excluded_address+' '+  
                 post.highest_excluded_address,
                'ip dhcp pool '+post.DHCP_pool_name,
                'network '+post.network_and_mask,
                'default-router '+post.gateway_IP,
                'dns-server 8.8.8.8'
               ]
    result = conn.send_config_set(commands)
    conn.save_config()
    return result.splitlines(), f'DHCP on Host_{Device_ID} configured successfully'


'''
  QoS configuration
'''
@app.post('/Devices/{Device_ID}/Configure/QoS', status_code=status.HTTP_201_CREATED)
def QoS_config(post: models.QoS_profile_bandwidth, Device_ID:str):
    sum_bandwidth = (post.Voice + post.Realtime_video + post.Critical_data 
                     +post.Scavenger)
    
    if sum_bandwidth > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail ='Bandwidth allocation exceeded 100%') 
    else:
        device = Routers[Device_ID]
        conn = ConnectHandler(**device)
        conn.enable()

        commands = [
                #Traffic classification
                     'class-map match-any Scavenger_class',
                     'match protocol bittorrent',
                     'match protocol netflix',
                     'match protocol facebook',
                     'match protocol instagram',
                     'match protocol twitter',
                     'match dscp cs1',
                     'class-map match-any Voice_class',
                     'match dscp ef',
                     'match protocol rtp-audio',
                     'class-map match-any Realtime_class',
                     'match protocol rtp-video',
                     'match dscp af41',
                     'class-map match-any Critical_data_class',
                     'match protocol dns',
                     'match dscp af31',
                #Declaring Policy Map
                     'policy-map '+post.Policy_name,
                     'class Scavenger_class',
                     'set dscp cs1',
                     'bandwidth percent '+str(post.Scavenger),
                #Voice-traffic data marking    
                     'class Voice_class',
                     'set dscp ef',
                     'priority level 1 percent '+str(post.Voice),
                #Real-time data marking
                     'class Realtime_class',
                     'set dscp af41',
                     'priority level 2 percent '+str(post.Realtime_video),
                #Critical data marking
                     'class Critical_data_class',
                     'set dscp af31',
                     'bandwidth percent '+str(post.Critical_data),
                #Class-default data marking:
                     'class class-default',
                     'fair-queue',
                #Activating the Policy
                     'interface '+post.Service_intf,
                     'service-policy output '+post.Policy_name ]
        result = conn.send_config_set(commands)
        conn.save_config()       
        return result.splitlines(), f'QoS on Host_{Device_ID} configured successfully'


'''
  API POST Configuring Ethernet and Loopback Interfaces
'''
@app.post('/Devices/{Device_ID}/Configure/Interface', status_code=status.HTTP_201_CREATED)
def Intf_conf(post : models.interface_conf_class, Device_ID: str):
    device   = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()
    commands = [
                'int '+post.interface_type,
                'description '+post.Description,
                'ip address '+post.ip_address+' '+post.subnet_mask,
                'no shut'
               ]
    result = conn.send_config_set(commands)
    return result.splitlines(), f'Interface {post.interface_type} on {Device_ID} configured successfully'


'''
   API POST Configuring GRE tunnel interfaces
'''
@app.post('/Devices/{Device_ID}/Configure/Interface/Tunnel', status_code=status.HTTP_201_CREATED)
def Intf_conf(post : models.tunnel_conf_class, Device_ID:str):
    device   = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()
    commands = [
                'int tunnel '+str(post.tunnel_id),
                'tunnel source '+post.tunnel_src,
                'tunnel destination '+post.tunnel_dest,
                'ip address '+post.ip_address+' '+post.subnet_mask,
                'ip mtu 1400'
               ]
    result = conn.send_config_set(commands)
    return result.splitlines(), f'Tunnel{post.tunnel_id} on {Device_ID} configured successfully'


'''
   CoPP configuration
'''
@app.post('/Devices/{Device_ID}/Configure/CoPP',status_code=status.HTTP_201_CREATED)
def CoPP_conf(Device_ID: str):
    device   = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()
    from Models.models import CoPP 
    result = conn.send_config_set(CoPP)
    conn.save_config()
    return result.splitlines(), f'CoPP on {Device_ID} configured successfully'


'''
  Configuring EEM for automatic Config Backup
'''
class EEM_Class(BaseModel):
    filename : str
    tftp_server : str
@app.post('/Devices/{Device_ID}/Configure/EEM', status_code=status.HTTP_201_CREATED)
def EEM_config(post: EEM_Class, Device_ID: str):
    device   = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()
    commands = [
                'event-manager environment filename '+post.filename,
                'event-manager environment tftpserver tftp://'+post.tftp_server+'/',
                'event-manager applet AUTOMATIC_CONFIG_BACKUP',
                'event-timer cron cron-entry "30 23 * * 1-6"',
                'action 1.0 cli command "enable"',
                'action 1.1 cli command "debug event manager action cli"',
                'action 1.2 cli command "conf t"',
                'action 1.3 cli command "file prompt quiet"',
                'action 1.4 cli command "do copy run $tftpserver$filename"',
                'action 1.5 cli command "no file prompt quiet"',
                'action 1.6 syslog priority informational msg "Backup Successful!"'
               ]
    result = conn.send_config_set(commands)
    conn.save_config()
    return result.splitlines(), f'EEM on {Device_ID} Configured successfully!'
    

'''
  API GET
    - show interfaces brief
'''
@app.get('/GET/Devices/{Device_ID}/interfaces')
def intf_status(Device_ID: str):
    device   = Routers[Device_ID] 
    conn = ConnectHandler(**device)
    conn.enable()
    result = conn.send_command('show ip interface brief', use_textfsm=True)
    return result
    

'''
   API GET
   - Device information
'''
@app.get('/GET/Devices/{Device_ID}/version')
def Device_info(Device_ID: str):
    device   = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()
    result = conn.send_command('show version', use_textfsm=True)
    return result 
