# Kubernetes

## Introduction

* Kubernetes is an open source platform for managing container technologies such as Docker.

* Docker lets you create containers for a pre-configured image and application. 

* Kubernetes provides the next step, allowing you to balance loads between containers and run multiple containers across multiple systems.

**NOTE:** This guide will walk you through how to install Kubernetes on Ubuntu 18.04.

### Prerequisites
* 2 or more Linux servers running Ubuntu 18.04
* Access to a user account on each system with sudo or root privileges
* The apt package manager, included by default
* Command-line/terminal window (Ctrl-Alt-T)

## Steps to Install Kubernetes on Ubuntu

### Set up Docker

**Step 1:** Install Docker

Kubernetes requires an existing Docker installation. If you already have Docker installed, skip ahead to Step 2.

If you do not have Kubernetes, install it by following these steps:

1. Update the package list with the command:
```
sudo apt-get update
```
2. Next, install Docker with the command:
```
sudo apt-get install docker.io
```
3. Repeat the process on each server that will act as a node.

4. Check the installation (and version) by entering the following:
```
docker ––version
```

**Step 2:** Start and Enable Docker

1. Set Docker to launch at boot by entering the following:
```
sudo systemctl enable docker
```
2. Verify Docker is running:
```
sudo systemctl status docker
```
**NOTE:** To start Docker if it’s not running:
```
sudo systemctl start docker
```
3. Repeat on all the other nodes.

### Install Kubernetes

**Step 3:** Add Kubernetes Signing Key

Since you are downloading Kubernetes from a non-standard repository, it is essential to ensure that the software is authentic. This is done by adding a signing key.

1. Enter the following to add a signing key:
```
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add
```
NOTE: If you get an error that curl is not installed, install it with:
```
sudo apt-get install curl
```
2. Then repeat the previous command to install the signing keys. Repeat for each server node.

**Step 4:** Add Software Repositories

Kubernetes is not included in the default repositories. To add them, enter the following:
```
sudo apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"
Repeat on each server node.
```


**Step 5:** Kubernetes Installation Tools

Kubeadm (Kubernetes Admin) is a tool that helps initialize a cluster. It fast-tracks setup by using community-sourced best practices. Kubelet is the work package, which runs on every node and starts containers. The tool gives you command-line access to clusters.

1. Install Kubernetes tools with the command:
```
sudo apt-get install kubeadm kubelet kubectl
sudo apt-mark hold kubeadm kubelet kubectl
```
Allow the process to complete.

2. Verify the installation with:
```
kubeadm version
```
3. Repeat for each server node.

### Kubernetes Deployment

**Step 6:** Begin Kubernetes Deployment
Start by disabling the swap memory on each server:
```
sudo swapoff --a
```

**Step 7:** Assign Unique Hostname for Each Server Node 

Decide which server to set as the master node. Then enter the command:
```
sudo hostnamectl set-hostname master-node
```
Next, set a worker node hostname by entering the following on the worker server:
```
sudo hostnamectl set-hostname worker01
```
If you have additional worker nodes, use this process to set a unique hostname on each.

**Step 8:** Initialize Kubernetes on Master Node
Switch to the master server node, and enter the following:

`sudo kubeadm init --pod-network-cidr=FILL_MASTER_IP_ADDRESS/16`

```
sudo kubeadm init --pod-network-cidr=10.217.70.62/16
```

**Note:** Output

Once this command finishes, it will display a kubeadm join message at the end. Make a note of the whole entry. This will be used to join the worker nodes to the cluster.

```
Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 10.217.70.62:6443 --token 4j9b95.1cdx9tadejremcm9 \
    --discovery-token-ca-cert-hash sha256:6c136ea5116ea3cdcbcdc9e7fa0eb941f16ed85ca5e67c73b2d3f9b1e56fc2ea 
```


Next, enter the following to create a directory for the cluster:
```
kubernetes-master:~$ mkdir -p $HOME/.kube
kubernetes-master:~$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
kubernetes-master:~$ sudo chown $(id -u):$(id -g) $HOME/.kube/config
```


**Step 9:** Deploy Pod Network to Cluster

A Pod Network is a way to allow communication between different nodes in the cluster. This tutorial uses the flannel virtual network.

Enter the following:
```
sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```
Allow the process to complete.
Verify that everything is running and communicating:
```
kubectl get pods --all-namespaces
```


**Step 10:** Join Worker Node to Cluster

As indicated in Step 7, you can enter the kubeadm join command on each worker node to connect it to the cluster.
Switch to the worker01 system and enter the command you noted from Step 7:

```
kubeadm join 10.217.70.62:6443 --token 4j9b95.1cdx9tadejremcm9 \
    --discovery-token-ca-cert-hash sha256:6c136ea5116ea3cdcbcdc9e7fa0eb941f16ed85ca5e67c73b2d3f9b1e56fc2ea 
```

Replace the alphanumeric codes with those from your master server. Repeat for each worker node on the cluster. Wait a few minutes; then you can check the status of the nodes.

Switch to the master server, and enter:
```
kubectl get nodes
```
The system should display the worker nodes that you joined to the cluster.
