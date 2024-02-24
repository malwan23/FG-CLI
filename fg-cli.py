#Main Script
#Beta Version 1.5

import click
import configparser
import requests
import subprocess
import sys
import json

# Read the configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
api_token = config['API']['token']
verify_ssl = config.getboolean('API', 'verify_ssl')
management_ip = config['API']['management_ip']
management_port = config.getint('API', 'management_port')

# Base URL for APIs
base_url = f'https://{management_ip}:{management_port}/api/v2/'

# Base URLs for the APIs
base_urls = {
    'fortiview': 'monitor/fortiview/statistics',
    'switch': 'monitor/switch-controller/managed-switch/status',
    'wifi': 'monitor/wifi/ap_status',
    'user_firewall': 'monitor/user/firewall',
    'user_banned': 'monitor/user/banned',
    'license': 'monitor/license/status',
    'fortiguard': 'monitor/fortiguard/service-communication-stats',
    'config_backup': 'backup/config/start',
    'fortianalyzer': 'log/fortianalyzer/{}/raw',
    'forticloud': 'log/forticloud/{}/raw',
    'memory': 'log/memory/{}/raw',
    'disk': 'log/disk/{}/raw',
    'dns_filter': 'cmdb/dnsfilter/domain-filter/{id}',
    'routing': 'monitor/router/statistics',
    'vpn': 'monitor/vpn/ipsec',
    'ntp_status': 'monitor/system/ntp/status',
    'dhcp_status': 'monitor/system/interface/dhcp-status',
    'snmp_status': 'cmdb/system.snmp/sysinfo',
    'dns_status': 'monitor/system/acquired-dns',
    'voip_profile': 'cmdb/voip/profile/',
    'waf': 'cmdb/waf/main-class/{id}',
    'dlp': 'cmdb/dlp/filepattern/{id}',
    'ips': 'monitor/ips/anomaly',
    'proxy_pac_file': 'monitor/webproxy/pacfile/download'  # Add Proxy PAC file key
}




