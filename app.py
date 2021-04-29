import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
import plotly.express as px
from plotly.graph_objs import *

layout = Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)


stock_list = pd.read_csv("https://www1.nseindia.com/content/indices/ind_nifty500list.csv")
stock_list = list(stock_list["Symbol"])

stock = st.selectbox("Select Stock",[''] + stock_list)

if stock :
    end = datetime.now()
    start = datetime.now() - relativedelta(years=12)
    data = yf.download(stock+'.NS',start=start,end=end,threads=True)


    period_list = ['1 Day','1 Week','1 Month','3 Months','6 Months','1 Year','3 Years','5 Years','7 Years','10 Years']
    #[days,weeks,months,years]
    pl = [[0,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,3,0],[0,0,6,0],[0,0,0,1],[0,0,0,3],[0,0,0,5],[0,0,0,7],[0,0,0,10]]
    period = st.selectbox("Select Period",period_list)

    ind = period_list.index(period)

    if ind == 0 :
        daily = (100 * data.Close[-1])/data.Close[-2] - 100
        st.write(period + " return is : " + str(round(daily,2)) + "%") 
        temp_data = yf.download(tickers=stock+'.NS', period="1d", interval="15m")
        temp_data = temp_data.reset_index()[['Datetime','Close']]
        temp_data.Datetime = temp_data.Datetime.apply(lambda x : str(x)[11:16])
        fig = px.line(temp_data,y='Close',x='Datetime')
        fig.update_layout(layout)
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig)

    else :
        dates = data.index[-1] - relativedelta(days=pl[ind][0],weeks=pl[ind][1],months=pl[ind][2],years=pl[ind][3])

        while True :
            try :
                ret = (100 * data.Close[-1])/data.loc[dates.strftime("%Y-%m-%d")].Close - 100
                st.write(period + " return is : " + str(round(ret,2)) + "%") 
                temp_data = data.loc[dates:,'Close'].reset_index()
                fig = px.line(temp_data,y='Close',x='Date')
                fig.update_layout(layout)
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False)
                st.plotly_chart(fig)
                break
            except :
                dates = dates + relativedelta(days=1)