import datetime as dt
import calendar
import polars as pol
import plotly.express as px
from typing import Any
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from core.baseModels.accounting_models import DepositModel
from core.utilities.utils import convert_timestamp
from core.utilities.calendar_days import PlotBaseMonth
from config import CHARTS_PATH

#______________ Setup ______________

if CHARTS_PATH.exists():
    pass
else:
    CHARTS_PATH.mkdir(exist_ok=True)


def file_path(file_name:str):
    return CHARTS_PATH / file_name



class IncomeDataFrame(BaseModel):
    deposits:list[DepositModel] = []
    dates:list[str] = []
    amounts:list[float] = []
    chart_width:int= 600
    chart_height:int= 400     

    @property
    def update(self):
        for deposit in self.deposits:
            date_str:str = convert_timestamp(deposit.date) 
            self.dates.append(dt.date.fromisoformat(date_str)) # type: ignore
        #self.dates = [item.date for item in self.deposits ] # type: ignore
        self.amounts = [item.amount for item in self.deposits ]


    @property
    def data_frame(self):
        df = pol.DataFrame({
            "date": self.dates,
            "deposit": self.amounts            
        })       
        return df   

   
    
    def group_data_frame(self, period:str="1mo"):
        df = self.data_frame
        frame = df.group_by_dynamic("date", every=period, closed="right").agg(pol.col("deposit").sum())
        return frame
    
    @property
    def calendars(self):
        ''' '''
        dates = self.group_data_frame(period="1mo")["date"]
        cal = calendar.HTMLCalendar(firstweekday=0)
        #cal2 = calendar.TextCalendar(firstweekday=0)
        months:list= []
        new_month:Any = None
        range:int = dates.len()
        active_days:list = []
        plotter:PlotBaseMonth = PlotBaseMonth()
        for item in dates:           
            month = cal.formatmonth(item.year, item.month)            
            for date in list(self.data_frame['date']):
                if date.year == item.year and date.month == item.month:
                    active_days.append(date.day)
                    #new_month = month.replace(f'">{date.day}<', f' bg-blue-300 font-semibold">{date.day}<')
               

                    #print(f"Year: {date.year}-{item.year} / Month: {date.month}-{item.month} Date {date.day}") 
            new_month = plotter.plot_month_dates(year=item.year, range=range, active_days=active_days) 
            if new_month:
                months.append(new_month)  
                active_days = [] # Reset           
        return months

    
    def deposit_histogram(self, period:str='date',  bargap:float=0.2):
        df = self.data_frame
        fig = px.histogram(df, x=list(df["date"]), y=list(df["deposit"]), 
            title="Account Deposits Periods", 
            labels={"x": "Date Period", "y": "Deposits"},
            template="simple_white",
            width=self.chart_width, 
            height=self.chart_height 
            )
        fig.update_layout(bargap=bargap)
        #fig.show()
        return fig.to_html()


    def load_data(self, data:list=[]):
        """Load a List of DepositModels from The Project Account Deposit Transactions """
        if data:
            self.deposits = [item for item in data]
            self.update
    
   

    def heatMap(self, chart_data:dict={}):
        f_name = 'heatmap.html'
        #file = file_path(f_name)
        data=[[1, 25, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, 5, 20]]
        fig = px.imshow(
            data,
            labels=dict(x="Day of Week", y="Time of Day", color="Productivity"),
            x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            y=['Morning', 'Afternoon', 'Evening'],
            template="simple_white",
            width=self.chart_width, 
            height=self.chart_height 
        )
        fig.update_xaxes(side="top")
        #fig.write_html(file)
        return fig.to_html()
        

remote_desktop= dict(
    device_name= 'centry-main',
    rda = 'ms-rd://centry-main.local',
    vnc_address = 'vnc://centry-main.local',
    username = 'ian',
    access = 'h0tsaUce'
)