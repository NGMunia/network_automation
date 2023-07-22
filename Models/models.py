
from pydantic import BaseModel

# NTP Class
class NTPClass (BaseModel):
    ntp_server : str

#SNMP Class
class SNMPClass(BaseModel):
    snmp_server_host : str
    snmp_password : str

#NetFlow Class
class Netflow_Class(BaseModel):
    flow_intf : str
    udp_port  : int
    dest_ip   : str

#Syslog Class
class Syslog_class(BaseModel):
    server_ip : str

#HSRP Class
class HSRP_class(BaseModel):
    virtual_IP : str
    group_ID : int
    HSRP_intf : str
    priority : int

#DHCP Class
class DHCP_class(BaseModel):
    network_and_mask : str
    lowest_excluded_address : str
    highest_excluded_address : str
    gateway_IP : str
    DHCP_pool_name : str

#QoS Class
class QoS_profile_bandwidth(BaseModel):
    Policy_name : str
    Service_intf: str
    Voice : int
    Realtime_video : int
    Critical_data : int
    Scavenger : int

#Interface Class
class interface_conf_class(BaseModel):
    interface_type : str
    Description : str
    ip_address : str
    subnet_mask : str

#Tunnel Class
class tunnel_conf_class(BaseModel):
    tunnel_id : int
    tunnel_src : str
    tunnel_dest : str
    ip_address : str
    subnet_mask : str

#EEM Class
class EEM_Class(BaseModel):
    filename : str
    tftp_server : str


CoPP  =    [
            #Configuring ACLs
                 'ip access-list extended Route_acl',
                 'permit ospf any host 224.0.0.5',
                 'permit ospf any host 224.0.0.6',
                 'ip access-list extended Mgt_acl',
                 'permit udp any any eq 161',
                 'permit tcp any any eq 22',
                 'permit udp any any eq ntp',
                 'ip access-list extended Icmp_acl',
                 'permit icmp any any',
            #Configuring CLass-maps
                 'class-map Route_class',
                 'match access-group name Route_acl',
                 'class-map Mgt_class',
                 'match access-group name Mgt_acl',
                 'class-map Icmp_class',
                 'match access-group name Icmp_acl',
            #Configuring Policy maps
                 'policy-map CoPP-Policy',
                 'class Route_class',
                 'police 128k conform-action transmit exceed-action transmit violate-action transmit',
                 'class Mgt_class',
                 'police 128k conform-action transmit exceed-action transmit violate-action transmit',
                 'class Icmp_class',
                 'police 8k conform-action transmit exceed-action transmit violate-action drop',
            #Activating CoPP
                 'control-plane',
                 'service-policy input CoPP-Policy'     
               ]

