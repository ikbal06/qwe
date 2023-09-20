#!/bin/bash

alias ll="ls -al"

function create_env() {
    # python için bir sanal ortam yaratıyor. Böylece kendi belirlediğimiz
    # python sürümünü, pip ve diğer kütüphaneleri sistem ari kurup kullanabilirz

    # .venv adında bir sanal ortam oluştur
    python3 -m venv .venv

    # sudo chown -R $USER .venv

    # Sanal ortamı etkinleştir
    source .venv/bin/activate

    # requirements.txt dosyasındaki paketleri yükle
    # Aşağıdaki komut paketleri "/usr/lib/python3/dist-packages" adresine yükler
    pip install -r requirements.txt

    # Aşağıdaki komut paketleri ".venv/lib64/python3.11/site-packages" adresine yükler
    # pip install -t ../.venv/lib64/python3.11/site-packages -r requirements.txt
}

# create_env