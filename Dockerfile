ARG CPU
FROM ${CPU}/ubuntu
ARG CPU

# install deb packages for machine learning
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install software-properties-common openssh-server wget vim nodejs npm -y

# install pip
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install python3-pip -y

# install modules for machine learning
RUN python3 -m pip install matplotlib scikit-learn scipy plotly ipywidgets prophet scikit-image imgaug albumentations Augmentor pillow jupyterlab jupyterhub --break-system-packages
RUN npm install -g configurable-http-proxy
RUN jupyterhub --generate-config

# set for connecting to ssh
RUN mkdir /var/run/sshd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' \
    /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional \
    pam_loginuid.so@g' -i /etc/pam.d/sshd

# copy source code
COPY . /machine-learning-lecture
RUN rm -rf /machine-learning-lecture/.git

# set jupyter
RUN echo 'c.Authenticator.allow_all = True' | tee -a /jupyterhub_config.py

# service start ssh
# add user
COPY service /
# set execute
RUN chmod +x /service

EXPOSE 22
CMD ["/bin/bash", "-c", "/service; /bin/bash"]