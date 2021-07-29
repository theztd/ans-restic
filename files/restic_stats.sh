#!/bin/bash -l

# Check if logs path exists
[ -d /var/log/restic/ ] || exit 0


for f in /var/log/restic/summary-*.json; do
    echo "${f}"
done

