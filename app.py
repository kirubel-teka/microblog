import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)


uri = (
    "mongodb://sekirubelteka:Haymanote1234@"
    "ac-bxlw8wp-shard-00-00.8xoi5yp.mongodb.net:27017,"
    "ac-bxlw8wp-shard-00-01.8xoi5yp.mongodb.net:27017,"
    "ac-bxlw8wp-shard-00-02.8xoi5yp.mongodb.net:27017/"
    "microblog?ssl=true&replicaSet=atlas-lqsrdy-shard-0&authSource=admin&retryWrites=true&w=majority"
)


client = MongoClient(uri)
app.db = client.microblog

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        entry_content = request.form.get("content")
        formatted_date = datetime.datetime.today().strftime('%Y-%m-%d')
        app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

    entries_with_date = {
        (
            entry["content"],
            entry["date"],
            datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%d %b %Y")    
        )
        
        for entry in app.db.entries.find({})
    }
    return render_template("home.html", entries=entries_with_date)