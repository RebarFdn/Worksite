# Standard library
import calendar
# Third party
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import base64
from io import BytesIO

import plotly.tools as tls
from tablerpy import (OutlineIcon, FilledIcon, get_icon)
import tablerpy as tab
from pydantic import BaseModel, Field

COLOR = "#FC5200"
OFFSET = 0.5

class PlotBaseMonth(BaseModel):
    COLOR:str = Field(default="#FC5200")
    OFFSET:float = Field(default=0.5)
    icons:dict = {
            "bike": get_icon(OutlineIcon.BIKE),
            "run": get_icon(OutlineIcon.RUN),
            "swim": get_icon(OutlineIcon.SWIMMING),
            "weight": get_icon(OutlineIcon.BARBELL)
        }

    # Prepare the Axis
    def prepare_axes(self, ax):
        ax.set(aspect=1, xlim=(0, 7), ylim=(0, 7))
        ax.axis("off")
        return ax
    
    # Text Placement
    def place_text(self, ax, x, y, text):
        ax.text(x + OFFSET, y + OFFSET, s=text,
                ha="center", va="center", color=COLOR)
        
    ## Highlighted Text    
    def place_highleted_text(self, ax, x, y, text, highlighted=False):  # default parameter
        ax.text(x + OFFSET, y + OFFSET, s=text,
                ha="center", va="center",
                # default is COLOR, otherwise use face color is hightlighted is True
                color=COLOR if not highlighted else ax.get_facecolor())
        

    def label_weekday(self, ax):
        top_row_position = 6
        for day_number, weekday in enumerate(calendar.day_abbr):
            self.place_text(ax=ax, x=day_number, y=top_row_position, text=weekday[0])


    def draw_circle(self, ax, x_pos, y_pos):
        ax.add_artist(
            mpatches.Circle(
                (x_pos + OFFSET, y_pos + OFFSET), radius=0.45,
                edgecolor=COLOR, facecolor="None"))
        
    def draw_highleted_circle(self, ax, x_pos, y_pos, highlight=False):  # default parameter
        ax.add_artist(
            mpatches.Circle(
                (x_pos + OFFSET, y_pos + OFFSET), radius=0.45,
                # default is no color, otherwise use COLOR
                edgecolor=COLOR, facecolor=COLOR if highlight else "None"))

    
    def place_icon(self, ax, activity, x_pos, y):
        icons = self.icons
        padding = .02
        newax = ax.inset_axes([x_pos / 7 + padding, y / 7 + padding, .1, .1])
        icon = icons.get(activity) or get_icon(OutlineIcon.BOLT)
        newax.imshow(icon)#newax.imshow(pytablericons.TablerIcons.load(icon))
        
        newax.axis('off')  


    def draw_calendar_of_a_month(self, ax, first, num_days):
        ax = self.prepare_axes(ax)
        self.label_weekday(ax)
        x_pos = first
        y = 5
        for day in range(1, num_days + 1):
            self.draw_circle(ax, x_pos, y)
            self.place_text(ax, x_pos, y, day)
            x_pos = (x_pos + 1) % 7
            if x_pos == 0:
                y -= 1

    
    def draw_calendar_of_a_month_highlights(self, ax, first, num_days, highlights):  # additional parameter
        ax = self.prepare_axes(ax)
        self.label_weekday(ax)
        x_pos = first
        y = 5
        for day in range(1, num_days + 1):
            # set a highlight boolean
            highlight: bool = day in highlights if highlights else False
            self.draw_highleted_circle(ax, x_pos, y, highlight)  # provide argument
            self.place_highleted_text(ax, x_pos, y, day, highlighted=highlight)  # provide argument
            x_pos = (x_pos + 1) % 7
            if x_pos == 0:
                y -= 1

    
    def draw_calendar_of_a_month_highlights_icons(self, ax, first, num_days, highlights=None, activities=None, show_icon=False):
        ax = self.prepare_axes(ax)
        self.label_weekday(ax)
        x_pos = first
        y = 5

        for day in range(1, num_days + 1):
            highlight = day in highlights if highlights else False
            self.draw_highleted_circle(ax, x_pos, y, highlight)
            # Either place an icon or text based on the hightlight value
            if show_icon and day in highlights:
                self.place_icon(ax, activities.pop(0) if activities else None, x_pos, y)
            else:
                self.place_highleted_text(ax, x_pos, y, day, highlighted=highlight)
            x_pos = (x_pos + 1) % 7
            if x_pos == 0:
                y -= 1


    # Plot June 2025 the month that spans six calendar weeks
    def plot_month(self, year:int=2025, range:int=6):
        fig = plt.figure()
        ax = fig.add_subplot()
        first_day, number_of_days = calendar.monthrange(year, range)
        self.draw_calendar_of_a_month(ax, first_day, number_of_days)
        plt.show()

    def plot_month_dates(self, year:int=2025, range:int=2, active_days:list=[5, 6, 7, 10, 27]):
        fig = plt.figure()
        ax = fig.add_subplot()
        first_day, number_of_days = calendar.monthrange(year, range)
        self.draw_calendar_of_a_month_highlights(ax, first_day, number_of_days, active_days )
        #plt.show()
        tmpfile = BytesIO()
        plt.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        html = f'<img src="data:image/png;base64,{encoded}" width="450px">'
        with open('plot.html', 'w') as f:
            f.write(html)
        return html
        

    def plot_month_icons(self, year:int=2025, range:int=6, active_days:list=[5, 6, 7, 10, 27]):
        fig = plt.figure()
        ax = fig.add_subplot()
        first_day, number_of_days = calendar.monthrange(year, range)
        self.draw_calendar_of_a_month_highlights_icons(ax, first_day, number_of_days, highlights=active_days, activities=list(self.icons.keys()), show_icon=True )
        plt.show()


am = PlotBaseMonth()
#.plot_month_icons()
html_file = am.plot_month_dates()

#print(html_file)

#am.plot_month_dates()