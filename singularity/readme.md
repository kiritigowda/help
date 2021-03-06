# Singularity

Singularity is a free, cross-platform and open-source computer program that performs operating-system-level virtualization also known as containerization. One of the main uses of Singularity is to bring containers and reproducibility to scientific computing and the high-performance computing (HPC) world. Using Singularity containers, developers can work in reproducible environments of their choosing and design, and these complete environments can easily be copied and executed on other platforms.

Singularity enables users to have full control of their environment. Singularity containers can be used to package 
entire scientific workflows, software and libraries, and even data. This means that you don’t have to ask your 
cluster admin to install anything for you - you can put it in a Singularity container and run.

Did you already invest in Docker? The Singularity software can import Docker images without having 
Docker installed or being a superuser. Need to share your code? Put it in a Singularity container and 
your collaborator won’t have to go through the pain of installing missing dependencies. 

Do you need to run a different operating system entirely? You can “swap out” the operating system on your host for 
a different one within a Singularity container. As the user, you are in control of the extent to which your container 
interacts with its host. There can be seamless integration, or little to no communication at all.

Research clusters do not allow Dockers and virtual machines because it introduces huge security issues.

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
    sudo make install && rm -rf ../../singularity-3.3.0.tar.gz && cd
```
## Singularity WorkFlow


### Build
* Build from docker
````
sudo singularity build ubuntu-18.04.simg docker://kiritigowda/ubuntu-18.04:latest
````
* Build from library
````
sudo singularity build ubuntu.simg library://kiritigowda/default/ubuntu-18.04:latest
````
### Secure Images

* Authenticate
````
sudo singularity sign ubuntu-18.04.simg
````
* Verify
````
sudo singularity verify ubuntu-18.04.simg
````
### Shell 

````
sudo singularity shell ubuntu-18.04.simg
````
* export QT_X11_NO_MITSHM=1
* export LC_ALL=C; unset LANGUAGE
