from flask import *
import sqlite3
import requests

app = Flask(__name__)

weather_api_key="400eb01df4e34a908e993414250103"
@app.route("/")
def home():
    return render_template("auth/signup.html")

@app.route("/signup_message", methods=["POST"])
def signup():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    conn = sqlite3.connect("Database/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
    existing_user = cursor.fetchone()
    if existing_user:
        conn.close()
        return render_template("result.html", value="Error: Username or Email already exists!")
    else:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        conn.close()
        return render_template("result.html", value="Signup Successful!")


@app.route("/login")
def login():
    return render_template("auth/login.html")

@app.route("/login_message", methods=["POST"])
def login_message():
    email = request.form["email"]
    password = request.form["password"]
    conn = sqlite3.connect("Database/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return render_template("select_api.html")
    else:
        return render_template("result.html", value="Invalid Email or Password!")

@app.route("/crypto_currency_api")
def api():
    return render_template("currency_api/api_call.html")

@app.route("/get_price", methods=["POST"])
def get_price():
    crypto = request.form["crypto"].lower()
    currency = request.form["currency"].lower()
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies={currency}"
    response = requests.get(url)
    data = response.json()
    print("Response JSON:", data)  
    if response.status_code == 200 :
        price = data[crypto][currency]
        return render_template("currency_api/api_call_result.html", crypto=crypto.capitalize(), currency=currency.upper(), price=price)
    else:
        return render_template("currency_api/api_call_result.html", error="Invalid cryptocurrency or currency!")



@app.route("/weather")
def weather():
    return render_template("weather/weather_api_call.html")

@app.route("/get_weather", methods=["GET", "POST"])
def get_weather():
    if request.method == "POST":
        city = request.form["city"]
        url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}"
        
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temperature = data["current"]["temp_c"]
            latitude = data["location"]["lat"]
            longitude = data["location"]["lon"]
            country = data["location"]["country"]
            condition = data["current"]["condition"]["text"]
            icon = data["current"]["condition"]["icon"]
            localtime = data["location"]["localtime"]  # Get local time from JSON

            return render_template("weather/weather_api_call.html", 
                                   city=city.capitalize(), 
                                   temperature=temperature, 
                                   latitude=latitude, 
                                   longitude=longitude, 
                                   country=country, 
                                   condition=condition,
                                   icon=icon,
                                   localtime=localtime)  # Pass localtime to template
        else:
            return render_template("weather/weather_api_call.html", error="Invalid city name or API error!")

    return render_template("weather/weather_api_call.html")





if __name__ == "__main__":
    app.run(debug=True)


