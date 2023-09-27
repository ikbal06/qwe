#!/bin/bash

cd tests/ornekler/birden_fazla_listener

robot --listener ./KiwiListener.py --listener ./AnalizciListener.py ./bir.robot ./iki.robot