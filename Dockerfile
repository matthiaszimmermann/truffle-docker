FROM phusion/baseimage:focal-1.0.0

RUN rm /bin/sh && ln -s /bin/bash /bin/sh && \
    sed -i 's/^mesg n$/tty -s \&\& mesg n/g' /root/.profile

WORKDIR /app

ENV NVM_DIR /usr/local/nvm
ENV PATH $NVM_DIR/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH

RUN mkdir $NVM_DIR

# install additional packages
RUN apt-get update && apt-get install -y \
    git \
    make \
    iputils-ping \
    tree \
    python3-pip

# install nvm and default node version.
RUN curl https://raw.githubusercontent.com/creationix/nvm/v0.37.2/install.sh | bash && \
    echo 'source $NVM_DIR/nvm.sh' >> /etc/profile

# truffle install based on "mastering ethereum"
RUN /bin/bash -l -c "nvm install --lts"
RUN /bin/bash -l -c "npm -g install truffle"
RUN /bin/bash -l -c "npm install dotenv"

# python web3 install
RUN /bin/bash -l -c "pip3 install web3"

# clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# use baseimage-docker's init system.
CMD ["/sbin/my_init"]