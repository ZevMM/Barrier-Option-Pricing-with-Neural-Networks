from scipy.interpolate import griddata
import requests
from datetime import date

def Get_Date():
    query = '''SELECT `date`
    FROM `option_chain`
    ORDER BY `date` DESC
    LIMIT 1;
    '''
    res = requests.get(
    'https://www.dolthub.com/api/v1alpha1/post-no-preference/options',
    params={'q': query}
    )

    return res.json()["rows"][0]["date"]

def Get_Points_Vals(asset):
    d = Get_Date()
    query = '''SELECT `date`, `act_symbol`, `expiration`, `strike`, `bid`, `vol`
    FROM `option_chain`
    WHERE `act_symbol` = '{}' AND `call_put` = 'Call' AND `date` = "{}"
    '''.format("AAPL", d)
    res = requests.get(
    'https://www.dolthub.com/api/v1alpha1/post-no-preference/options',
    params={'q': query}
    )

    options = res.json()['rows']
    points = []
    values = []
    price = Get_Price(asset)
    for o in options:
        toAppend = []
        toAppend.append(float(o['strike'])/price)
        yr, month, day = [int(x) for x in o['date'].split('-')]
        cur = date(yr, month, day)
        yr, month, day = [int(x) for x in o['expiration'].split('-')]
        expiration = date(yr, month, day)
        toAppend.append((expiration - cur).days)
        points.append(toAppend)
        values.append(float(o['bid']))
        #might wanna average bid and ask
        #yeah I need to do some kinda filtering by bid
    return points, values

def Get_Price(asset):
    d = Get_Date()
    res = requests.get(
    'https://api.polygon.io/v2/aggs/ticker/{}/range/1/day/{}/{}?adjusted=true&sort=asc&limit=120&apiKey=pTb5_jDgptuLl8wKxz2XKIfCQd4CCwYY'.format(asset, d, d)
    )
    return res.json()["results"][0]['vw']

def European_Price(asset, strike, time):
    price = Get_Price(asset)
    moneyness = float(strike) / price
    points, vals = Get_Points_Vals(asset)
    return griddata(points, vals, (moneyness, time), method='cubic')

def Get_Risk_Free_Rate():
    res = requests.get(
    'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates?fields=record_date,avg_interest_rate_amt,src_line_nbr&sort=-record_date&filter=src_line_nbr:eq:3&limit=1',
    )
    return float(res.json()['data'][0]['avg_interest_rate_amt']) / 100
