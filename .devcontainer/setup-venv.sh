#!/bin/bash

# python için bir sanal ortam yaratıyor. Böylece kendi belirlediğimiz
# python sürümünü, pip ve diğer kütüphaneleri sistem ari kurup kullanabilirz

# .venv adında bir sanal ortam oluştur
python3 -m venv .venv

# Sanal ortamı etkinleştir
source .venv/bin/activate

# requirements.txt dosyasındaki paketleri yükle
pip install -r requirements.txt