from bokeh.io import output_file, show
import bokeh
from bokeh.plotting import figure
from bokeh.charts import TimeSeries, Scatter, show, output_file
from bokeh.embed import components
from bokeh.models import HoverTool

from bokeh.layouts import column
import bokeh.palettes
import datetime
import time

class YAMdisplay():
    def __init__(self):
        None

    def buildTemperature(self, series):
        p = bokeh.plotting.figure(plot_width=1000,
                                  plot_height=500, x_axis_type="datetime",
                                  x_axis_label="Date / Time",
                                  y_axis_label="Temperature dgC", y_range = (15.0,33.0),
                                  webgl=True,
                                  background_fill_color = "gray",
                                  background_fill_alpha = 0.05,
                                  outline_line_width = 2,
                                  outline_line_alpha = 0.8,
                                  outline_line_color = "black"
                                  )
        
        #colors = bokeh.palettes.d3["Category20b"][12]
        colors = bokeh.palettes.brewer['Paired'][12]
        
        max_lines = 100
        lines = 0
        
        for name in series:
            lines = lines +1
            if lines > max_lines:
                break

            color = colors.pop(0)
            data = {}
            data["time"] = []
            data["temp"] = []
            data["name"] = []
            data["time_str"] = []
            
            for time, temp in sorted(series[name].items()):

                if temp is not None:
                    time = datetime.datetime.fromtimestamp(time)
                    data["time"].append(time)
                    data["time_str"].append(time.strftime("%H:%M"))
                    data["name"].append(name)
                    data["temp"].append(float(temp))
            
            p.line(source=data, x="time", y="temp", color=color, line_width=2, legend=name)


        p.legend.location = "top_left"
        p.legend.click_policy="hide"
        hover = HoverTool(tooltips=[("Name", "@name"), ("Time", "@time_str"), ("Temp", "@temp")], attachment="vertical")
        p.add_tools(hover)
        
        return p

    def showTemperature(self, series):

        p = self.buildTemperature(series)

    
        a = datetime.datetime.now()
        output_file('temperature.html')
        b = datetime.datetime.now()
        show(p)
        c = datetime.datetime.now()

        print(b-a)
        print(c-b)

    def getTemperature(self, series):
        plot = self.buildTemperature(series)
        script, div = components(plot)
    
        return [script, div]
