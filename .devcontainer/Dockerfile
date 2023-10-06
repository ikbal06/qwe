FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Ansible kurulu gelsin
RUN apt-get update 
RUN DEBIAN_FRONTEND=noninteractive apt install -y ansible sshpass
RUN ssh-keygen -q -t rsa -N '' -f /root/.ssh/id_rsa

