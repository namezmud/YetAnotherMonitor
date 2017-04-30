from boto import dynamodb2
from boto.dynamodb2.table import Table
import boto
import json
from bokeh.io import output_file, show
import bokeh
from bokeh.plotting import figure
from bokeh.charts import TimeSeries, Scatter, show, output_file
from bokeh.layouts import column
import bokeh.palettes

import datetime

table_name = "YAM_YRR"


##### aws_keys.json 
{
	"Region":"ap-southeast-2",
	"AccessKey":"_your key_",
        "SecretKey":"_your key_"
}

aws = json.loads(open("aws_keys.json").read())

conn = dynamodb2.connect_to_region(aws["Region"], aws_access_key_id=aws["AccessKey"], aws_secret_access_key=aws["SecretKey"])

table = Table(table_name, connection=conn)

#data = table.query_2(name__eq="Temp.Hatchy")
#data = table.query_2()

series = {}
# not assuming the db entries are in time order.
for entry in data:
    if entry["name"] not in series.keys():
        series[entry["name"]] = {}
    series[entry["name"]][float(entry["time_ms"])] = entry["temperature"]



X = []
Y = []

colors = bokeh.palettes.d3["Category20c"][20]
color = colors.pop(0)
name = "Temp.Hatchy"
for time, temp in sorted(series[name].items()):
    X.append(datetime.datetime.fromtimestamp(time/1000.0))
    Y.append(float(temp))
p.line(x=X, y=Y, color=color, legend=name)
    
p = bokeh.plotting.figure(plot_width=650, 
                          plot_height=450, x_axis_type="datetime",
                          x_axis_label="Date / Time",
                          y_axis_label="Temperature dgC", y_range = (15.0,33.0))

colors = bokeh.palettes.d3["Category20c"][20]

p.line(x=["Date", "Date"],  y=['Temp.Hatchy', 'Other'], source=data)
#p.line(x="Date",  y='Other', source=data)

##tsline = TimeSeries(data,
##    x='Date', y=['Temp.Hatchy'],
##    color=['Temp.Hatchy'],
##    title="Timeseries", ylabel='Temperatures', legend=True)


##plot = figure(plot_width=400, tools='pan,box_zoom')
##plot.circle([1,2,3,4,5], [8,6,5,2,3])
output_file('circle.html')
show(p)
