FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye
RUN pip install robotframework
RUN apt-get update 
RUN DEBIAN_FRONTEND=noninteractive apt install -y ansible

USER vscode
# VSIX dosyalarını kopyala
COPY ./uzantilar/*.vsix /tmp/

# Otomatize betiği kopyala ve çalıştır
COPY install_extensions.py /tmp/
RUN python /tmp/install_extensions.py

