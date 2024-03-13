# How to produce windows executable

First we need to install pyinstaller using the following command :

```shell
pip install pyinstaller
```

Then we need to use the following command to package the script into an executable :

```shell
pyinstaller -F <your_python_script>.py -n <output_name>
```

