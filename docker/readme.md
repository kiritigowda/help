# Docker

## Prerequisites for docker
* ubuntu 16.04.3 LTS

## Step 1 - *Setup Docker*
````
sudo apt-get install curl
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
apt-cache policy docker-ce
sudo apt-get install -y docker-ce
sudo systemctl status docker
````

## Step 2 - *Get Docker Image*
````
sudo docker pull kiritigowda/ubuntu_16.04.3:amdovx-drop
````

## Step 3 - *Run the docker image*
````
sudo docker run -it --device=/dev/kfd --device=/dev/dri --group-add video --network host kiritigowda/ubuntu_16.04.3:amdovx-drop
````
