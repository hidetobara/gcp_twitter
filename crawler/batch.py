import os,sys,string,traceback,random,glob,json,datetime,argparse

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './private/twitter-261302-f4efec35fd83.json'
from google.cloud import bigquery
import twitter

from tool import strdt, strd, strpt

def upload_to_bq():
    client = bigquery.Client()
    sql = "SELECT MIN(`id`) as min_id FROM `{}`".format("twitter-261302.source.my_timeline")
    print("sql=", sql)
    for row in client.query(sql).result():
        min_id = None if row['min_id'] is None else row['min_id']
    print("min_id=", min_id)
    with open('data/home.txt', 'r') as f:
        rows = []
        for line in f:
            cells = line.strip().split("\t")
            if len(cells) < 4: continue
            tid = int(cells[0])
            at_created = datetime.datetime.strptime(cells[1], "%Y-%m-%d %H:%M:%S")
            at_created_date = at_created.date()
            screen_name = cells[2]
            text = cells[3]
            if tid > min_id:
                print("min_id exceed tid=", tid)
                break
            rows.append( {"id":tid, "screen_name":screen_name, "text":text, "at_created":strdt(at_created), "by_year_month":strpt(at_created_date), } )
            if len(rows) >= 1000:
                insert_rows(client, rows)
                rows = []
                break
        insert_rows(client, rows)
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--tobq', action='store_true')
    args = parser.parse_args()
    if args.tobq:
        upload_to_bq()


