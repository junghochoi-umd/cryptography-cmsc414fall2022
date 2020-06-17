#! /bin/bash

docker run --privileged --rm --memory="4m" --memory-swap="4m" -v "$(pwd):/opt" -w /opt baseline ./constrained_encrypt2 $@

