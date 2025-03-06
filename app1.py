from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    love_percentage = None
    fname = None
    sname = None
    
    if request.method == 'POST':
        fname = request.form['fname']
        sname = request.form['sname']
        
        url = f"https://flames-love-calculator.p.rapidapi.com/flame/{fname}/{sname}"

        headers = {
	        "x-rapidapi-key": "8154f5f5aemsh9e8b85c1cf796d1p1e0b28jsn40100e53075a",
	        "x-rapidapi-host": "flames-love-calculator.p.rapidapi.com"
        }
    
        
        try:
            response = requests.get(url, headers=headers)
            print(response)
            data = response.json()
            print(data)
            love_percentage = data['result']
        except:
            love_percentage = "Error: Could not calculate"

    return render_template('index.html', 
                         percentage=love_percentage,
                         fname=fname,
                         sname=sname)

if __name__ == '__main__':
    app.run()   