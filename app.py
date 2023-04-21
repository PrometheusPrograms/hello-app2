import re
from datetime import datetime
import git
import subprocess
import requests
from bs4 import BeautifulSoup
import pdfminer
import threading
import pandas as pd
import plotly.graph_objs as go


from flask import Flask, request, redirect, render_template
from flask.wrappers import Response

import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields import DateField

from forms import StockForm

import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)





#@app.route("/")
#def home():
#    return "Hello, Flask bitch 123!"
  #  return redirect("/tesla_closing_price")

'''
def main(): 
    symbol = "AAPL"
    data = yf.download(symbol, start="2022-01-01", end="2022-03-31")
    closing_prices = data["Adj Close"]
    df = pd.DataFrame({"Closing Prices": closing_prices})
    table_html = df.to_html()
    return render_template("index.html", table=table_html)

@app.route("/stock_data")
def stock_data():
    return main()
'''

@app.route("/", methods=["GET", "POST"])
def home():
    form = StockForm()
  #  symbol = "AAPL"  # Default value
#    start_date = "2022-01-01"  # Default value
 #   end_date = "2022-03-31"  # Default value
    if request.method == "POST":
        # Retrieve stock data using yfinance
        symbol = request.form.get("symbol")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        data = yf.download(symbol, start=start_date, end=end_date)
        closing_prices = data["Adj Close"]
        
        # Convert data to a Pandas DataFrame
        df = pd.DataFrame({"Closing Prices": closing_prices})
        
        # Convert DataFrame to an HTML table
        table_html = df.to_html()
        
        # Create a Plotly figure
        fig = go.Figure(data=[go.Scatter(x=df.index, y=df["Closing Prices"])])
        fig.update_layout(title="Closing Prices for {}".format(symbol))

        # Convert the Plotly figure to JSON
        graph_json = fig.to_json()

        # Render the HTML template with the Plotly graph
        #return render_template("index.html", table=table_html,graph_json=graph_json)
        return render_template("index.html", form=form, graph_json=graph_json)

    # Render the HTML template with an empty form
    return render_template("index.html",form=form)  


#if __name__ == "__main__":
 #   app.run(debug=True)
    

  #  plt.plot(closing_prices)
  #  plt.show()

def plot_graph():
    plt.ion() # turn on interactive mode
    symbol = "AAPL"
    data = yf.download(symbol, start="2022-01-01", end="2022-03-31")
    closing_prices = data["Adj Close"]
    plt.plot(closing_prices)
    plt.show()
    threading.Thread(target=plot_graph).start()

'''
@app.route('/tesla_closing_price', methods=['GET'])
def tesla_closing_price():
# Set the ticker symbol for Tesla
    ticker = "TSLA"

# Calculate the date range for the last 5 days
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d')

# Retrieve the stock data for the specified date range
    stock_data = yf.download(ticker, start=start_date, end=end_date)

# Extract the closing price data for the last 5 days
    closing_prices = stock_data['Close']

# Plot the closing prices on a line chart
    plt.plot(closing_prices)
    plt.title("Tesla Closing Prices for the Last 5 Days")
    plt.xlabel("Date")
    plt.ylabel("Closing Price ($)")
    plt.show()
'''
    
@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content
'''
@app.route('/update', methods=['POST'])
def webhook():
        if request.method == 'POST':
            repo = git.Repo('./hello-app2')
            origin = repo.remotes.origin
            repo.create_head('main',origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
            origin.pull()
            return 'Updated PythonAnywhere successfully', 200
        else:
            return 'Wrong event type', 400
'''
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True,)


@app.route('/update', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Pull changes from the GitHub repo
        subprocess.run(['git', '-C', './hello-app2', 'pull', 'origin','master'])
        # Restart the app to load the new code
        subprocess.run(['touch', '/var/www/greenmangroup_pythonanywhere_com_wsgi.py'])
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400






'''

def scrape_10k_filings():
    # Use the requests library to send a GET request to the Tesla investor relations webpage
    url = 'https://ir.tesla.com/sec-filings'
    response = requests.get(url)
    
    # Use BeautifulSoup to parse the HTML of the webpage and extract the links to the 10-K filings
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.endswith('.pdf') and '10-K' in href:
            links.append(href)
    
    # Download the 10-K filings using the links obtained in the previous step
    earnings_data = []
    for link in links:
        response = requests.get(link)
        with open('filename.pdf', 'wb') as f:
            f.write(response.content)
        
        # Use pdfminer to extract the earnings data from the PDFs of the 10-K filings
        with open('filename.pdf', 'rb') as f:
            # Use pdfminer to extract the text from the PDF
            # Parse the text to extract the earnings data
            earnings = parse_earnings(text)
            earnings_data.append(earnings)
    
    return earnings_data

def parse_earnings(text):
    # Use regular expressions to extract the earnings data from the text
    # Return a dictionary containing the earnings data for that year
    return earnings_dict

@app.route('/tesla_earnings', methods=['GET'])
def tesla_earnings():
    # Scrape the 10-K filings and extract the earnings data
    earnings_data = scrape_10k_filings()
    
    # Use matplotlib to plot the earnings data
    plot_earnings(earnings_data)
    
    # Upload the earnings data to Tableau and create a visualization
    upload_to_tableau(earnings_data)
    
    # Return a response to the user
    return Response('Tesla earnings data plotted and uploaded to Tableau')
'''