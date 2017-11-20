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
    var mchart_cbv = Highcharts.chart('container_backup_infos', {{
        chart: {{
            zoomType: 'x'
        }},
        title: {{
            text: 'Backup infos'
        }},
        subtitle: {{
            text: 'Source: pgbackrest manifests'
        }},
        xAxis: {{
            categories: backup_label['data'],
            crosshair: true
        }},
       yAxis: [{{
            id : 'Volume',
            labels: {{
                 formatter: function() {{
                     return bytes(this.value, true);
                 }}
            }},
            title: {{
                text: 'Volume'
            }}
        }},{{
            id : 'Duration',
            labels: {{
            formatter: function() {{
                 return  secondsTimeSpanToDHMS(this.value);
            }},
            style: {{
                 color: Highcharts.getOptions().colors[4]
            }}
         }},
            title: {{
                 text: 'Duration',
                 style: {{
                     color: Highcharts.getOptions().colors[4]
                 }}
             }},
             opposite: true
         }},{{
             id : 'Items',
             labels: {{
                style: {{
                    color: Highcharts.getOptions().colors[5]
                }}
             }},
             title: {{
                 text: 'Items',
                 style: {{
                    color: Highcharts.getOptions().colors[5]
                 }}
            }},
            opposite: true
         }},{{
            id : '% compression',
            labels: {{
                 style: {{
                     color: Highcharts.getOptions().colors[6]
                 }}
            }},
            title: {{
                text: '% compression',
                style: {{
                     color: Highcharts.getOptions().colors[6]
                }}
            }},
            opposite: true
         }}],
        legend: {{
            layout: 'horizontal',
            align: 'center',
            verticalAlign: 'bottom'	
        }},
         tooltip: {{
              formatter: function () {{
                  var s = '<b>' + this.x + '</b>';

                  $.each(this.points, function () {{
                       s += '<br/>' + this.series.name + ': '
                       switch (this.series.name){{
                           case duree['name']:
                               s += secondsTimeSpanToDHMS(this.y);
                               break;
                           case backup_items['name']:
                               s += this.y + ' items<br/>';
                               break;
                           case compression['name']:
                               s += this.y + '%<br/>';
                               break;
                           default:
                               s += bytes(this.y, true);
                        }}
                   }});

                   return s;
                }},
                shared: true
        }},
        series: [{{
            name: backup_size['name'],
            data: backup_size['data'],
            yAxis: 0
        }}, {{
            name: partial_backup_size['name'],
            data: partial_backup_size['data'],
            yAxis: 0,
            visible: false		
        }}, {{
            name: original_size['name'],
            data: original_size['data'],
            yAxis: 0
        }}, {{
            name: partial_original_size['name'],
            data: partial_original_size['data'],
            yAxis: 0,
            visible: false		
        }}, {{
            name: duree['name'],
            data: duree['data'],
            yAxis: 1
        }}, {{
            name: backup_items['name'],
            data: backup_items['data'],
            yAxis: 2,
            visible: false		
        }}, {{
           name: compression['name'],
           data: compression['data'],
           yAxis: 3,
           visible: false			
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
            layout: 'horizontal',
            align: 'center',
            verticalAlign: 'bottom'
        }},
        tooltip: {{
            formatter: function() {{
                return  '<b>' + this.x + '</b><br/>'+ this.series.name +': ' + secondsTimeSpanToDHMS(this.y);
            }}
        }},
        series: [{{
            name: time_since_last_backup['name'],
            data: time_since_last_backup['data']
        }}],
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
            layout: 'horizontal',
            align: 'center',
            verticalAlign: 'bottom'	
        }},
        tooltip: {{
              formatter: function () {{
                  var s = '<b>' + this.x + '</b>';

                  $.each(this.points, function () {{
                       s += '<br/>' + this.series.name + ': ' + this.y + ' (' + bytes(this.y*16,true) + ' without compression)';
                   }});

                   return s;
                }},
                shared: true
        }},
        series: [{{
            name: archive_between_backup['name'],
            data: archive_between_backup['data']
        }}, {{
            name: archive_during_backup['name'],
            data: archive_during_backup['data']
        }}]
    }});
}});
</script>
<h1>Pgbackrest info<h1>
<h2>Server info</h2>
<p>pgbackrest version : {info_backrest_version}</p>
<p>database version : {info_database_version}</p>
<p>database system-id : {info_database_system_id}</p>
<p>
    <p>eventlist:</p>
    <ul>
    {event_list:repeat:<li>{{item}}</li>}
    </ul>
</p>
<h2>Backup stats</h2>
<div id="container_backup_infos" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
<div id="container_backup_time_since_last" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
<h2>Wals stats</h2>
<div id="container_archives" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
</body>
</html>
