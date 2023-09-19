#!/bin/bash

# .venv adında bir sanal ortam oluştur
python3 -m venv .venv

# Sanal ortamı etkinleştir
source .venv/bin/activate

# requirements.txt dosyasındaki paketleri yükle
pip install -r requirements.txt