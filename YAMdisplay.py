from bokeh.io import output_file, show
import bokeh
from bokeh.plotting import figure
from bokeh.charts import TimeSeries, Scatter, show, output_file
from bokeh.layouts import column
import bokeh.palettes
import datetime

class YAMdisplay():
    def __init__(self):
        None

    def displayTemperature(self, series):
        X = []
        Y = []
        
        p = bokeh.plotting.figure(plot_width=650,
                                  plot_height=450, x_axis_type="datetime",
                                  x_axis_label="Date / Time",
                                  y_axis_label="Temperature dgC", y_range = (15.0,33.0))
    
        colors = bokeh.palettes.d3["Category20c"][20]
        color = colors.pop(0)
        
        for name in series:
            print(name)
            for time, temp in sorted(series[name].items()):
                X.append(datetime.datetime.fromtimestamp(time))
                Y.append(float(temp))
            p.line(x=X, y=Y, color=color, legend=name)
        
        ##tsline = TimeSeries(data,
        ##    x='Date', y=['Temp.Hatchy'],
        ##    color=['Temp.Hatchy'],
        ##    title="Timeseries", ylabel='Temperatures', legend=True)
        
        
        ##plot = figure(plot_width=400, tools='pan,box_zoom')
        ##plot.circle([1,2,3,4,5], [8,6,5,2,3])
        output_file('temperature.html')
        show(p)

