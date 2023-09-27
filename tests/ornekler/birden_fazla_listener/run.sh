#!/bin/bash

cd tests/ornekler/birden_fazla_listener

robot --listener ./KiwiListener.py --listener ./AnalizciListener.py ./bir.robot ./iki.robot
# Etikete göre test koş
# robot -d ./output -P ./ -P ./libraries -P ./tests/KT-TESTS -P ./resources --listener kiwi.KiwiListener  -v TEST_ID:KT_CN_001 -i listener .