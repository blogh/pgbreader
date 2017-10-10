<html>
<head>
<title>{title_name}</title>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
<script src="http://code.highcharts.com/highcharts.js"></script>
</head>
<body>
<script id="data">
var backup_label = {{
    'name' : 'Backup label',
    'data' : [{data_backup_label}]
}};
var duree = {{
    'name' : 'duree',
    'data' : [{data_duration}]
}};
var backup_size = {{
    'name' : 'backup size',
    'data' : [{data_backup_size}]
}};
var partial_backup_size = {{
    'name' : 'partial backup size',
    'data' : [{data_partial_backup_size}]
}};
var original_size = {{
    'name' : 'original size',
    'data' : [{data_original_size}]
}};
var partial_original_size = {{
    'name' : 'partial original size',
    'data' : [{data_partial_original_size}]
}};
var backup_items = {{
    'name' : 'items in backup',
    'data' : [{data_backup_items}]
}};
var time_since_last_backup = {{
    'name' : 'time since last backup',
    'data' : [{data_time_since_last_backup}]
}};
var compression = {{
    'name' : 'average compression ratio',
    'data' : [{data_compression}]
}};
var archive_during_backup = {{
    'name' : 'number of archives during backup',
    'data' : [{data_archive_during_backup}]
}};
var archive_between_backup = {{
    'name' : 'number of archives between backup',
    'data' : [{data_archive_between_backup}]
}};
</script>
<script>
function secondsTimeSpanToDHMS(s) {{
    var d = Math.floor(s / 86400); //Get whole days
    s -= d * 86400
    var h = Math.floor(s / 3600); //Get whole hours
    s -= h * 3600;
    var m = Math.floor(s / 60); //Get remaining minutes
    s -= m * 60;
    return d + " days " + h + ":" + (m < 10 ? '0' + m : m) + ":" + (s < 10 ? '0' + s : s); //zero padding on minutes and seconds
}}
function bytes(bytes, label) {{
    if (bytes == 0) return '';
    var s = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB'];
    var e = Math.floor(Math.log(bytes)/Math.log(1024));
    var value = ((bytes/Math.pow(1024, Math.floor(e))).toFixed(2));
    e = (e<0) ? (-e) : e;
    if (label) value += ' ' + s[e];
    return value;
}}

$(function() {{
    var mchart_cbv = Highcharts.chart('container_backup_volumes', {{
        chart: {{
            zoomType: 'x'
        }},
        title: {{
            text: 'Volume of backed-up data and original data'
        }},
        subtitle: {{
            text: 'Source: pgbackrest manifests'
        }},
        xAxis: {{
            categories: backup_label['data'],
            crosshair: true
        }},
       yAxis: {{
            title: {{
                text: 'Volume (bytes)'
            }}
        }},
        legend: {{
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        }},
        series: [{{
            name: backup_size['name'],
            data: backup_size['data']
        }}, {{
            name: partial_backup_size['name'],
            data: partial_backup_size['data']
        }}, {{
            name: original_size['name'],
            data: original_size['data']
        }}, {{
            name: partial_original_size['name'],
            data: partial_original_size['data']
        }}],
        tooltip: {{
            formatter: function() {{
                return bytes(this.y, true);
            }}
        }}
    }});
    var mchart_cbd = Highcharts.chart('container_backup_duration', {{
        chart: {{
            zoomType: 'x'
        }},
        title: {{
            text: 'Length of backups'
        }},
        subtitle: {{
            text: 'Source: pgbackrest manifests'
        }},
        xAxis: {{
            categories: backup_label['data'],
            crosshair: true
        }},
        yAxis: {{
            title: {{
                text: 'Duration'
            }},
            labels: {{
                formatter: function() {{
                    return  secondsTimeSpanToDHMS(this.value);
                }}               
            }}
        }},
        legend: {{
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        }},
        series: [{{
            name: duree['name'],
            data: duree['data']
        }}],
        tooltip: {{
            formatter: function() {{
                return  '<b>' + this.series.name +'</b><br/>' + secondsTimeSpanToDHMS(this.y);
            }}
        }}
    }});
    var mchart_cbn = Highcharts.chart('container_backup_nitems', {{
        chart: {{
            zoomType: 'x'
        }},
        title: {{
            text: 'Scanned items per backup'
        }},
        subtitle: {{
            text: 'Source: pgbackrest manifests'
        }},
        xAxis: {{
            categories: backup_label['data'],
            crosshair: true
        }},
        yAxis: {{
            title: {{
                text: 'Units'
            }}
        }},
        legend: {{
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        }},
        series: [{{
            name: backup_items['name'],
            data: backup_items['data']
        }}]
    }});
    var mchart_cbt = Highcharts.chart('container_backup_time_since_last', {{
        chart: {{
            zoomType: 'x'
        }},
        title: {{
            text: 'Time since last backup'
        }},
        subtitle: {{
            text: 'Source: pgbackrest manifests'
        }},
        xAxis: {{
            categories: backup_label['data'],
            crosshair: true
        }},
        yAxis: {{
            title: {{
                text: 'Time'
            }},
            labels: {{
                formatter: function() {{
                    return  secondsTimeSpanToDHMS(this.value);
                }}               
            }}
        }},
        legend: {{
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        }},
        series: [{{
            name: time_since_last_backup['name'],
            data: time_since_last_backup['data']
        }}],
        tooltip: {{
            formatter: function() {{
                return  '<b>' + this.series.name +'</b><br/>' + secondsTimeSpanToDHMS(this.y);
            }}
        }}
    }});
    var mchart_cc = Highcharts.chart('container_compression', {{
        chart: {{
            zoomType: 'x'
        }},
        title: {{
            text: 'Compression ratio'
        }},
        subtitle: {{
            text: 'Source: pgbackrest manifests'
        }},
        xAxis: {{
            categories: backup_label['data'],
            crosshair: true
        }},
        yAxis: {{
            title: {{
                text: '%'
            }},
            labels: {{
                formatter: function() {{
                    return  this.value + '%';
                }}               
            }}               
        }},
        legend: {{
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        }},
        series: [{{
            name: compression['name'],
            data: compression['data']
        }}],
        tooltip: {{
            formatter: function() {{
                return  '<b>' + this.series.name +'</b><br/>' + this.y + '%';
            }}
        }}
    }});
    var mchart_cc = Highcharts.chart('container_archives', {{
        chart: {{
            zoomType: 'x'
        }},
        title: {{
            text: 'Archive counts'
        }},
        subtitle: {{
            text: 'Source: pgbackrest manifests'
        }},
        xAxis: {{
            categories: backup_label['data'],
            crosshair: true
        }},
        yAxis: {{
            title: {{
                text: 'Units'
            }}
        }},
        legend: {{
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        }},
        series: [{{
            name: archive_between_backup['name'],
            data: archive_between_backup['data']
        }}, {{
            name: archive_during_backup['name'],
            data: archive_during_backup['data']
        }}],
        tooltip: {{
            formatter: function() {{
                return  '<b>' + this.series.name +'</b><br/>' + this.y;
            }}
        }}
    }});
}});
</script>
<p>pgbackrest version : {info_backrest_version}</p>
<p>database version : {info_database_version}</p>
<p>database system-id : {info_database_system_id}</p>
<p>
    <p>eventlist:</p>
    <ul>
    {event_list:repeat:<li>{{item}}</li>}
    </ul>
</p>
<div id="container_backup_volumes" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
<div id="container_backup_duration" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
<div id="container_backup_nitems" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
<div id="container_backup_time_since_last" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
<div id="container_compression" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
<div id="container_archives" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
</body>
</html>
