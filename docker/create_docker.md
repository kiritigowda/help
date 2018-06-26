# Create a docker image

## Prerequisites
* Docker Hub Account - {dockerhub_username}
* Docker installed on your ubuntu machine

## Step 1: Starting from an Ubuntu Image

* Pull offical ubuntu docker from docker hub.

````
sudo docker pull ubuntu:16.04
````
* Ubuntu docker hub repo has many versions available, use the image and tag which is required.

## Step 2: Run the docker image

````
sudo docker run -it {USER_OPTIONS} --group-add video --network host ubuntu:16.04
````
* Running the docker image with different user options, lets docker access different resources.
* Review the user options using the following commands
````
 man docker
````
* --groups-add video - adds you to the video group, --network host - allows you to access host network

## Step 3: Install software or make changes to your docker image

* Now you can change the docker image from within to include the software or changes to the settings
* Inside the docker, use it as a normal ubuntu machine terminal

## Step 4: Save changes on the docker

* Open another terminal on the host machine
* Check which docker images are currently in use, the below commands lists all docker in use
````
sudo docker ps
````
* Now select the docker your are working on by noting the container id
* Commit your changes to your docker
````
sudo docker commit {container_id} {dockerhub_username}/{docker_name_you_want}:{tag}
````

## Step 5: Push docker image to your docker hub

````
sudo docker push {dockerhub_username}/{docker_name_you_want}:{tag}
````
* Now the docker image is available on docker hub.
* Check in help can be found using the following command
````
docker push --help
````
