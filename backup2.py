#backup2.py

import requests
import os
import configparser  

# Read the API token from the config.ini file
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
api_token = config['API']['token']

api_url = f'https://{INSERT_IP_HERE:MGMT_PORT}/api/v2/monitor/system/config/backup?scope=global&access_token={api_token}'

requests.packages.urllib3.disable_warnings()

data = requests.get(api_url, verify=False)

# Save the backup file in the same directory as the script
backup_file_path = os.path.join(os.path.dirname(__file__), 'backup.conf')
with open(backup_file_path, 'wb') as f:
    for line in data:
        f.write(line)
