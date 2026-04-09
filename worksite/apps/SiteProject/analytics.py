import datetime as dt
import calendar
import polars as pol
import plotly.express as px
from typing import Any
from pydantic import BaseModel
from bs4 import BeautifulSoup
from core.baseModels.accounting_models import DepositModel
from core.utilities.utils import convert_timestamp, to_dollars
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
    chart_width:int= 500
    chart_height:int= 380     

    @property
    def update(self):
        for deposit in self.deposits:
            date_str:str = convert_timestamp(deposit.date)  # type: ignore
            self.dates.append(dt.date.fromisoformat(date_str)) # type: ignore
        #self.dates = [item.date for item in self.deposits ] # type: ignore
        self.amounts = [item.amount for item in self.deposits ]

    def timestamp_to_date(self, time_stamp:int):
        date_str:str = convert_timestamp(time_stamp)  # type: ignore
        return dt.date.fromisoformat(date_str)

    ## Data Frames
    @property
    def base_data_frame(self):
        # Containers
        deposits = dict(
            date=[],
            amount=[],
            day=[]
        )
        # Load containers
        for item in self.deposits:
            deposits['date'].append( self.timestamp_to_date(item.date))
            deposits['amount'].append(item.amount)
            deposits['day'].append(self.timestamp_to_date(item.date).day)
        # Construct The DaraFrame   
        df = pol.DataFrame(deposits)
        #print(f"Size: {df.estimated_size()} b") 
        return df  
    
    @property
    def data_frame(self):
        df = pol.DataFrame({
            "date": self.dates,
            "deposit": self.amounts            
        })       
        return df   
    
    ## Monthly 
    def group_data_frame(self, period:str="1mo"):
        df = self.data_frame
        frame = df.group_by_dynamic("date", every=period, closed="right").agg(pol.col("deposit").sum())
        return frame
    
    
    @property
    def deposit_days(self):
        date_deposit = {}
        dates = set([self.timestamp_to_date(deposit.date) for deposit in self.deposits ])        
        for date in dates:
            key = f'{date.day}_{date.month}'
            date_deposit[key] = set()
            for deposit in self.deposits:
                d_day=self.timestamp_to_date(deposit.date)
                c_key = f'{d_day.day}_{d_day.month}'
                if c_key in date_deposit.keys():                    
                    date_deposit[c_key].add(deposit.amount)       
        return date_deposit


    def plot_month_higlight_dates(self, html, dates:dict={}):
        soup = BeautifulSoup(html, 'html.parser')
        # style the table
        table = soup.find('table')
        table.attrs['class'].append('bg-base-50 text-xs shadow-sm w-64') # type: ignore        
        tds = soup.find_all('td')    
          
        for td in tds:
            if td.text in dates.keys():
                new_tag = soup.new_tag("span", attrs={"class":"badge badge-outline badge-xs badge-primary p-1"})
                new_tag.insert(0, td.text)
                new_tag.attrs['uk-tooltip'] = f"Amount Deposited {to_dollars(dates.get(td.text))}" # type: ignore               
                td.clear()
                td.append(new_tag)              
        
        return(soup)


    @property
    def calendars(self):
        ''' '''
        dates = self.group_data_frame(period="1mo")["date"]
        cal = calendar.HTMLCalendar(firstweekday=0)
        #cal2 = calendar.TextCalendar(firstweekday=0)
        months:list= []
        new_month:Any = None        
        active_days:dict= {}
       
        for item in dates:           
            month = cal.formatmonth(item.year, item.month)            
            for date in list(self.data_frame['date']):
                key = f'{date.day}_{date.month}'
                daily_deposit = round(sum(self.deposit_days.get(key)),2) # type: ignore # Total daily deposit                
                if date.year == item.year and date.month == item.month:
                    active_days[str(date.day)] = daily_deposit  
            if month: 
                new_month = self.plot_month_higlight_dates(month, active_days) 
                months.append(new_month)  
                active_days = {} # Reset           
        return months

    
    def deposit_histogram(self, period:str='date',  bargap:float=0.2):
        df = self.data_frame
        fig = px.histogram(df, x=list(df["date"]), y=list(df["deposit"]), 
            #title="Account Deposits Periods", 
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
    
   

    def heatMap(self, chart_data:dict={}, period='1d'):
        df = self.base_data_frame #(period='1mo')
        #frame = df.group_by("date", every=period, closed="right").agg(pol.col("deposit").sum())
        #print(df)
        f_name = 'heatmap.html'
        #file = file_path(f_name)
        data=[[1, 25, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, 5, 20]]

        fig = px.imshow([  list(item.month for item in df['date']),list(df['amount']), list(df['day']),  ],
            labels=dict(x="Date", y="Month", color="Amount"),
            
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