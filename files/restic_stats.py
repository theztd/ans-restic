#!/usr/bin/env python3


from os import path
from time import time
from sys import argv
import json

def logI(msg):
    print("INFO: ", msg)

def logE(msg):
    print("ERR: ", msg)

def file_age_in_min(file_path):
    try:
        return int((time() - path.getmtime(file_path)) / 60)

    except IOError as err:
        logE(err)
        return 0


def restic_get_summary(file_path):
    try:
        with open(file_path, "r") as fsum_in:
            return json.load(fsum_in)

    except IOError as err:
        logE(err)
        return {}



if __name__ == "__main__":
    job_name = argv[1]
    file_age = file_age_in_min(argv[2])

    # if the source file is newer than 3O minutes regenerate snapshot stats
    if file_age < 30:
        data = restic_get_summary(argv[2])
        print(f"""# Restic last snapshot stats
restic_stats_backup_duration{{backup_job="{job_name}", snapshot_id="{data['snapshot_id']}"}} {data['total_duration']}
restic_stats_data_added{{backup_job="{job_name}", snapshot_id="{data['snapshot_id']}"}} {data['data_added']}
restic_stats_bytes_processed{{backup_job="{job_name}", snapshot_id="{data['snapshot_id']}"}} {data['total_bytes_processed']}
restic_stats_files_unmodified{{backup_job="{job_name}", snapshot_id="{data['snapshot_id']}"}} {data['files_unmodified']}
restic_stats_files_changed{{backup_job="{job_name}", snapshot_id="{data['snapshot_id']}"}} {data['files_changed']}
restic_stats_files_new{{backup_job="{job_name}", snapshot_id="{data['snapshot_id']}"}} {data['files_new']}
restic_stats_dirs_unmodified{{backup_job="{job_name}", snapshot_id="{data['snapshot_id']}"}} {data['dirs_unmodified']}
restic_stats_dirs_changed{{backup_job="{job_name}", snapshot_id="{data['snapshot_id']}"}} {data['dirs_changed']}
restic_stats_dirs_new{{backup_job="{job_name}", snapshot_id="{data['snapshot_id']}"}} {data['dirs_new']}
        """)

    print(f"""# Restic general stats
restic_stats_last_snapshot_age{{backup_job="{job_name}"}} {file_age}
""")
