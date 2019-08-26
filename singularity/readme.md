# Singularity

Singularity enables users to have full control of their environment. Singularity containers can be used to package 
entire scientific workflows, software and libraries, and even data. This means that you don’t have to ask your 
cluster admin to install anything for you - you can put it in a Singularity container and run. 
Did you already invest in Docker? The Singularity software can import your Docker images without having 
Docker installed or being a superuser. Need to share your code? Put it in a Singularity container and 
your collaborator won’t have to go through the pain of installing missing dependencies. 

Do you need to run a different operating system entirely? You can “swap out” the operating system on your host for 
a different one within a Singularity container. As the user, you are in control of the extent to which your container 
interacts with its host. There can be seamless integration, or little to no communication at all.

### Install Dependencies

#### Install base deps with `apt-get` or `yum`

* `apt-get`
  
```
sudo apt-get update && sudo apt-get install -y build-essential libssl-dev uuid-dev libgpgme11-dev squashfs-tools libseccomp-dev pkg-config
```

* `yum`

````
sudo yum update -y && sudo yum groupinstall -y 'Development Tools' && sudo yum install -y openssl-devel libuuid-devel libseccomp-devel wget squashfs-tools
````

#### Install Go

* Install Go with wget

````
wget https://dl.google.com/go/go1.12.9.linux-amd64.tar.gz && \
    sudo tar -C /usr/local -xzvf go1.12.9.linux-amd64.tar.gz && \
    rm go1.12.9.linux-amd64.tar.gz
````

* Set up environment for Go
````
echo 'export GOPATH=${HOME}/go' >> ~/.bashrc && \
    export PATH=$PATH:/usr/local/go/bin && \
    echo 'export PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin' >> ~/.bashrc && \
    source ~/.bashrc
````

### Install Singularity

* Download and install Singularity from a release

```
cd && \
    wget https://github.com/sylabs/singularity/releases/download/v3.3.0/singularity-3.3.0.tar.gz && \
    tar -xzf singularity-3.3.0.tar.gz && \
    cd singularity && \
    ./mconfig && \
    cd builddir && make && \
    sudo make install && rm -rf ../../singularity-3.3.0.tar.gz
```
