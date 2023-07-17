from Devices.Device_list import R1_LAN, R1_EDGE, R2_EDGE, R1_VPN, R2_VPN
from netmiko import ConnectHandler
from rich import print as rp
import ntc_templates


# '''
#   Verifying Device information (version)
# '''
# for devices in R1_LAN, R1_EDGE, R2_EDGE, R1_VPN, R2_VPN:
#     rp('\n'f'[cyan]{("-"*20)}Host {devices.get("ip")}{"-"*20}')
    
#     conn = ConnectHandler(**devices)
#     conn.enable()
#     result = conn.send_command('show version', use_textfsm=True)
#     for output in result:
#         for k,v in output.items():
#             print(f'{k:>15} : {v}')


'''
Verifying HSRP status
'''
for devices in R1_EDGE, R2_EDGE:
    rp('\n'f'[cyan]{("-"*20)}Host {devices.get("ip")}{"-"*20}')

    conn = ConnectHandler(**devices)
    conn.enable()

    result =conn.send_command('show standby e0/0.25', use_textfsm=True)
    for output in result:
        for k,v in output.items():
            print(f'{k:>19} : {v}')


