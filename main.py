from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from utility import get_next_earnings_date

app = Flask(__name__)

raw_df = pd.read_csv('data/nasdaq_screener_20240218.csv')
countries = raw_df['Country'].unique().tolist()
sectors = raw_df['Sector'].unique().tolist()
if "Technology" in sectors:
        sectors.remove("Technology")
        sectors.insert(0, "Technology")

@app.route('/', methods=['GET', 'POST'])
def index():
    df = raw_df.copy()

    selected_country = request.form.get('country', default='United States')
    selected_sector = request.form.get('sector', default='Technology')

    if selected_country:
        df = df[df['Country'] == selected_country]

    if selected_sector:
        df = df[df['Sector'] == selected_sector]

    df = df.drop(columns=['Country', 'Sector']).sort_values('Volume', ascending=False)
        
    #format table columns
    df['IPO Year'] = df['IPO Year'].astype(str).apply(lambda x: x.split('.')[0])
    df['Market Cap'] = df['Market Cap'].replace([np.inf, -np.inf, np.nan], 0).astype(int).apply(lambda x: '{:,}'.format(x))
    df['Volume'] = df['Volume'].replace([np.inf, -np.inf, np.nan], 0).astype(int).apply(lambda x: '{:,}'.format(x))

    #add earnings date
    #df['NextEarningsDate'] = df['Symbol'].astype(str).apply(get_next_earnings_date)
    #.astype(str).apply(get_next_earnings_date)ß
    #.dt.strftime('%Y-%m-%d %H')
    
    return render_template('index.html', table=df.to_html(index=False), 
                           countries=countries, sectors=sectors,
                           selected_country=selected_country, selected_sector=selected_sector)

if __name__ == '__main__':
    app.run(debug=True)
