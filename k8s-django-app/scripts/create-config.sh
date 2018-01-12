#!/bin/sh
kubectl create -f development/namespace -f development/secret -f development/configmap -f development/volume -f development/deployment -f development/service -f development/ingress --recursive
