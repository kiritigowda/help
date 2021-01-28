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
sudo docker pull kiritigowda/ubuntu_16.04.3
````

## Step 3 - *Run the docker image*
````
sudo docker run -it --group-add video --network host kiritigowda/ubuntu_16.04.3
````


# Docker Commands

1. View docker images in use
````
sudo docker ps
````
2. View all docker images on the system
````
sudo docker images
````
3. Remove docker images
````
sudo docker rm $(sudo docker ps -aq)
````

```
sudo docker image prune --all --filter "until=1500h"
```

4. Run Camera from docker

````
sudo docker run -it 
-v /home/kiriti/:/root/hostDrive/ 
-v /dev/video0:/dev/video0 
-v /tmp/.X11-unix:/tmp/.X11-unix 
--volume="$HOME/.Xauthority:/root/.Xauthority:rw" 
-e "PACKAGES=ffmpeg" 
-e DISPLAY=$DISPLAY  
-e DISPLAY  
--device=/dev/kfd 
--device=/dev/dri 
--device=/dev/mem 
--device /dev/video0 
--device /dev/snd 
--cap-add=SYS_RAWIO 
--group-add video 
--network host 
--env="DISPLAY" 
kiritigowda/annie
````