# Function to fetch data from APIs
def fetch_data(endpoint, params=None):
    try:
        url = base_url + base_urls[endpoint]
        if params:
            url = url.format(**params)
        response = requests.get(url, headers={'Authorization': 'Bearer ' + api_token}, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            click.echo(f"Error: {response.text}")
            return None
    except Exception as e:
        click.echo(f"An error occurred: {e}")
        return None

# Function to fetch FortiView statistics
def fetch_fortiview_statistics():
    data = fetch_data('fortiview')
    if data:
        click.echo(json.dumps(data, indent=4))

# Function to fetch switch controller status
def fetch_switch_controller_status():
    data = fetch_data('switch')
    if data:
        click.echo(data)

# Function to fetch WiFi access point status
def fetch_wifi_ap_status():
    data = fetch_data('wifi')
    if data:
        click.echo(data)

# Function to fetch firewall user information
def fetch_firewall_user_info():
    data = fetch_data('user_firewall')
    if data:
        click.echo(data)

# Function to fetch banned user information
def fetch_banned_user_info():
    data = fetch_data('user_banned')
    if data:
        click.echo(data)

# Function to fetch license status
def fetch_license_status():
    data = fetch_data('license')
    if data:
        click.echo(data)

# Function to fetch FortiGuard status
def fetch_fortiguard_status():
    data = fetch_data('fortiguard')
    if data:
        click.echo(data)

# Function to fetch DNS filter information
def fetch_dns_filter_info():
    data = fetch_data('dns-filter')
    if data:
        click.echo(data)

# Function to fetch routing statistics
def fetch_routing_statistics():
    data = fetch_data('routing')
    if data:
        click.echo(data)

# Function to fetch VPN information
def fetch_vpn_info():
    data = fetch_data('vpn')
    if data:
        click.echo(data)

# Function to fetch NTP status
def fetch_ntp_status():
    data = fetch_data('ntp_status')
    if data:
        click.echo(json.dumps(data, indent=4))

# Function to fetch DHCP status
def fetch_dhcp_status():
    data = fetch_data('dhcp_status')
    if data:
        click.echo(json.dumps(data, indent=4))

# Function to fetch VOIP profile
def fetch_voip_profile(voip_profile_name):
    data = fetch_data('voip_profile', params={'name': voip_profile_name})
    if data:
        click.echo(json.dumps(data, indent=4))

# Function to fetch SNMP status
def fetch_snmp_status():
    data = fetch_data('snmp_status')
    if data:
        click.echo(json.dumps(data, indent=4))

# Function to fetch DNS status
def fetch_dns_status():
    data = fetch_data('dns_status')
    if data:
        click.echo(json.dumps(data, indent=4))

# Function to fetch WAF data
def fetch_waf_data(waf_id):
    url = base_url + base_urls['waf'].format(id=waf_id)
    data = fetch_data('waf', {'id': waf_id})  # Pass endpoint and params separately
    if data:
        click.echo(data)

# Function to fetch DLP data
def fetch_dlp_data(dlp_id):
    url = base_url + base_urls['dlp'].format(id=dlp_id)
    data = fetch_data('dlp', {'id': dlp_id})  # Pass endpoint and params separately
    if data:
        click.echo(data)

# Function to fetch IPS anomaly data
def fetch_ips_anomaly():
    try:
        url = base_url + base_urls['ips']  # Use the 'ips' key to access the IPS endpoint
        response = requests.get(url, headers={'Authorization': 'Bearer ' + api_token}, verify=False)
        if response.status_code == 200:
            click.echo(response.json())
        else:
            click.echo(f"Error: {response.text}")
    except Exception as e:
        click.echo(f"An error occurred: {e}")

# Function to fetch Proxy PAC file
def fetch_proxy_pac_file():
    try:
        url = base_url + base_urls['proxy_pac_file']  # Update the key in base_urls dictionary
        response = requests.get(url, headers={'Authorization': 'Bearer ' + api_token}, verify=False)
        if response.status_code == 200:
            # Save the PAC file or handle its content as needed
            click.echo("PAC file downloaded successfully.")
        else:
            click.echo(f"Error: {response.text}")
    except Exception as e:
        click.echo(f"An error occurred: {e}")

# Function to initiate configuration backup
def initiate_config_backup():
    try:
        url = base_url + base_urls['config_backup']
        subprocess.run([sys.executable, 'backup2.py', api_token])
        click.echo("Configuration backup initiated successfully.")
    except Exception as e:
        click.echo(f"Error initiating configuration backup: {e}")

# Function to fetch data for FortiAnalyzer status, FortiCloud logs, Memory logs, Disk logs
def fetch_logging_data(endpoint):
    data = fetch_data(endpoint)
    if data:
        click.echo(data)

# Function to handle the submenu for FortiAnalyzer logging
def fortianalyzer_logging_submenu():
    while True:
        click.echo("FortiAnalyzer Logging Submenu:")
        click.echo("Available types: virus, webfilter, waf, ips, anomaly, app-ctrl, emailfilter, dlp, voip, gtp, dns, ssh, ssl, cifs, file-filter")
        click.echo("Enter 'exit' to return to the main menu.")
        type_choice = click.prompt("Enter the type", type=str)
        
        # Check if the user wants to exit
        if type_choice.lower() == 'exit':
            return
        
        base_url_fortianalyzer = f'https://{management_ip}:{management_port}/api/v2/log/fortianalyzer/{type_choice}/raw'

        try:
            response = requests.get(base_url_fortianalyzer, headers={'Authorization': 'Bearer ' + api_token}, verify=False)
            if response.status_code == 200:
                # Print out the response content for debugging
                click.echo("Response content:")
                click.echo(response.content)
            else:
                click.echo(f"Error: {response.text}")
        except requests.exceptions.RequestException as e:
            click.echo(f"Request error occurred: {e}")
        except Exception as e:
            click.echo(f"Error occurred: {e}")

# Function to handle the submenu for FortiCloud logging
def forticloud_logging_submenu():
    while True:
        click.echo("FortiCloud Logging Submenu:")
        click.echo("Available types: virus, webfilter, waf, ips, anomaly, app-ctrl, emailfilter, dlp, voip, gtp, dns, ssh, ssl, cifs, file-filter")
        click.echo("Enter 'exit' to return to the main menu.")
        type_choice = click.prompt("Enter the type", type=str)
        
        # Check if the user wants to exit
        if type_choice.lower() == 'exit':
            return
        
        base_url_forticloud = f'https://{management_ip}:{management_port}/api/v2/log/forticloud/{type_choice}/raw'

        try:
            response = requests.get(base_url_forticloud, headers={'Authorization': 'Bearer ' + api_token}, verify=False)
            if response.status_code == 200:
                # Print out the response content for debugging
                click.echo("Response content:")
                click.echo(response.content)
            else:
                click.echo(f"Error: {response.text}")
        except requests.exceptions.RequestException as e:
            click.echo(f"Request error occurred: {e}")
        except Exception as e:
            click.echo(f"Error occurred: {e}")

# Function to handle the submenu for Memory logging
def memory_logging_submenu():
    while True:
        click.echo("Memory Logging Submenu:")
        click.echo("Available types: virus, webfilter, waf, ips, anomaly, app-ctrl, emailfilter, dlp, voip, gtp, dns, ssh, ssl, cifs, file-filter")
        click.echo("Enter 'exit' to return to the main menu.")
        type_choice = click.prompt("Enter the type", type=str)
        
        # Check if the user wants to exit
        if type_choice.lower() == 'exit':
            return
        
        base_url_memory = f'https://{management_ip}:{management_port}/api/v2/log/memory/{type_choice}/raw'

        try:
            response = requests.get(base_url_memory, headers={'Authorization': 'Bearer ' + api_token}, verify=False)
            if response.status_code == 200:
                # Print out the response content for debugging
                click.echo("Response content:")
                click.echo(response.content)
            else:
                click.echo(f"Error: {response.text}")
        except requests.exceptions.RequestException as e:
            click.echo(f"Request error occurred: {e}")
        except Exception as e:
            click.echo(f"Error occurred: {e}")

# Function to handle the submenu for Disk logging
def disk_logging_submenu():
    while True:
        click.echo("Disk Logging Submenu:")
        click.echo("Available types: virus, webfilter, waf, ips, anomaly, app-ctrl, emailfilter, dlp, voip, gtp, dns, ssh, ssl, cifs, file-filter")
        click.echo("Enter 'exit' to return to the main menu.")
        type_choice = click.prompt("Enter the type", type=str)
        
        # Check if the user wants to exit
        if type_choice.lower() == 'exit':
            return
        
        base_url_disk = f'https://{management_ip}:{management_port}/api/v2/log/disk/{type_choice}/raw'

        try:
            response = requests.get(base_url_disk, headers={'Authorization': 'Bearer ' + api_token}, verify=False)
            if response.status_code == 200:
                # Print out the response content for debugging
                click.echo("Response content:")
                click.echo(response.content)
            else:
                click.echo(f"Error: {response.text}")
        except requests.exceptions.RequestException as e:
            click.echo(f"Request error occurred: {e}")
        except Exception as e:
            click.echo(f"Error occurred: {e}")


# Function to handle the submenu for network services
def services_network_submenu():
    while True:
        click.echo("Network Services Submenu:")
        click.echo("1. DNS Filter")
        click.echo("2. Routing")
        click.echo("3. VPN")
        click.echo("4. Exit")

        choice = click.prompt("Enter your choice", type=int)
        if choice == 1:
            fetch_dns_filter_info()
        elif choice == 2:
            fetch_routing_statistics()
        elif choice == 3:
            fetch_vpn_info()
        elif choice == 4:
            return
        else:
            click.echo("Invalid choice. Please try again.")

# Submenu for System
def system_submenu():
    click.echo("System Submenu:")
    click.echo("1. License")
    click.echo("2. FortiGuard")
    click.echo("3. Exit")

    choice = click.prompt("Enter your choice", type=int)
    if choice == 1:
        fetch_license_status()
    elif choice == 2:
        fetch_fortiguard_status()
    elif choice == 3:
        return
    else:
        click.echo("Invalid choice. Please try again.")

# Submenu for Switch/WiFi Controller
def switch_wifi_controller_submenu():
    click.echo("Switch/WiFi Controller Submenu:")
    click.echo("1. Fetch Switch Controller Status")
    click.echo("2. Fetch WiFi AP Status")
    click.echo("3. Exit")

    choice = click.prompt("Enter your choice", type=int)
    if choice == 1:
        fetch_switch_controller_status()
    elif choice == 2:
        fetch_wifi_ap_status()
    elif choice == 3:
        return
    else:
        click.echo("Invalid choice. Please try again.")

# Submenu for Services
def services_submenu():
    while True:
        click.echo("Services Submenu:")
        click.echo("1. NTP")
        click.echo("2. DHCP")
        click.echo("3. VOIP")
        click.echo("4. SNMP")
        click.echo("5. DNS")
        click.echo("6. Exit")

        choice = click.prompt("Enter your choice", type=int)
        if choice == 1:
            fetch_ntp_status()
        elif choice == 2:
            fetch_dhcp_status()
        elif choice == 3:
            voip_profile_name = click.prompt("Enter the VOIP profile name", type=str)
            fetch_voip_profile(voip_profile_name)
        elif choice == 4:
            fetch_snmp_status()
        elif choice == 5:
            fetch_dns_status()
        elif choice == 6:
            return
        else:
            click.echo("Invalid choice. Please try again.")

# Submenu for Security
def security_submenu():
    while True:
        click.echo("Security Submenu:")
        click.echo("1. WAF")
        click.echo("2. DLP")
        click.echo("3. IPS")
        click.echo("4. Proxy")
        click.echo("5. Exit")

        choice = click.prompt("Enter your choice", type=int)
        if choice == 1:
            waf_id = click.prompt("Enter the WAF ID", type=int)
            fetch_waf_data(waf_id)
        elif choice == 2:
            dlp_id = click.prompt("Enter the DLP ID", type=int)
            fetch_dlp_data(dlp_id)
        elif choice == 3:
            fetch_ips_anomaly()  # Call function to fetch IPS anomaly data
        elif choice == 4:
            # Call function to handle proxy submenu
            proxy_submenu()
        elif choice == 5:
            return
        else:
            click.echo("Invalid choice. Please try again.")

# Submenu for Proxy
def proxy_submenu():
    while True:
        click.echo("Proxy Submenu:")
        click.echo("1. Download PAC File")
        click.echo("2. Back")

        choice = click.prompt("Enter your choice", type=int)
        if choice == 1:
            fetch_proxy_pac_file()  # Call function to download PAC file
        elif choice == 2:
            return
        else:
            click.echo("Invalid choice. Please try again.")

# Function to handle the submenu for Logging
def logging_submenu(api_token):
    while True:
        click.echo("Logging Submenu:")
        click.echo("1. FortiAnalyzer")
        click.echo("2. FortiCloud")
        click.echo("3. Memory")
        click.echo("4. Disk")
        click.echo("5. Exit")

        choice = click.prompt("Enter your choice", type=int)
        if choice == 1:
            fortianalyzer_logging_submenu()
        elif choice == 2:
            forticloud_logging_submenu()
        elif choice == 3:
            memory_logging_submenu()
        elif choice == 4:
            disk_logging_submenu()
        elif choice == 5:
            return
        else:
            click.echo("Invalid choice. Please try again.")

# Submenu for Users
def users_submenu():
    click.echo("Users Submenu:")
    click.echo("1. Fetch Firewall User Info")
    click.echo("2. Fetch Banned User Info")
    click.echo("3. Exit")

    choice = click.prompt("Enter your choice", type=int)
    if choice == 1:
        fetch_firewall_user_info()
    elif choice == 2:
        fetch_banned_user_info()
    elif choice == 3:
        return
    else:
        click.echo("Invalid choice. Please try again.")

# Main function to handle the menu
@click.command()
def main():
    while True:
        click.echo("""
        ███████╗ ██████╗ ██████╗ ████████╗██╗███╗   ██╗███████╗████████╗
        ██╔════╝██╔═══██╗██╔══██╗╚══██╔══╝██║████╗  ██║██╔════╝╚══██╔══╝
        █████╗  ██║   ██║██████╔╝   ██║   ██║██╔██╗ ██║█████╗     ██║
        ██╔══╝  ██║   ██║██╔══██╗   ██║   ██║██║╚██╗██║██╔══╝     ██║
        ██║     ╚██████╔╝██║  ██║   ██║   ██║██║ ╚████║███████╗   ██║
        ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝
        """)
        click.echo("Welcome to the Fortinet CLI application!\n")
        click.echo("Please select an option:")
        click.echo("1. FortiView")
        click.echo("2. Switch/WiFi Controller")
        click.echo("3. System")
        click.echo("4. Network")
        click.echo("5. Security")
        click.echo("6. Services")
        click.echo("7. Users")
        click.echo("8. Logging")
        click.echo("9. Configuration Backup")
        click.echo("0. Exit")

        choice = click.prompt("Enter your choice", type=int)
        if choice == 1:
            fetch_fortiview_statistics()
        elif choice == 2:
            switch_wifi_controller_submenu()
        elif choice == 3:
            system_submenu()
        elif choice == 4:
            services_network_submenu()  # Call network submenu function
        elif choice == 5:
            security_submenu()  # Call security submenu function
        elif choice == 6:
            services_submenu()  # Call services submenu function
        elif choice == 7:
            users_submenu()
        elif choice == 8:
            api_token = config['API']['token']
            logging_submenu(api_token)  # Pass api_token argument
        elif choice == 9:
            initiate_config_backup()
        elif choice == 0:
            click.echo("Exiting the program.")
            return
        else:
            click.echo("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
