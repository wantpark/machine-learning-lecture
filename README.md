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
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
nvm install 20
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
CREATE DATABASE IF NOT EXISTS mobiusdb;
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

### Jetson nano

```shell
sudo apt-get update
sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran -y

sudo apt-get install python3-pip -y
sudo pip3 install -U pip testresources setuptools==49.6.0

sudo pip3 install -U --no-deps numpy==1.19.4 future==0.18.2 mock==3.0.5 keras_preprocessing==1.1.2 keras_applications==1.0.8 gast==0.4.0 protobuf pybind11 cython pkgconfig packaging
sudo env H5PY_SETUP_REQUIRES=0 pip3 install -U h5py==3.1.0

sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v461 tensorflow
sudo pip3 install -U pillow keras==2.6
```
