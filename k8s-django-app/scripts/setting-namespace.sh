#!/bin/sh
kubectl config set-context $(kubectl config current-context) --namespace=k8s-django-app-development
