import datetime as dt
import calendar
import polars as pol
import plotly.express as px
from asyncio import run
from pydantic import BaseModel
from apps.SiteProject.project import ( create_project, read_project, delete_project, get_workers , get_worker, all_projects, get_account)
from core.baseModels.project_models import Project
from core.baseModels.accounting_models import DepositModel
from core.utilities.utils import convert_timestamp, converTime


ids = ['KS03093','LM8603']

class IncomeDataFrame(BaseModel):
    deposits:list[DepositModel] = []
    dates:list[str] = []
    amounts:list[float] = []
    
    @property
    def data_frame(self):
        df = pol.DataFrame({
            "deposit": self.amounts,
            "date": self.dates
        })
        return df


    def load_data(self, data:list=[]):
        if data:
            self.deposits = [item for item in data]
            self.update
    
    @property
    def update(self):
        for deposit in self.deposits:
            date_str:str = convert_timestamp(deposit.date) 
            self.dates.append(dt.date.fromisoformat(date_str)) # type: ignore
        #self.dates = [item.date for item in self.deposits ] # type: ignore
        self.amounts = [item.amount for item in self.deposits ]



async def projects():
    all_p =  await all_projects()
    print(all_p)


async def project_expenditure(project_id:str=''):
    project:Project | dict = await read_project(id=project_id)
    if project:
        project.load_account() # type: ignore
        frame:IncomeDataFrame= IncomeDataFrame()
        frame.load_data( project.account.transactions.deposit)  # type: ignore
        date = frame.dates[4]
        cal = calendar.HTMLCalendar(firstweekday=0)
        month = cal.formatmonth(date.year, date.month)
        df = frame.data_frame
        #df.group_by("dates",  maintain_order=True)
        #df.filter(pol.col("dates") > date)
        nf = df.group_by_dynamic("date", every="1d", closed="right").agg(pol.col("deposit").sum())
        print(nf)

   

if __name__ == '__main__':
    run( project_expenditure( ids[0] ) )
    print( px.data.stocks())
    #print(calendar.)