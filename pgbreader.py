#!/usr/bin/python

from pgbreader.options import get_options
from pgbreader.parsers import (parse_file, parse_directory)
from pgbreader.aggregators import aggregate_backup_info
from pgbreader.output_utils import (template_loader, output_details, output_csv)
from pgbreader.output_html import output_html
import logging

VERSION='0.1.0'

# dump une date en json
def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

def main():
    """ main part of the program """
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO)
    logging.debug("Beginning")

    inoptions, inarguments = get_options(version=VERSION)
   
    #----------------------------------------------------------------------------------------------
    # Parsing files
    #----------------------------------------------------------------------------------------------
    infos = []
    if inoptions.input_file:
        tmp = parse_file(inoptions.input_file)
        if tmp:
            infos.append(tmp)

    elif inoptions.input_dir: 
        infos = parse_directory(inoptions.input_dir, inoptions.start_date, inoptions.end_date)

    #----------------------------------------------------------------------------------------------
    # Display
    #----------------------------------------------------------------------------------------------
    if inoptions.output_type == "details":
        output_details(infos)
    elif inoptions.output_type == "csv":
        output_csv(infos)
    elif inoptions.output_type == "html":
        summary, events = aggregate_backup_info(infos)
        print output_html(summary, events)

    logging.debug("End")
    exit(0)


if __name__ == '__main__':
    main()

