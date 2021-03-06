from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    data = mongo.db.data.find_one()

    # Return template and data
    return render_template("index.html", mars=data)


# Route that will trigger the scrape function by import scrape_mars
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.data.update({}, mars_data, upsert=True)
    
    print(mars_data)

    # Redirect back to home page
    #return redirect("/")
    return "Scraping successing!"

if __name__ == "__main__":
    app.run(debug=True)
