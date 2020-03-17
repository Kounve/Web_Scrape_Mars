from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():

    # Find one record of data from the mongo database
    data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars=data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function s
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
