# IoT platform

## Server

```text
Ubuntu Server 20.04
```

### Select default all except ssh

```text
[x] Install OpenSSH server
```

### Install development tools

```shell
sudo apt-get update
sudo apt-get install build-essential -y
```

### Install pip

```shell
sudo apt-get install python3-pip -y
```

## MQTT

```shell
sudo apt-get install mosquitto mosquitto-clients -y
sudo systemctl enable mosquitto
```

## MySQL

```shell
sudo apt install mysql-server -y
sudo mysql
```

### Set root password

```mysql
mysql> UPDATE mysql.user SET authentication_string=null WHERE User='root';
mysql> FLUSH PRIVILEGES;
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'P@ssw0rd';
mysql> FLUSH PRIVILEGES;
mysql> exit
```

## oneM2M

### Install Node.js

```shell
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
source ~/.bashrc
nvm install 16
```

### Install Mobius

```shell
git clone https://github.com/IoTKETI/Mobius
cd Mobius
npm install
```

### Set database

```shell
vi mobius/mobiusdb.sql
- CREATE DATABASE IF NOT EXISTS mobiusdb;
USE mobiusdb;
sudo mysql -u root -p < mobius/mobiusdb.sql
vi mobius.js
- line 25 conf.dbpass = "P@ssw0rd";
```

### Execute oneM2M

```shell
node mobius.js
```

## Jupyter

```shell
python3 -m pip install jupyterlab plotly ipywidgets
jupyter labextension install jupyterlab-plotly
source ~/.profile
```

### Set default password

```shell
jupyter notebook --generate-config
jupyter notebook password
Enter password: 1
Verify password: 1
vi ~/.jupyter/jupyter_notebook_config.py
- c.NotebookApp.ip = '*'
- c.NotebookApp.open_browser = False
```

### Execute Jupyter

```shell
jupyter-lab
```

## Time-series tools

### Prophet

```shell
python3 -m pip install pystan==2.19.1.1
python3 -m pip install prophet
```

### SciPy

```shell
python3 -m pip install scipy
```

## Image tools

### scikit-learn

```shell
python3 -m pip install scikit-image
```

### Data Augmentation

```shell
python3 -m pip install scikit-learn imgaug albumentations Augmentor
```
