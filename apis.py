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
'''


from fastapi import FastAPI, status, HTTPException
from netmiko import ConnectHandler
from pydantic import BaseModel
from Devices.Device_list import R1_LAN, R1_EDGE, R2_EDGE, R1_VPN, R2_VPN
import ntc_templates


app = FastAPI()


'''
    NTP POST:
     - Configures NTP server.
     - Updates login and debug timestamps to NTP server time.
'''
class NTPClass (BaseModel):
    Device_IP  : str
    ntp_server : str
@app.post('/Devices/Configure/NTP', status_code = status.HTTP_201_CREATED)
def ntp_config(post: NTPClass):
    device   = {
                'device_type': 'cisco_ios',
                'username': 'Automation',
                'password': 'cisco123',
                'secret': 'cisco123',
                'ip' : post.Device_IP
               }
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
    return result
    

'''
    SNMP POST:
      - Configures SNMP on all devices
'''
class SNMPClass(BaseModel):
    Device_IP : str
    snmp_server_host : str
    snmp_password : str
@app.post('/Devices/Configure/SNMP', status_code = status.HTTP_201_CREATED)
def snmpconf(post: SNMPClass):
    device   = {
                'device_type': 'cisco_ios',
                'username': 'Automation',
                'password': 'cisco123',
                'secret': 'cisco123',
                'ip' : post.Device_IP }

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
    return result.splitlines(), f'SNMP on Host_{post.Device_IP} configured successfully'
     
    
'''
    NetFlow POST:
      - Configures traditional NetFlow
      - Configures Top-talkers
      - Activates NBAR
'''
class Netflow_Class(BaseModel):
    Device_IP : str
    flow_intf : str
    udp_port  : int
    dest_ip   : str
@app.post('/Devices/Configure/NetFlow', status_code = status.HTTP_201_CREATED)
def netflowconf(post: Netflow_Class):
    device   = {
                'device_type': 'cisco_ios',
                'username': 'Automation',
                'password': 'cisco123',
                'secret': 'cisco123',
                'ip' : post.Device_IP
               }
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
    return result.splitlines(), f'NetFlow on Host_{post.Device_IP} configured successfully'

'''
    SYSLOG POST:
      - Configures Syslog on all network devices.
'''
class Syslog_class(BaseModel):
    server_ip : str
    Device_IP : str
@app.post('/Devices/Configure/Syslog', status_code = status.HTTP_201_CREATED)
def syslog_conf(post: Syslog_class):
    device   = {
                'device_type': 'cisco_ios',
                'username': 'Automation',
                'password': 'cisco123',
                'secret': 'cisco123',
                'ip' : post.Device_IP
               }
    conn = ConnectHandler(**device)
    conn.enable()
    commands = ['logging monitor informational',
                'logging host '+post.server_ip,
                'logging trap']
    result = conn.send_config_set(commands)
    conn.save_config()
    return result.splitlines(), f'Syslog on Host_{post.Device_IP} configured successfully'
        

'''
    HSRP POST:
      - Configuring HSRP
'''
class HSRP_class(BaseModel):
    host_IP : str
    virtual_IP : str
    group_ID : int
    HSRP_intf : str
    priority : int
@app.post('/Devices/Configure/HSRP', status_code = status.HTTP_201_CREATED)
def HSRP_Config(post: HSRP_class):
    device   = {
                'device_type': 'cisco_ios',
                'username': 'Automation',
                'password': 'cisco123',
                'secret': 'cisco123',
                'ip' : post.host_IP
               }
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
    return result.splitlines(), f'HSRP on Host_{post.Device_IP} configured successfully'


'''
    DHCP POST
      - Configures DHCP
'''
class DHCP_class(BaseModel):
    host_IP : str
    network_and_mask : str
    lowest_excluded_address : str
    highest_excluded_address : str
    gateway_IP : str
    DHCP_pool_name : str
@app.post('/Devices/Configure/DHCP', status_code = status.HTTP_201_CREATED)
def DHCP_Conf(post: DHCP_class):
    device   = {
                'device_type': 'cisco_ios',
                'username': 'Automation',
                'password': 'cisco123',
                'secret': 'cisco123',
                'ip' : post.host_IP
               }
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
    return result.splitlines(), f'DHCP on Host_{post.Device_IP} configured successfully'


'''
  QoS configuration
'''
class QoS_profile_bandwidth(BaseModel):
    Host_IP : str
    Policy_name : str
    Service_intf: str
    Voice : int
    Realtime_video : int
    Critical_data : int
    Scavenger : int
@app.post('/Devices/Configure/QoS', status_code=status.HTTP_201_CREATED)
def QoS_config(post: QoS_profile_bandwidth):
    sum_bandwidth = (post.Voice + post.Realtime_video + post.Critical_data 
                     +post.Scavenger)
    
    if sum_bandwidth > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail ='Bandwidth allocation exceeded 100%') 
    else:
        device = {
                  'device_type': 'cisco_ios',
                  'username': 'Automation',
                  'password': 'cisco123',
                  'secret': 'cisco123',
                  'ip' : post.Host_IP
                 }
        conn = ConnectHandler(**device)
        conn.enable()

        commands = [
                #Traffic classification
                     'class-map match-any Scavenger_class',
                     'match protocol bittorrent',
                     'match protocol netflix',
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
        return result.splitlines(), f'QoS on Host_{post.Device_IP} configured successfully'



'''
  API POST Configuring Ethernet and Loopback Interfaces
'''
class interface_conf_class(BaseModel):
    Host_IP : str
    interface_type : str
    ip_address : str
    subnet_mask : str
@app.post('/Devices/Configure/Interface', status_code=status.HTTP_201_CREATED)
def Intf_conf(post :interface_conf_class):
    device   = {
                'device_type': 'cisco_ios',
                'username': 'Automation',
                'password': 'cisco123',
                'secret': 'cisco123',
                'ip' : post.host_IP
               }
    conn = ConnectHandler(**device)
    conn.enable()

    commands = [
                'int '+post.interface_type,
                'ip addresss '+post.ip_address+' '+post.subnet_mask,
                'no shut'
               ]
    result = conn.send_config_set(commands)
    return result.splitlines(), f'Interface {post.interface_type} on Host_{post.Device_IP} configured successfully'



'''
   API POST Configuring GRE tunnel interfaces
'''
class tunnel_conf_class(BaseModel):
    Host_IP : str
    tunnel_id : int
    tunnel_src : str
    tunnel_dest : str
    ip_address : str
    subnet_mask : str

@app.post('/Devices/Configure/Interface/Tunnel', status_code=status.HTTP_201_CREATED)
def Intf_conf(post :tunnel_conf_class):
    device   = {
                'device_type': 'cisco_ios',
                'username': 'Automation',
                'password': 'cisco123',
                'secret': 'cisco123',
                'ip' : post.Host_IP
               }
    conn = ConnectHandler(**device)
    conn.enable()

    commands = [
                'int tunnel '+str(post.tunnel_id),
                'tunnel source '+post.tunnel_src,
                'tunnel destination '+post.tunnel_dest,
                'ip address '+post.ip_address+' '+post.subnet_mask,
                'no shut'
               ]
    result = conn.send_config_set(commands)
    return result.splitlines(), f'Tunnel{post.tunnel_id}on Host_{post.Device_IP} configured successfully'


