import logging
from output_utils import (template_loader, SuperFormatter)

def output_html(summary, events):
    """ Generate a string containing the html output corresponding to the input

    Arguments:
    infos --- array of dictionnaries with backup infos
    """
    sf = SuperFormatter()

    return sf.format(template_loader('backup_history.tpl'),
       title_name = 'pgbackrest reader'
        , info_backrest_version = summary["last_pgbackrest_version"]
        , info_database_version = summary["last_db_version"]
        , info_database_system_id = summary["last_db_system_id"]
        , event_list = [event["backup_label"] + ": " + event["event_name"] for event in events]
        , data_backup_label = summary["backup_label"]
        , data_duration = summary["duration"]
        , data_backup_size = summary["backup_size"]
        , data_partial_backup_size = summary["partial_backup_size"]
        , data_original_size  = summary["original_size"]
        , data_partial_original_size = summary["partial_original_size"]
        , data_backup_items = summary["backup_items"]
        , data_time_since_last_backup = summary["time_since_last_backup"]
        , data_compression = summary["compression"]
        , data_archive_during_backup = summary["archives_during_backup"]
        , data_archive_between_backup = summary["archives_between_backup"]
    )


