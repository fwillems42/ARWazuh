import os
import subprocess
import platform
import shutil
import sys


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
        sys.exit(1)
    except FileNotFoundError:
        print("Git is not installed. Please install Git and try again.")
        sys.exit(1)
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

            src_scripts = "scripts/linux"
            dst_scripts = "/var/ossec/active-response/bin"

            copy_script_to_ar_directory(folder_name, src_scripts, dst_scripts)

            src_api = os.path.join(install_dir, folder_name, 'api')
            dst_api = os.path.join(dst_scripts, 'api')
            shutil.copytree(src_api, dst_api)

            src_domain = os.path.join(install_dir, folder_name, 'domain')
            dst_domain = os.path.join(dst_scripts, 'domain')
            shutil.copytree(src_domain, dst_domain)

        create_linux_scheduled_task(install_dir)

        venv_dir = os.path.join(install_dir, 'venv')
        subprocess.run(["python3", "-m", "venv", venv_dir], check=True)

        activate_script = os.path.join(venv_dir, "bin", "activate")
        activate_cmd = f"source {activate_script}"
        subprocess.run(["/bin/bash", "-c", activate_cmd], check=True)

        requirements = os.path.join(install_dir, folder_name, 'requirements.txt')
        subprocess.run(["pip", "install", "-r", requirements])
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

            src_scripts = "scripts/macos"
            dst_scripts = "/Library/Ossec/active-response/bin"

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
        task_count = 0
        if not check_windows_scheduled_task(task_name_daily):
            subprocess.run(command_daily, shell=True, check=True)
            task_count += 1

        if not check_windows_scheduled_task(task_name_startup):
            subprocess.run(command_startup, shell=True, check=True)
            task_count += 1

        if task_count > 0:
            print("Windows scheduled tasks created successfully.")
        else:
            print("Windows scheduled tasks are already present.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating scheduled task: {e}")


def create_linux_scheduled_task(install_dir):
    cron_command_midnight = f"(crontab -l ; echo '0 0 * * * python3 {install_dir}/deployment/deployment.py') | crontab -"
    cron_command_reboot = f"(crontab -l ; echo '@reboot python3 {install_dir}/deployment/deployment.py') | crontab -"

    try:
        task_count = 0
        if not check_linux_scheduled_task(f'0 0 * * * python3 {install_dir}/deployment/deployment.py'):
            os.system(cron_command_midnight)
            task_count += 1

        if not check_linux_scheduled_task(f'@reboot python3 {install_dir}/deployment/deployment.py'):
            os.system(cron_command_reboot)
            task_count += 1

        if task_count > 0:
            print("Linux scheduled tasks created successfully.")
        else:
            print("Linux scheduled tasks are already present.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating scheduled task: {e}")


def create_macos_scheduled_task(install_dir):
    raise Exception("Macos scheduled tasks are not yet implemented")


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
    raise Exception("Macos scheduled tasks are not yet implemented")


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
