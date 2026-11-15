#!/bin/sh
set -e
kind create cluster --name todo --config kind/kind-config.yaml
for node in $(kind get nodes --name todo); do
  docker exec "$node" mkdir -p /etc/containerd/certs.d/localhost:5000
  echo '[host."http://registry:5000"]' | docker exec -i "$node" \
    cp /dev/stdin /etc/containerd/certs.d/localhost:5000/hosts.toml
done
docker network connect kind registry || true