import subprocess
import os
import platform
import shutil


def git_clone(repository_url, folder_name):
    if os.path.exists(folder_name):
        print("Repository already exists. Pulling latest changes...")
        subprocess.run(["git", "pull"], cwd=folder_name)
    else:
        print("Cloning repository...")
        subprocess.run(["git", "clone", repository_url, folder_name])


def deploy_on_windows():
    print("Deploying on Windows...")
    # Copy scripts from 'windows' directory to destination
    windows_dir = "windows"
    destination_dir = "C:\\Program Files (x86)\\ossec-agent\\active-response\\bin"
    if os.path.exists(windows_dir):
        for item in os.listdir(windows_dir):
            item_path = os.path.join(windows_dir, item)
            if os.path.isfile(item_path):
                shutil.copy(item_path, destination_dir)


def deploy_on_linux():
    print("Deploying on Linux...")
    # Copy Python scripts from 'linux' directory to destination
    linux_dir = "linux"
    destination_dir = "/var/ossec/active-responses/bin"
    if os.path.exists(linux_dir):
        for item in os.listdir(linux_dir):
            item_path = os.path.join(linux_dir, item)
            if os.path.isfile(item_path):
                shutil.copy(item_path, destination_dir)


def deploy_on_mac():
    print("Deploying on macOS...")
    # Copy scripts from 'macos' directory to destination
    macos_dir = "macos"
    destination_dir = "/Library/Ossec/active-response/bin"
    if os.path.exists(macos_dir):
        for item in os.listdir(macos_dir):
            item_path = os.path.join(macos_dir, item)
            if os.path.isfile(item_path):
                shutil.copy(item_path, destination_dir)


def main():
    repository_url = "https://github.com/fwillems42/ARWazuh"
    repository_folder = "ARWazuh"

    # Clone or pull the repository
    git_clone(repository_url, repository_folder)

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
