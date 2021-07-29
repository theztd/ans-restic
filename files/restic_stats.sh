#!/bin/bash -l

LOGS_DIR=$1
METRICS_DIR=$2

# Check if logs path exists
[ -d ${LOGS_DIR} ] || exit 0

for f in ${LOGS_DIR}/summary-*.json; do
    job_name=$(basename ${f} | sed 's/summary-//g' | sed 's/.json//g')
    echo "Processing: /usr/local/bin/restic_stats.py ${job_name} ${f}"
    /opt/restic/restic_stats.py ${job_name} ${f} > ${METRICS_DIR}/restic_stats_${job_name}.prom
done