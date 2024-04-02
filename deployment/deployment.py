import os
import subprocess
import platform
import shutil


def git_clone(repository_url, folder_name):
    try:
        if os.path.exists(folder_name):
            print("Repository already exists. Pulling latest changes...")
            subprocess.run(["git", "pull"], cwd=folder_name, check=True)
        else:
            print("Cloning repository...")
            subprocess.run(["git", "clone", repository_url, folder_name], check=True)
    except subprocess.CalledProcessError as e:
        print("Error:", e)


def deploy_on_windows():
    try:
        print("Deploying on Windows...")
        # Copy scripts from 'windows' directory to destination
        windows_dir = "scripts\\windows"
        destination_dir = "C:\\Program Files (x86)\\ossec-agent\\active-response\\bin"
        if os.path.exists(windows_dir):
            for item in os.listdir(windows_dir):
                item_path = os.path.join(windows_dir, item)
                if os.path.isfile(item_path):
                    shutil.copy(item_path, destination_dir)
    except Exception as e:
        print("Error:", e)


def deploy_on_linux():
    try:
        print("Deploying on Linux...")
        # Copy Python scripts from 'linux' directory to destination
        linux_dir = "scripts/linux"
        destination_dir = "/var/ossec/active-response/bin"
        if os.path.exists(linux_dir):
            for item in os.listdir(linux_dir):
                item_path = os.path.join(linux_dir, item)
                if os.path.isfile(item_path):
                    shutil.copy(item_path, destination_dir)
    except Exception as e:
        print("Error:", e)


def deploy_on_mac():
    try:
        print("Deploying on macOS...")
        # Copy scripts from 'macos' directory to destination
        macos_dir = "scripts/macos"
        destination_dir = "/Library/Ossec/active-response/bin"
        if os.path.exists(macos_dir):
            for item in os.listdir(macos_dir):
                item_path = os.path.join(macos_dir, item)
                if os.path.isfile(item_path):
                    shutil.copy(item_path, destination_dir)
    except Exception as e:
        print("Error:", e)


def main():
    repository_url = "https://github.com/fwillems42/ARWazuh"
    repository_folder = "ARWazuh"

    # Clone or pull the repository
    git_clone(repository_url, repository_folder)
    os.chdir(repository_folder)

    # Determine the platform and deploy accordingly
    current_platform = platform.system()
    if current_platform == "Windows":
        deploy_on_windows()
    elif current_platform == "Linux":
        deploy_on_linux()
    elif current_platform == "Darwin":
        deploy_on_mac()
    else:
        print("Unsupported platform:", current_platform)


if __name__ == "__main__":
    main()
