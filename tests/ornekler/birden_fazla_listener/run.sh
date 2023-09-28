#!/bin/bash

cd tests/ornekler/birden_fazla_listener

robot --listener ./KiwiListener.py --listener ./AnalizciListener.py ./bir.robot ./iki.robot
# Etikete göre test koş
# robot -d ./output -P ./ -P ./resources -P ./tests/KT-TESTS --listener kiwi.KiwiListener  -v TEST_ID:KT_CN_001 -i listener .
# /home/vscode/.local/bin/robot -P ./tests/ornekler/birden_fazla_listener/ -P ./tests/KT-TESTS --listener ListenerKiwi -i listener .