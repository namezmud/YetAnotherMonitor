from bokeh.io import output_file, show
import bokeh
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool

from bokeh.layouts import column
import bokeh.palettes
import datetime
import time

# Create the figure with Bokeh.
# call showTemeprature to display or getTemperature to embed in html.
#
class YAMdisplay():
    def __init__(self):
        None

    # Build and populate temperature figure.
    def buildTemperature(self, series):
        p = bokeh.plotting.figure(plot_width=700,
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
        # Choose a 12 color palette.
        colors = bokeh.palettes.brewer['Paired'][12]
        
        max_lines = 20
        lines = 0

        min_time = datetime.datetime.max
        max_time = datetime.datetime.min
        
        for name in series:
            lines = lines +1
            if lines > max_lines:
                break

            # if we run out of colors, the rest are black.
            color = "black"
            if len(colors):
                color = colors.pop(0)
                
            data = {}
            data["time"] = []
            data["temp"] = []
            data["name"] = []
            data["time_str"] = []
            
            for time, temp_str in sorted(series[name].items()):

                # Catch exception if error in 1 record.  Do all conversions first to
                # avoid appending half a record
                try:
                    # TODO, make more pythonic.
                    if temp_str is not None:
                        time = datetime.datetime.fromtimestamp(time)
                        time_str = time.strftime("%H:%M")
                        temp = float(temp_str)

                        # If there is a gap in the data, insert a NaN to create a gap in the plot
                        if len(data["time"]) > 0 and (time - data["time"][-1] > datetime.timedelta(hours=1)):
                            data["time"].append(data["time"][-1] + datetime.timedelta(seconds = 10))
                            data["time_str"].append("")
                            data["name"].append(name)
                            data["temp"].append(float("nan"))                          
                            
                        data["time"].append(time)
                        data["time_str"].append(time_str)
                        data["name"].append(name)
                        data["temp"].append(temp)
                        
                except (TypeError, ValueError) as err:
                    print("Error ", err, " @ ", time)               
                    
            max_time = max(max_time, data["time"][-1])
            min_time = min(min_time, data["time"][0])
            p.line(source=data, x="time", y="temp", color=color, line_width=2, legend=name)

        # Make shaded boxes for nights
        night_boxes = []
        d = min_time - datetime.timedelta(days=1)
        while d < max_time:
            start = datetime.datetime.combine(d.date(), datetime.time(hour=19))
            end = datetime.datetime.combine(d.date() + datetime.timedelta(days=1), datetime.time(hour=7))
            print (start, end)
            night_boxes.append(
               bokeh.models.BoxAnnotation(plot=p, left=start.timestamp()*1000, right=end.timestamp()*1000, 
                                          fill_alpha=0.3, fill_color='gray'))
            d = d + datetime.timedelta(days=1)
        p.renderers.extend(night_boxes)

        p.legend.location = "top_left"
        p.legend.click_policy="hide"
        # set tooltip format
        hover = HoverTool(tooltips=[("Name", "@name"), ("Time", "@time_str"), ("Temp", "@temp")], attachment="vertical")
        p.add_tools(hover)
        
        return p

    # Build and show the figure.
    def showTemperature(self, series):

        p = self.buildTemperature(series)

    
        a = datetime.datetime.now()
        output_file('temperature.html')
        b = datetime.datetime.now()
        show(p)
        c = datetime.datetime.now()

        # log timing info.
        print("Time - output file", b-a)
        print("Time - show()", c-b)

    # return the components of the figure to embed in a page.
    def getTemperature(self, series):
        plot = self.buildTemperature(series)
        script, div = components(plot)
    
        return [script, div]
