import gzip
import ConfigParser
import json
from datetime import timedelta, date, time, datetime
from os import path
import os
import logging

def parse_file(input_file, start_date = datetime(1970,1,1), end_date = datetime(9999,12,31,23,59,59), backup_stamps = None):
    """ Scans a manifest file (.gz or not) and get the stats of the backups.

    Arguments:
    input_file --- File to scan
    start_date --- Lower bound to filter the start date
    end_date --- Upper bound to filter the start date
    backup_stamps --- dictionary of labels with their end timestamp
    """
    logging.debug("Beginning parse_file {}".format(input_file))
    config = ConfigParser.ConfigParser()
  
    # C est moche mais dans notre cas c est suffirant
    logging.debug("Openning file")
    if input_file.endswith(".manifest.gz"):  
        try:
            f = gzip.open(input_file, 'rb')
            config.readfp(f)
        except IOError as e:
            logging.error("Failed to acess file", exc_info=True)
            exit(1)
        except:
            raise
    elif input_file.endswith(".manifest"):
        try:
            f = open(input_file, 'r')
            config.readfp(f)
        except IOError as e:
            logging.error("Failed to acess file", exc_info=True)
            exit(1)
        except:
            raise
    else:
        logging.error("Invalid File", exc_info=True)
        exit(1)
        
    # Load Backup infos 
    info = {}
    info["file"] = input_file
    info["backup_size"] = 0
    info["partial_backup_size"] = 0
    info["original_size"] = 0
    info["partial_original_size"] = 0
    info["backup_items"] = 0
    try:
        logging.debug("Fetching backrest info")
        info["backrest_version"] = config.get("backrest","backrest-version")
        
        logging.debug("Fetching backup info")
        info["backup_archive_start"] = config.get("backup","backup-archive-start")
        info["backup_archive_stop"] = config.get("backup","backup-archive-stop")
        info["backup_lsn_start"] = config.get("backup","backup-lsn-start")
        info["backup_lsn_start"] = config.get("backup","backup-lsn-start")
        info["backup_label"] = config.get("backup", "backup-label")
        info["backup_type"] = config.get("backup", "backup-type")
        if info["backup_type"] != "\"full\"":
            try:
                info["backup_prior"] = config.get("backup", "backup-prior")
            except:
                raise
        else:
            info["backup_prior"] = None

        drift = 2
        info["backup_timestamp_start"] = config.get("backup", "backup-timestamp-start")
        info["backup_timestamp_start_ts"] = datetime(1970,1,1) + timedelta(hours=drift, seconds=int(info["backup_timestamp_start"]))
        info["backup_timestamp_stop"] = config.get("backup", "backup-timestamp-stop")
        info["backup_timestamp_stop_ts"] = datetime(1970,1,1) + timedelta(hours=drift, seconds=int(info["backup_timestamp_stop"]))
 
        logging.debug("Fetching db info")
        info["db_system_id"] = config.get("backup:db","db-system-id")
        info["db_version"] = config.get("backup:db","db-version")
    except KeyError:
        logging.error("Wrong key in manifest file", exc_info=True)
        exit(1)
    except ConfigParser.NoSectionError:
        logging.error("Wrong section in manifest file", exc_info=True)
        exit(1)

    logging.debug("Check dates {} [{}; {}]".format(info["backup_timestamp_start_ts"],start_date ,end_date))
    if info["backup_timestamp_start_ts"] <= start_date:
       return None

    if info["backup_timestamp_start_ts"] >= end_date:
       return None

    logging.debug("Item processing")
    for item in config.items("target:file"):
        parsed_item = json.loads(item[1])
        
        tmp_ts = datetime(1970,1,1) + timedelta(hours=drift, seconds=int(parsed_item["timestamp"]))

        info["backup_items"] += 1
        try:
            info["backup_size"] += parsed_item["repo-size"]
        except KeyError:
            pass

        if backup_stamps and info["backup_prior"] and backup_stamps[info["backup_prior"]] <= tmp_ts:
            info["partial_backup_size"] += parsed_item["repo-size"]

        try:
            info["original_size"] += parsed_item["size"]
        except KeyError:
            pass

        if backup_stamps and info["backup_prior"] and backup_stamps[info["backup_prior"]] <= tmp_ts:
            info["partial_original_size"] += parsed_item["size"]
    
    if info["backup_type"] == "\"full\"":
        info["partial_backup_size"] = info["backup_size"]
        info["partial_original_size"] = info["original_size"]

    try:
        info["compression"] = 100 * (int(info["partial_original_size"]) - int(info["partial_backup_size"])) /  int(info["partial_original_size"])
    except ZeroDivisionError:
        # case where we scan a incremental backup manifest alone
        info["compression"] = 0
 
    logging.debug("End parse_file")
    return info


def parse_directory(input_dir, start_date = datetime(1970,1,1), end_date = datetime(9999,12,31,23,59,59)):
    """ Scans a manifest file (.gz or not) and get the stats of the backups.

    Arguments:
    input_dir --- Dir to scan
    start_date --- Lower bound to filter the start date
    end_date --- Upper bound to filter the start date
    """
    logging.debug("Beginning parse_directory {}".format(input_dir))

    def parse_gzipped_directory(input_dir,  start_date, end_date, infos, backup_stamps):
        """ Scans a gzipped directory. This one in different situation """
        try:
            file_names = sorted(os.listdir(input_dir))     
            for file_name in file_names:
                 if file_name.endswith(".manifest.gz") or file_name.endswith(".manifest"):
                     tmp = parse_file(input_dir + "/" + file_name, start_date, end_date, backup_stamps)
                     backup_stamps[tmp["backup_label"]] = tmp["backup_timestamp_stop_ts"]
                     if tmp:
                             infos.append(tmp)
        except OSError as e:
            logging.error("Failed to open directory", exc_info=True)
            exit(1)
        except:
            raise
     
    if not path.isdir(input_dir):
        logging.error("The specified path is not a directory")
        exit(1)

    infos = []
    backup_stamps = {}
    if path.exists(input_dir + "/backup.info"):

        dir_names = sorted(os.listdir(input_dir + "/backup.history"))
        for dir_name in dir_names:
            parse_gzipped_directory(input_dir + "/backup.history/" + dir_name, start_date, end_date, infos, backup_stamps)

    else:
        parse_gzipped_directory(input_dir, start_date, end_date, infos, backup_stamps)
    
    logging.debug("End parse_directory")
    return infos
