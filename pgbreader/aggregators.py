import logging

def wal_diff(wal_start, wal_stop):
    """ count wals files between two wals """
    event = []

    wal_start_tl = int(wal_start[0:8],16)
    wal_start_blocid = int(wal_start[8:16],16)
    wal_start_segid = int(wal_start[16:24],16)
    wal_start_num = wal_start_tl * int('FF',16) * int('FF',16) + wal_start_blocid * int('FF',16) + wal_start_segid

    wal_stop_tl = int(wal_stop[0:8],16)
    wal_stop_blocid = int(wal_stop[8:16],16)
    wal_stop_segid = int(wal_stop[16:24],16)
    wal_stop_num = wal_start_tl * int('FF',16) * int('FF',16) + wal_stop_blocid * int('FF',16) + wal_stop_segid

    logging.debug("start {} ({} {} {}) {}".format(wal_start, wal_start_tl, wal_start_blocid, wal_start_segid, wal_start_num))
    logging.debug("stop  {} ({} {} {}) {}".format(wal_stop, wal_stop_tl, wal_stop_blocid, wal_stop_segid, wal_stop_num))

    if wal_start_tl != wal_stop_tl:
       diff = 0
    else:
       diff = wal_stop_num - wal_start_num

    return diff, wal_start_tl, wal_stop_tl
    
        

