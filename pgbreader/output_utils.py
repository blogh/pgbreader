import logging
import pkg_resources
import string

def template_loader(file_name):
    """ Loads a file from the package to string 

    Arguments:
    file_name --- name of the template to load from the package
    """

    try:
        resource = pkg_resources.resource_string(__name__, file_name)
    except IOError as e:
        logging.error("Failed to acess file", exc_info=True)
        exit(1)
    except:
        raise

    return resource

class SuperFormatter(string.Formatter):
    """World's simplest Template engine.
    from https://github.com/ebrehault/superformatter
    """

    def format_field(self, value, spec):
        if spec.startswith('repeat'):
            template = spec.partition(':')[-1]
            if type(value) is dict:
                value = value.items()
            return ''.join([template.format(item=item) for item in value])
        elif spec == 'call':
            return value()
        elif spec.startswith('if'):
            return (value and spec.partition(':')[-1]) or ''
        else:
            return super(SuperFormatter, self).format_field(value, spec)


def output_details(infos):
    """ Display the backup info in the detail mode

    Arguments:
    infos --- array of dictionnaries with backup infos
    """
    logging.debug("Beginning output_details")

    for info  in infos:
        print ("backup label {}\n"
               "backup type : {}\n"
               "backup timestamp start: {}\n"
               "backup timestamp stop: {} \n"
               "full backup size: {} MB\n"
               "backup size: {} MB\n"
               "original size: {} MB\n"
               "backedup original size: {} MB\n"
               "Compression: {}\n"
               "backup items: {}\n"
               "wals: {} - {}\n").format(
            info["backup_label"]
            ,info["backup_type"]
            ,info["backup_timestamp_start_ts"]
            ,info["backup_timestamp_stop_ts"]
            ,int(info["backup_size"])/1024/1024
            ,int(info["partial_backup_size"])/1024/1024
            ,int(info["original_size"])/1024/1024
            ,int(info["partial_original_size"])/1024/1024
            ,info["compression"]
            ,info["backup_items"]
            ,info["backup_archive_start"]
            ,info["backup_archive_stop"])
    logging.debug("End output_details")


def output_csv(infos):
    """ Display the backup info in the csv mode
    Todo: use the csv API

    Arguments:
    infos --- array of dictionnaries with backup infos
    """
    logging.debug("Beginning output_csv")

    for info  in infos:
        print "{};{};{};{};{};{};{};{};{}".format(
            info["backup_label"]
            ,info["backup_type"]
            ,info["backup_timestamp_start_ts"]
            ,info["backup_timestamp_stop_ts"]
            ,info["backup_size"]
            ,info["partial_backup_size"]
            ,info["original_size"]
            ,info["partial_original_size"]
            ,info["backup_items"])
    logging.debug("End output_csv")

