from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    results = mongo.db.mars_collection.find_one()
    print(results)
    # Return template and data
    return render_template("index.html", data=results)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # run the scrape function
    mars = scrape_mars.scrape()

    # insert the mars data in to the collection
    mongo.db.mars_collection.update({}, mars, upsert=True)

    # go back to the home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)