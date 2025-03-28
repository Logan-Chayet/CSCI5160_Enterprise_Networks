from netmiko import ConnectHandler
from napalm import get_network_driver
import csv
import datetime

def sshInfo():
    csv_file = "devices.csv"
    data = {}

    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            router_name = row["hostname"]
            router_data = {
                "device_type": row["device_type"],
                "ip": row["ip"],
                "username": row["username"],
                "password": row["password"] 
            }
            data[router_name] = router_data

    return data 

def getconfig(device_type, ip, user, password):
    driver = get_network_driver(device_type)
    eos = driver(ip, user, password)

    eos.open()

    eos_output = eos.get_config(retrieve='running')

    eos.close()

    return eos_output['running']
def get_show_ip_route(device_type, ip, user, password):
    driver = get_network_driver(device_type)
    eos = driver(ip, user, password)

    eos.open()

    eos_output = eos.cli(['show ip route'])

    eos.close()

    return eos_output['show ip route']
def get_show_spanning_tree(device_type, ip, user, password):
    driver = get_network_driver(device_type)
    eos = driver(ip, user, password)

    eos.open()

    eos_output = eos.cli(['show spanning-tree'])

    eos.close()

    return eos_output['show spanning-tree']
 
def getGoldenConfig():
    return_info = []
    routers = sshInfo()
    
    for i in routers:
        string = routers[i]['device_type']
        result = string.split('_')[1]
        output = get_show_spanning_tree(result, routers[i]['ip'], routers[i]['username'], routers[i]['password'])
        
        #Name the config
        fileName = i+"_spanning_tree.txt"

        #Write the configs to a new file
        with open("golden_configs/"+fileName, 'w') as file:
            file.write(output)

        print(fileName)
        return_info.append(fileName)
    return "\n".join(return_info)

getGoldenConfig()