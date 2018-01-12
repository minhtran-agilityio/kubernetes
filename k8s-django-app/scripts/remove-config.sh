#!/bin/sh
kubectl delete -f development/deployment -f development/secret -f development/configmap -f development/ingress -f development/volume -f development/service -f development/namespace --recursive
