# How to produce windows executable

1. Install pyinstaller using the following command

```shell
pip install pyinstaller
```

2. Activate our environment

```
.\env\ar\Scripts\activate
```

3. Package the script into an executable

```shell
pyinstaller -F <your_python_script>.py -n <output_name>

# for more complicated scripts :
pyinstaller --onefile --add-data "domain;domain" --add-data "api;api" --workpath .\build\ban_ip_pfsense\ --distpath .\scripts\windows\ .\scripts\linux\ban-ip-pfsense.py

```

0. How to generate deployment script for windows
```shell
.\env\ar\Scripts\activate
pyinstaller.exe --onefile --workpath .\build\deployment\ --distpath .\deployment\windows\ .\deployment\linux\deployment.py
```
