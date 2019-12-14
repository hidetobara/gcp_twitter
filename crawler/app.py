import os,sys,string,traceback,random,glob,json,datetime
from flask import Flask, render_template, request, send_from_directory, redirect, jsonify

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './private/twitter-261302-f4efec35fd83.json'
from google.cloud import bigquery
import twitter

app = Flask(__name__)

def strdt(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")
def strd(dt):
    return dt.strftime("%Y-%m-%d")

@app.route('/')
def get_index():
    bq = json.load(open('./private/bigquery.json', 'r'))
    days3 = datetime.datetime.now() - datetime.timedelta(days=3)
    sql = "SELECT at_created,screen_name,`text` FROM `{}` WHERE `at_created_date` > '{}' ORDER BY at_created DESC LIMIT 30".format(bq["table"], strd(days3))
    print("sql=", sql)
    tweets = []
    for row in bigquery.Client().query(sql).result():
        tweets.append( {'at_created':strdt(row['at_created']), 'screen_name':row['screen_name'], 'text':row['text']} )
    context = { 'title':"Current tweets.", 'tweets': tweets }
    return render_template('index.html', **context)

@app.route('/status')
def get_status():
    bq = json.load(open('./private/bigquery.json', 'r'))
    days3 = datetime.datetime.now() - datetime.timedelta(days=3)
    sql = "SELECT FORMAT_DATETIME('%H', `at_created`) as hours, COUNT(*) as cnt FROM `{}` WHERE `at_created_date` > '{}' GROUP BY hours ORDER BY hours".format(bq["table"], strd(days3))
    print("sql=", sql)
    client = bigquery.Client()
    rates = []
    for row in client.query(sql).result():
        rates.append(row)
    context = { 'title':"Status", 'rates_of_tweets':rates }
    return render_template('status.html', **context)

@app.route('/update.json')
def get_update():
    LIMIT = 200
    account = json.load(open('./private/hidetobara.json', 'r'))
    bq = json.load(open('./private/bigquery.json', 'r'))

    days3 = datetime.datetime.now() - datetime.timedelta(days=3)
    client = bigquery.Client()
    sql = "SELECT MAX(`id`) as max_id FROM `{}` WHERE at_created_date > '{}'".format(bq["table"], strd(days3))
    print("sql=", sql)
    max_id = 0
    for row in client.query(sql).result():
        max_id = 0 if row['max_id'] is None else row['max_id']

    api = twitter.Api(**account)
    statuses = api.GetHomeTimeline(count=LIMIT,exclude_replies=True)
    rows = []
    for s in statuses:
        if s.id <= max_id: continue
        at_created = datetime.datetime.strptime(s.created_at, "%a %b %d %H:%M:%S +0000 %Y")
        at_created = at_created + datetime.timedelta(hours=+9) # japanese timezone
        at_created_date = at_created.date()
        rows.append({"id":s.id, "screen_name":s.user.screen_name, "text":s.text, "at_created":strdt(at_created), "at_created_date":strd(at_created_date)})

    if len(rows) > 0:
        dataset_ref = client.dataset("source")
        table_ref = dataset_ref.table("my_timeline")
        table = client.get_table(table_ref)
        client.insert_rows_json(table, rows)

    return jsonify({'result':'ok', 'max_id':max_id, 'count':len(rows), 'limit':LIMIT})

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8080)
