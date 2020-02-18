import os,sys,string,traceback,random,glob,json,datetime
from flask import Flask, render_template, request, send_from_directory, redirect, jsonify

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './private/twitter-261302-f4efec35fd83.json'
from google.cloud import bigquery
import twitter
from tool import strdt, strd, strpt
import Manager


app = Flask(__name__)

@app.route('/')
def get_index():
    bq = json.load(open('./private/production.json', 'r'))
    days3 = datetime.datetime.now() - datetime.timedelta(days=3)
    sql = "SELECT at_created,screen_name,`text` FROM `{}` WHERE `by_year_month` >= {} ORDER BY at_created DESC LIMIT 30".format(bq["table"], strpt(days3))
    print("sql=", sql)
    tweets = []
    for row in bigquery.Client().query(sql).result():
        tweets.append( {'at_created':strdt(row['at_created']), 'screen_name':row['screen_name'], 'text':row['text']} )
    context = { 'title':"Current tweets.", 'tweets': tweets }
    return render_template('index.html', **context)

@app.route('/status')
def get_status():
    bq = json.load(open('./private/production.json', 'r'))
    days3 = datetime.datetime.now() - datetime.timedelta(days=3)
    sql = "SELECT FORMAT_DATETIME('%H', `at_created`) as hours, COUNT(*) as cnt FROM `{}` WHERE `at_created` > '{}' AND `by_year_month` >= {} GROUP BY hours ORDER BY hours".format(bq["table"], strd(days3), strpt(days3))
    print("sql=", sql)
    client = bigquery.Client()
    rates = []
    for row in client.query(sql).result():
        rates.append(row)
    context = { 'title':"Status", 'rates_of_tweets':rates }
    return render_template('status.html', **context)

@app.route('/update.json')
def get_update():
    m = Manager.Manager('./private/production.json')
    rows = m.get_timeline()
    m.insert_rows_origin(rows)
    items = m.decompose(rows)
    m.insert_rows_morphological(items)

    return jsonify({'result':'ok', 'max_id':m.max_id, 'count':len(rows)})

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8080)
