
import schedule
import time
import csv
from Devices.Device_list import Routers
from netmiko import ConnectHandler
from rich import print as rp


'''
  Documenting Devices' Hostname,IP-address,Software-Version,Uptime
'''
with open('/home/munia/Network_automation_with_API/Inventory/Inventory.csv', 'w')as f:
    write_data = csv.writer(f)
    write_data.writerow(['Hostname','IP address','Software Version','Serial-No','Uptime'])

    for key ,value in Routers.items():
        conn = ConnectHandler(**value)
        conn.enable()

        output   = conn.send_command('show version',use_textfsm=True)[0]
        hostname = output.get('hostname')
        ip_addr  = value.get('ip')
        version  = output.get('version')
        serial   = output.get('serial')
        uptime   = output.get('uptime')

        write_data.writerow([hostname,ip_addr,version,serial,uptime])
    
    rp(f"[cyan] Finished taking and Documenting Devices' information" )


'''
  Backing up Devices' Running Configurations Scheduled at 3PM everyday
'''
def backup_config():
    '''
    This will backup the running configs of all Routers:
    '''
    rp(f'[cyan]{backup_config.__doc__}[/cyan]')
    for key ,value in Routers.items():
        ip = value.get("ip")
        conn = ConnectHandler(**value)
        conn.enable()
        output = conn.send_command("show run")
        with open('RTR_'+ip,'w') as f:
            f.write(output)
        rp(f'[cyan] Finished backing up Host_{value.get("ip")} running-config')
schedule.every().day.at("15:00").do(backup_config) 
while True:
    schedule.run_pending()
    time.sleep(1)

