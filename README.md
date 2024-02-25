# FG-CLI
#READ ME



FG-CLI (FortiGate Command Line Interface)
FG-CLI is a command-line tool designed to interact with FortiGate devices through their multitude of REST APIs. It provides functionality for configuration, monitoring, and backup of FortiGate devices.


Dependencies

This project relies on several Python libraries to function properly. Before running the script, make sure you have the following libraries installed:

click: Used for creating beautiful command-line interfaces.
configparser: Used for parsing configuration files, such as config.ini.
requests: Used for making HTTP requests to interact with the Fortinet API.
subprocess: Used for spawning new processes, which may be required for certain functionalities.
json: Used for handling JSON data.
Additionally, for the backup2.py script to function correctly, ensure you have the following libraries installed:

os: Used for interacting with the operating system, which may be required for file operations.
You can install these dependencies using pip, the Python package installer, here is an example:
"pip install click"

Make sure to install these dependencies in your Python environment before executing the script or the backup functionality.

Getting Started

Before using FG-CLI, follow these steps to set up and configure the tool:

API User Setup:

Assign an API user on your FortiGate device with the appropriate permissions. This user will be used by FG-CLI to authenticate and access the FortiGate's REST API.

Generate API Token:

Generate an API token for the API user created in step 1. Ensure that you copy the generated token key, as it will be required for configuring FG-CLI.

Configuration:

Update the config.ini file with the following information:
API Token: Paste the API token generated in step 2.
Management IP Address: Enter the IP address of your FortiGate device.
HTTPS Port: Specify the HTTPS port used for API communication with the FortiGate.
Backup Configuration:

Modify the backup2.py file to include the same management IP address and HTTPS port as specified in the config.ini file. This ensures that the backup script communicates with the correct FortiGate device.

Testing:

After configuring config.ini and backup2.py, test the functionality of FG-CLI to ensure proper communication with your FortiGate device.
Usage

Once configured, FG-CLI offers various options for interacting with your FortiGate device:

FortiView: Retrieve FortiView statistics.
Switch/WiFi Controller: Access switch and WiFi controller status.
System: View license status and FortiGuard information.
Network: Explore DNS filtering, routing, and VPN statistics.
Security: Investigate WAF, DLP, IPS, and proxy settings.
Services: Manage NTP, DHCP, VOIP, SNMP, and DNS configurations.
Users: Fetch firewall user information and banned user details.
Logging: Download logs from FortiAnalyzer, FortiCloud, memory, and disk.
Configuration Backup: Initiate configuration backup of the FortiGate device.
