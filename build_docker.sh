#!/bin/bash
uid=$(eval "id -u")
gid=$(eval "id -g")
docker build --build-arg UID="$uid" --build-arg GID="$gid" --build-arg DOMAIN_ID=0 --build-arg CACHE_BUST="$(date +%s)" -t llm_docker .