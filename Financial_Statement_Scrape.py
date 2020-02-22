import pandas as pd
from bs4 import BeautifulSoup
import urllib.request as ur
import datetime


tickers = ["GOOG","NFLX","FB","AMZN"]

income_statements = {}
balance_sheets = {}
cash_flows = {}

for index,ticker in enumerate(tickers):

    # Create URLs
    url_is = "https://finance.yahoo.com/quote/" + ticker + "/financials?p=" + ticker
    url_bs = "https://finance.yahoo.com/quote/" + ticker + "/balance-sheet?p=" + ticker
    url_cf = "https://finance.yahoo.com/quote/" + ticker + "/cash-flow?p="+ ticker
    
    
##### Income Statements    
    
    # Read URLs
    read_data_income_statement = ur.urlopen(url_is).read() 
    soup_is = BeautifulSoup(read_data_income_statement,"lxml")
    print(ticker + " - Income Statement")

    # Assess how many years are posted to Yahoo Finance
    ls= [] 
    for l in soup_is.find_all("div"):          
        #Find all data structure that is ‘div’
        ls.append(l.string) # add each element one by one to the list
        ls = [e for e in ls if e not in ("Operating Expenses","Non-recurring Events")] # Exclude those columns
        new_ls = list(filter(None,ls))
        new_ls = new_ls[12:]  
        new_ls = [x.replace(",", "") for x in new_ls]
  
    if str(datetime.date.today().year - 1) in new_ls[2]:
        x = 6
    else:
        x = 5

    print(new_ls[2])

    ls= [] 
    for l in soup_is.find_all("div"): 
        
        #Find all data structure that is ‘div’
        ls.append(l.string) # add each element one by one to the list
        ls = [e for e in ls if e not in ("Operating Expenses","Non-recurring Events")] # Exclude those columns
        new_ls = list(filter(None,ls))
        new_ls = new_ls[12:]
        new_ls = [x.replace(",", "") for x in new_ls]
        is_data = list(zip(*[iter(new_ls)]*x))
        income_statements[ticker] = pd.DataFrame(is_data[0:])
        income_statements[ticker].iloc[1:,1:] = (income_statements[ticker].iloc[1:,1:].apply(pd.to_numeric,errors="coerce") * 1000)
        
    read_data_cash_flow = ur.urlopen(url_cf).read() 
    soup_cf = BeautifulSoup(read_data_cash_flow,"lxml")
    print(ticker + " - Cash Flow")



####### Cash Flow

    # Assess how many years are posted to Yahoo Finance
    ls= [] 
    for l in soup_cf.find_all("div"):          
        #Find all data structure that is ‘div’
        ls.append(l.string) # add each element one by one to the list
        ls = [e for e in ls if e not in ("Operating Expenses","Non-recurring Events")] # Exclude those columns
        new_ls = list(filter(None,ls))
        new_ls = new_ls[12:]  
        new_ls = [x.replace(",", "") for x in new_ls]
  
    if str(datetime.date.today().year - 1) in new_ls[2]:
        x = 6
    else:
        x = 5

    print(new_ls[2])

    ls= [] 
    for l in soup_cf.find_all("div"): 
        
        #Find all data structure that is ‘div’
        ls.append(l.string) # add each element one by one to the list
        ls = [e for e in ls if e not in ("Operating Expenses","Non-recurring Events")] # Exclude those columns
        new_ls = list(filter(None,ls))
        new_ls = new_ls[12:]
        new_ls = [x.replace(",", "") for x in new_ls]
        
        is_data = list(zip(*[iter(new_ls)]*x))
        cash_flows[ticker] = pd.DataFrame(is_data[0:]) 
        cash_flows[ticker].iloc[1:,1:] = (cash_flows[ticker].iloc[1:,1:].apply(pd.to_numeric,errors="coerce")*1000)


###### Balance Sheet        
        
    read_data_balance_sheet = ur.urlopen(url_bs).read() 
    soup_bs = BeautifulSoup(read_data_balance_sheet,"lxml")
    print(ticker + " - Balance Sheet")
    

    # Assess how many years are posted to Yahoo Finance
    ls= [] 
    for l in soup_bs.find_all("div"):          
        #Find all data structure that is ‘div’
        ls.append(l.string) # add each element one by one to the list
        ls = [e for e in ls if e not in ("Operating Expenses","Non-recurring Events")] # Exclude those columns
        new_ls = list(filter(None,ls))
        new_ls = new_ls[12:]  
        new_ls = [x.replace(",", "") for x in new_ls]
  
    if str(datetime.date.today().year - 1) in new_ls[1]:
        x = 5
    else:
        x = 4   

    print(new_ls[1])


    ls = []
    for l in soup_bs.find_all("div"): 
        
        #Find all data structure that is ‘div’
        ls.append(l.string) # add each element one by one to the list
        ls = [e for e in ls if e not in ("Operating Expenses","Non-recurring Events")] # Exclude those columns
        new_ls = list(filter(None,ls))
        new_ls = new_ls[12:]
        new_ls = [x.replace(",", "") for x in new_ls]
        is_data = list(zip(*[iter(new_ls)]*x))
        balance_sheets[ticker] = pd.DataFrame(is_data[0:])
        balance_sheets[ticker].iloc[1:,1:] = (balance_sheets[ticker].iloc[1:,1:].apply(pd.to_numeric,errors="coerce")*1000)
        
        
    # Index and name columns of statements    
    income_statements[ticker] = income_statements[ticker].rename(columns=income_statements[ticker].iloc[0,:], index=income_statements[ticker].iloc[:,0])
    income_statements[ticker] = income_statements[ticker].drop(columns='Annual',index='Annual')
    cash_flows[ticker] = cash_flows[ticker].rename(columns=cash_flows[ticker].iloc[0,:], index=cash_flows[ticker].iloc[:,0])
    cash_flows[ticker] = cash_flows[ticker].drop(columns='Annual',index='Annual')
    balance_sheets[ticker] = balance_sheets[ticker].rename(columns=balance_sheets[ticker].iloc[0,:], index=balance_sheets[ticker].iloc[:,0])
    balance_sheets[ticker] = balance_sheets[ticker].drop(columns='Annual',index='Annual')

    with pd.ExcelWriter('/Users/kevin/Documents/FinancialStatements/' + str(ticker) + '.xlsx') as writer:
        income_statements[ticker].to_excel(writer, sheet_name='Income Statement')
        cash_flows[ticker].to_excel(writer, sheet_name='Cash Flow')
        balance_sheets[ticker].to_excel(writer, sheet_name='Balance Sheet')
        
        
        
    print("---------------------------------------------------------------------")
      
        


       
        
        
        

        
        
        
        
