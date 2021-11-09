#! /bin/bash

docker run --privileged --rm --memory="6m" --memory-swap="6m" -v "$(pwd):/opt" -w /opt baseline ./constrained_encrypt2 $@

