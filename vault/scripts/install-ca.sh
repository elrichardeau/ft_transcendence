#!/usr/bin/env bash

if [ ! -f "./vault/ca/init" ]; then
  if [ "$(uname)" == "Darwin" ]; then
    sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ./vault/ca/transcendence_ca.crt
    sudo security add-trusted-cert -d -r trustAsRoot -k /Library/Keychains/System.keychain ./vault/ca/transcendence.crt
    touch ./vault/ca/init
  elif [ "$(uname -a | grep "microsoft")" ]; then
    gsudo certutil.exe -addstore root ./vault/ca/transcendence_ca.crt
    gsudo certutil.exe -addstore ca ./vault/ca/transcendence.crt
    sudo touch ./vault/ca/init
  elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    sudo cp ./vault/ca/transcendence_ca.crt /usr/local/share/ca-certificates
    sudo cp ./vault/ca/transcendence.crt /usr/local/share/ca-certificates
    sudo update-ca-certificates
    sudo touch ./vault/ca/init
  fi
fi

