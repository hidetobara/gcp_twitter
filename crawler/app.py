import os,sys,string,traceback,random,glob,json,datetime
from flask import Flask, render_template, request, send_from_directory, redirect, jsonify

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './private/twitter-261302-f4efec35fd83.json'
from google.cloud import bigquery
import twitter
from tool import strdt, strd, strpt
import Manager


app = Flask(__name__)
m = Manager.Manager('./private/production.json')

@app.route('/')
def get_index():
    tweets = m.get_timeline()

    context = { 'title':"Current tweets.", 'tweets': tweets }
    return render_template('index.html', **context)

@app.route('/status', methods=['POST'])
def post_status():
    if request.method == 'POST':
        text = request.form['content']
        m.post_status(text)
    return redirect('/')

@app.route('/info', methods=['GET'])
def get_info():
    bq = json.load(open('./private/production.json', 'r'))
    days3 = datetime.datetime.now() - datetime.timedelta(days=3)
    client = bigquery.Client()

    sql = "SELECT FORMAT_DATETIME('%H', `at_created`) as hours, COUNT(*) as cnt FROM `{}` WHERE `at_created` > '{}' AND `by_year_month` >= {} GROUP BY hours ORDER BY hours".format(bq["table"], strd(days3), strpt(days3))
    print("sql=", sql)
    rates = []
    for row in client.query(sql).result():
        rates.append(row)

    sql = "SELECT `name`, MAX(`volume`) as _sum FROM `{}` WHERE `at_created` > '{}' GROUP BY name ORDER BY _sum DESC LIMIT 10".format(bq["trend_table"], strd(days3))
    print("sql=", sql)
    trends = []
    for row in client.query(sql).result():
        trends.append(row)

    context = { 'title':"info", 'rates_of_tweets':rates, 'trends':trends }
    return render_template('info.html', **context)

@app.route('/update.json')
def get_update():
    rows = m.get_timeline(max_id=m.get_max_id())
    m.insert_rows_origin(m.filter_for_bq_timeline(rows))

    return jsonify({'result':'ok', 'rows':len(rows)})

@app.route('/trends.json')
def get_trends():
    trends = m.get_trends()
    m.insert_rows_trend(trends)

    m.insert_rows_samples(m.get_search(['#VRChat', '#VRC']))
    m.insert_rows_samples(m.get_search('#Cluster'))
    m.insert_rows_samples(m.get_search('#VRC撮影の集い'))

    return jsonify({'result':'ok', 'trends':len(trends)})

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8080)
