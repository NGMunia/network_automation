
from netmiko import ConnectHandler
from Devices.Device_list import R1_LAN, R1_EDGE, R2_EDGE, R1_VPN, R2_VPN
import ntc_templates
from rich import print as rp
import json

for devices in R1_LAN, R1_EDGE, R2_EDGE, R1_VPN:
        conn = ConnectHandler(**devices)
        conn.enable()

        result = conn.send_command('show version', use_textfsm=True)
        for output in result:
            rp('\n'f'Host_{devices.get("ip")}:',output)