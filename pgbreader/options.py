import optparse
from datetime import timedelta, datetime


def get_options(version='0.0.0'):
    """ parse the use input and create the inoptions dictionnary """

    p = optparse.OptionParser(usage = "usage: %prog [options] FILENAME", version = "%prog version " + version)

    g = optparse.OptionGroup(p, "General options")
    g.add_option("--input-file", "-I", action = "store", dest = "input_file", default = None, help = "Input")
    g.add_option("--input-dir", "-D", action = "store", dest = "input_dir", default = None, help = "Input directory, filters for .gz files")
    g.add_option("--output-type", "-T", action = "store", dest = "output_type", default = "details", choices = ["details","csv","html"], help = "Output format:  details, csv, html (experimental)")
    g.add_option("--log-level", action = "store", dest = "log_level", default = "INFO", choices = ["INFO","DEBUG","ERROR"], help = "Output format:  INFO, DEBUG, ERROR")
    p.add_option_group(g)

    g = optparse.OptionGroup(p, "Filtering options")
    g.add_option("--start-date", "-s", action = "store", dest = "start_date", default = None, help = "Filter starting from the specified start-date")
    g.add_option("--end-date", "-e", action = "store", dest = "end_date", default = None, help = "Filter until the specified end-date")
    p.add_option_group(g)

#    g = optparse.OptionGroup(p, "SSH Options"
#    g.add_option("--ssh-host", action = "store", dest = "ssh_host", default = None, help = "Filter starting from the specified start-date")
#    g.add_option("--ssh-user", action = "store", dest = "ssh_username", default = None, help = "Filter until the specified end-date")
#    g.add_option("--ssh-password", action = "store", dest = "ssh_password", default = None, help = "Filter until the specified end-date")
#    g.add_option("--ssh-timeout", action = "store", dest = "ssh_timeout", default = None, help = "Filter until the specified end-date")
#    p.add_option_group(g)

    inoptions, inarguments = p.parse_args()

    if inoptions.input_file == None and inoptions.input_dir == None:
        print "Either input_file or inoptions.input_dir is requiered"
        exit(1)

    if inoptions.start_date: 
        inoptions.start_date = datetime.strptime(inoptions.start_date, "%Y-%m-%d")
    else:
        inoptions.start_date = datetime(1970,1,1)
   
    if inoptions.end_date:
        inoptions.end_date = datetime.strptime(inoptions.end_date, "%Y-%m-%d")
        inoptions.end_date = inoptions.end_date + timedelta(hours=23, minutes=59, seconds=59)
    else:
        inoptions.end_date = datetime(9999,12,31,23,59)

#    if inoptions.log_level == "INFO":
#        logging.getLogger().setLevel(logging.INFO)
#    elif inoptions.log_level == "DEBUG":
#        logging.getLogger().setLevel(logging.DEBUG)
#    elif inoptions.log_level == "ERROR":
#        logging.getLogger().setLevel(logging.ERROR)

    return inoptions, inarguments

