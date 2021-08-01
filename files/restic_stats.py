#!/usr/bin/env python3


from os import path
from time import time
from sys import argv
import json
from json.decoder import JSONDecodeError

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

    except JSONDecodeError as err:
        logE("JSONDecodeError " + str(err))
        return {}


if __name__ == "__main__":
    stats_file = argv[1:]
    for f in stats_file:

        job_name = path.basename(f).split(".")[0].replace("summary-","")
        file_age = file_age_in_min(f)
        data = restic_get_summary(f)
        if data != {}:
            print(f"""
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

# HELP restic_stats_last_snapshot_age Age of latest snapshot in minutes

            print(f"""
restic_stats_last_snapshot_age{{backup_job="{job_name}"}} {file_age}
""")