#!/bin/bash

alias ll="ls -al"

# her git komutunda SSH doğrulaması için kullanılacak anahtarı bu repo için aşağıdaki dosya yolundan çek
# git config --add --local core.sshCommand 'ssh -i /workspace/.devcontainer/.ssh/github_id_rsa'
# git commit -am "git config komutu eklendi" && git push

function create_env() {
    # python için bir sanal ortam yaratıyor. Böylece kendi belirlediğimiz
    # python sürümünü, pip ve diğer kütüphaneleri sistem ari kurup kullanabilirz

    # .venv adında bir sanal ortam oluştur
    python3 -m venv .venv

    # sudo chown -R $USER .venv

    # Sanal ortamı etkinleştir
    source .venv/bin/activate

    # Aşağıdaki komut paketleri ".venv/lib64/python3.11/site-packages" adresine yükler
    # pip install -t ../.venv/lib64/python3.11/site-packages -r requirements.txt
}

function install_reqs(){
    # requirements.txt dosyasındaki paketleri yükle
    # Aşağıdaki komut paketleri "/usr/lib/python3/dist-packages" adresine yükler
    pip install -r requirements.txt
}

# create_env
install_reqs