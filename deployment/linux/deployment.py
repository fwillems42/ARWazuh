import os
import subprocess
import platform
import shutil


def git_clone(repository_url, folder_name):
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        if os.path.exists(folder_name):
            print("Repository already exists. Pulling latest changes...")
            result = subprocess.run(["git", "pull"], cwd=folder_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    check=False)
            changes_detected = "Already up to date" not in result.stdout.decode()
        else:
            print("Cloning repository...")
            result = subprocess.run(["git", "clone", repository_url, folder_name], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, check=True)
            changes_detected = True

        return changes_detected
    except subprocess.CalledProcessError as e:
        print("Git command failed:", e)
        exit(1)
    except FileNotFoundError:
        print("Git is not installed. Please install Git and try again.")
        exit(1)
    except Exception as e:
        print("Error:", e)


def deploy_on_windows(repository_url, folder_name):
    try:
        install_dir = "C:\\Program Files (x86)\\ossec-agent\\install"
        if not os.path.exists(install_dir):
            os.mkdir(install_dir)

        os.chdir(install_dir)
        changes_detected = git_clone(repository_url, folder_name)

        if changes_detected:
            print("Deploying on Windows...")

            src_scripts = "scripts\\windows"
            dst_scripts = "C:\\Program Files (x86)\\ossec-agent\\active-response\\bin"

            copy_script_to_ar_directory(folder_name, src_scripts, dst_scripts)

        create_windows_scheduled_task(install_dir)
    except Exception as e:
        print("Error:", e)


def deploy_on_linux(repository_url, folder_name):
    try:
        install_dir = "/var/ossec/install"
        if not os.path.exists(install_dir):
            os.mkdir(install_dir)

        os.chdir(install_dir)
        changes_detected = git_clone(repository_url, folder_name)

        if changes_detected:
            print("Deploying on Linux...")

            linux_dir = "scripts/linux"
            destination_dir = "/var/ossec/active-response/bin"

            copy_script_to_ar_directory(folder_name, src_scripts, dst_scripts)

        create_linux_scheduled_task(install_dir)
    except Exception as e:
        print("Error:", e)


def deploy_on_darwin(repository_url, folder_name):
    try:
        install_dir = "/Library/Ossec/install"
        if not os.path.exists(install_dir):
            os.mkdir(install_dir)

        os.chdir(install_dir)
        changes_detected = git_clone(repository_url, folder_name)

        if changes_detected:
            print("Deploying on macOS...")

            macos_dir = "scripts/macos"
            destination_dir = "/Library/Ossec/active-response/bin"

            copy_script_to_ar_directory(folder_name, src_scripts, dst_scripts)

        create_macos_scheduled_task(install_dir)
    except Exception as e:
        print("Error:", e)


def create_windows_scheduled_task(install_dir):
    task_command = f"{install_dir}\\deployment\\deployment.exe"

    task_name_daily = "ARUpdateDaily"
    task_trigger_daily = "daily"
    task_start_time_daily = "00:00"

    task_name_startup = "ARUpdateOnStart"
    task_trigger_startup = "onstart"

    command_daily = f"schtasks /create /tn {task_name_daily} /tr {task_command} /sc {task_trigger_daily} /st {task_start_time_daily}"
    command_startup = f"schtasks /create /tn {task_name_startup} /tr {task_command} /sc {task_trigger_startup}"

    try:
        subprocess.run(command_daily, shell=True, check=True)
        subprocess.run(command_startup, shell=True, check=True)

        print("Windows scheduled tasks created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating scheduled task: {e}")


def create_linux_scheduled_task(install_dir):
    try:
        cron_command_midnight = f"(crontab -l ; echo '0 0 * * * python3 {install_dir}/deployment/deployment.py') | crontab -"
        os.system(cron_command_midnight)

        cron_command_reboot = f"(crontab -l ; echo '@reboot python3 {install_dir}/deployment/deployment.py') | crontab -"
        os.system(cron_command_reboot)

        print("Linux scheduled tasks created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating scheduled task: {e}")

def create_macos_scheduled_task(install_dir):
    raise Exception("Macos scheduled tasks are not implemented")

def check_windows_scheduled_task(task_name):
    try:
        subprocess.run(f"schtasks /query /tn {task_name}", shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def check_linux_scheduled_task(task_command):
    try:
        crontab = os.popen('crontab -l').read()
        return task_command in crontab
    except Exception as e:
        print("Error:", e)

def check_darwin_schedules_task(task_name):
    raise Exception("Macos scheduled tasks are not implemented")

def copy_script_to_ar_directory(folder_name, src_scripts, dst_scripts):
    os.chdir(folder_name)
    if os.path.exists(src_scripts):
        for item in os.listdir(src_scripts):
            item_path = os.path.join(src_scripts, item)
            if os.path.isfile(item_path):
                shutil.copy(item_path, dst_scripts)

def main():
    repository_url = "https://github.com/fwillems42/ARWazuh"
    folder_name = "ARWazuh"

    # Determine the platform and deploy accordingly
    current_platform = platform.system()
    if current_platform == "Windows":
        deploy_on_windows(repository_url, folder_name)
    elif current_platform == "Linux":
        deploy_on_linux(repository_url, folder_name)
    elif current_platform == "Darwin":
        deploy_on_darwin(repository_url, folder_name)
    else:
        print("Unsupported platform:", current_platform)


if __name__ == '__main__':
    main()
