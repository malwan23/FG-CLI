import os
import configparser
import subprocess

def install_dependencies():
    print("Installing required Python libraries...")
    try:
        subprocess.run(["pip", "install", "requests", "click"])
        print("Dependencies installed successfully.")
    except Exception as e:
        print(f"Error installing dependencies: {e}")

def get_user_input():
    api_token = input("Enter your API key: ")
    management_ip = input("Enter the Management IP address: ")
    management_port = input("Enter the HTTPs port: ")

    return api_token, management_ip, management_port

def update_config_ini(api_token, management_ip, management_port):
    config = configparser.ConfigParser()
    config['API'] = {
        'token': api_token,
        'management_ip': management_ip,
        'management_port': management_port
    }

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("Configuration updated successfully.")

def main():
    install_dependencies()
    print("\nWelcome to the Fortinet CLI Tool Installation Wizard!\n")
    print("Please provide the following information:")
    api_token, management_ip, management_port = get_user_input()
    update_config_ini(api_token, management_ip, management_port)
    print("\nInstallation and configuration completed successfully.")

if __name__ == "__main__":
    main()