def aggregate_backup_info(infos):
    """ aggregate all backup info and generate a summary and list of events

    Arguments:
    infos --- array of dictionnaries with backup infos
    """
    logging.debug("Begin aggregate_backup_info")
    events = []
    summary = {}
    last = {}
    DURATION_THRESHOLD_MULT = .2
    ORIGINAL_SIZE_THRESHOLD_MULT = .1
    BACKUP_SIZE_THRESHOLD_MULT = .1

    logging.debug("Infos processing")
    start = True
    sep = ', '
    for info in infos:
        duration = (info["backup_timestamp_stop_ts"] - info["backup_timestamp_start_ts"]).total_seconds()
        if start:
            start = False
            timeSinceLastBackup = 0

            summary["first_backup"] = info["backup_timestamp_start_ts"]
            summary["last_backup"] = info["backup_timestamp_stop_ts"]
            summary["backup_count"] = 1
            summary["duration"] = str(duration)
            summary["backup_label"] = info["backup_label"]
            summary["backup_type"] = info["backup_type"]
            summary["backup_size"] = str(info["backup_size"])
            summary["partial_backup_size"] = str(info["partial_backup_size"])
            summary["original_size"] = str(info["original_size"])
            summary["partial_original_size"] = str(info["partial_original_size"])
            summary["backup_items"] = str(info["backup_items"])
            summary["time_since_last_backup"] = str(timeSinceLastBackup)
            summary["compression"] = str(info["compression"])
            diff, tl1, tl2 = wal_diff(info["backup_archive_start"][1:], info["backup_archive_stop"][1:]) 
            summary["archives_during_backup"] = str(diff)
            summary["archives_between_backup"] = str(0)

            last["backrest_version"] = info["backrest_version"]
            last["db_system_id"] = info["db_system_id"]
            last["db_version"] = info["db_version"]
            last["duration"] = duration
            last["original_size"] = info["original_size"]
            last["backup_size"] = info["backup_size"]
            last["backup_type"] = info["backup_type"] 
            last["backup_timestamp_start_ts"] = info["backup_timestamp_start_ts"]
            last["backup_archive_stop"] = info["backup_archive_stop"]
        else:
            timeSinceLastBackup = (info["backup_timestamp_start_ts"] - last["backup_timestamp_start_ts"]).total_seconds()

            summary["backup_label"] = summary["backup_label"] + sep +  info["backup_label"]
            summary["duration"] = summary["duration"] + sep + str(duration)
            summary["backup_type"] = summary["backup_type"] + sep + info["backup_type"]
            summary["backup_size"] = summary["backup_size"] + sep + str(info["backup_size"])
            summary["partial_backup_size"] = summary["partial_backup_size"] + sep + str(info["partial_backup_size"])
            summary["original_size"] = summary["original_size"] + sep + str(info["original_size"])
            summary["partial_original_size"] = summary["partial_original_size"] + sep + str(info["partial_original_size"])
            summary["backup_items"] = summary["backup_items"] + sep + str(info["backup_items"])
            summary["time_since_last_backup"] = summary["time_since_last_backup"] + sep + str(timeSinceLastBackup)
            summary["compression"] = summary["compression"] + sep + str(info["compression"])
            summary["last_backup"] = info["backup_timestamp_stop_ts"]
            summary["backup_count"] += 1
            diff, tl1, tl2 = wal_diff(info["backup_archive_start"][1:], info["backup_archive_stop"][1:])
            summary["archives_during_backup"] = summary["archives_during_backup"] + sep + str(diff)
            diff, tl1, tl2 = wal_diff(last["backup_archive_stop"][1:], info["backup_archive_start"][1:])
            summary["archives_between_backup"] = summary["archives_between_backup"] + sep + str(diff)

            if not last["backrest_version"] == info["backrest_version"]:
                events.append({ "backup_label": info["backup_label"], "event_name": "pgbackrest version change: {} => {}".format(last["backrest_version"], info["backrest_version"])})
                last["backrest_version"] = info["backrest_version"]

            if not last["db_system_id"] == info["db_system_id"]:
                events.append({ "backup_label": info["backup_label"], "event_name": "database system id changed: {} => {}".format(last["db_system_id"], info["db_system_id"])})
                last["db_system_id"] == info["db_system_id"]

            if not last["db_version"] == info["db_version"]:
                events.append({ "backup_label": info["backup_label"], "event_name": "database version changed: {} => {}".format(last["db_version"], info["db_version"])})
                last["db_version"] = info["db_version"]

            if ((last["duration"] + last["duration"] * DURATION_THRESHOLD_MULT) < duration and 
                last["backup_type"] == info["backup_type"]):
                events.append({ "backup_label": info["backup_label"], "event_name": "duration growth > {}%: {} => {}".format(DURATION_THRESHOLD_MULT * 100, last["duration"], duration)})

            if ((last["original_size"] + last["original_size"] * ORIGINAL_SIZE_THRESHOLD_MULT) < last["original_size"] and
                last["backup_type"] == info["backup_type"]):
                events.append({ "backup_label": info["backup_label"], "event_name": "backup size growth > {}%: {} => {}".format(ORIGINAL_SIZE_THRESHOLD_MULT * 100, last["original_size"], last["original_size"])})

            if ((last["backup_size"] + last["backup_size"] * BACKUP_SIZE_THRESHOLD_MULT) < info["backup_size"] and
                last["backup_type"] == info["backup_type"]):
                events.append({ "backup_label": info["backup_label"], "event_name": "database size growth > {}%: {} => {}".format(BACKUP_SIZE_THRESHOLD_MULT * 100, last["backup_size"], info["backup_size"])})

            if ((last["duration"] - last["duration"] * DURATION_THRESHOLD_MULT) > duration and
                last["backup_type"] == info["backup_type"]):
                events.append({ "backup_label": info["backup_label"], "event_name": "duration decrease > {}%: {} => {}".format(DURATION_THRESHOLD_MULT * 100, last["duration"], duration)})

            if ((last["original_size"] - last["original_size"] * ORIGINAL_SIZE_THRESHOLD_MULT) > last["original_size"] and
                last["backup_type"] == info["backup_type"]):
                events.append({ "backup_label": info["backup_label"], "event_name": "backup size decrease > {}%: {} => {}".format(ORIGINAL_SIZE_THRESHOLD_MULT * 100, last["original_size"], last["original_size"])})

            if ((last["backup_size"] - last["backup_size"] * BACKUP_SIZE_THRESHOLD_MULT) > info["backup_size"] and
                last["backup_type"] == info["backup_type"]):
                events.append({ "backup_label": info["backup_label"], "event_name": "database size decrease > {}%: {} => {}".format(BACKUP_SIZE_THRESHOLD_MULT * 100, last["backup_size"], info["backup_size"])})

            last["duration"] = duration
            last["original_size"] = info["original_size"]
            last["backup_size"] = info["backup_size"]
            last["backup_type"] = info["backup_type"]
            last["backup_timestamp_start_ts"] = info["backup_timestamp_start_ts"]
            last["backup_archive_stop"] = info["backup_archive_stop"]

    summary["last_pgbackrest_version"] = last["backrest_version"]
    summary["last_db_system_id"] = info["db_system_id"]
    summary["last_db_version"] = info["db_version"]

    logging.debug("End aggregate_backup_info")
    return summary, events
