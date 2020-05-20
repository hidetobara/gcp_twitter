import sys,os,json,datetime,re,html,urllib

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './private/twitter-261302-f4efec35fd83.json'
from google.cloud import bigquery
import twitter
import MeCab
import emoji
from tool import strdt, strd, strpt


class Manager:
    def __init__(self, opt_path):
        self.bq_client = bigquery.Client()
        account = json.load(open('./private/hidetobara.json', 'r'))
        self.tw_api = twitter.Api(**account)
        self.mecab = MeCab.Tagger ('-d /ipadic')

        self.re_rt = re.compile(r"^RT")
        self.re_url = re.compile(r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+")
        self.re_hash = re.compile(r"#[^ ]+")
        self.re_at = re.compile(r"@[^ ]+")

        self.opt = json.load(open(opt_path, 'r'))

    def remove_emoji(self, src_str):
        return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)

    def parse_status_time(self, txt):
        created = datetime.datetime.strptime(txt, "%a %b %d %H:%M:%S +0000 %Y")
        created = created + datetime.timedelta(hours=+9) # japanese timezone
        return created

    def parse_trend_time(self, txt):
        created = datetime.datetime.strptime(txt, "%Y-%m-%dT%H:%M:%SZ")
        created = created + datetime.timedelta(hours=+9) # japanese timezone
        return created

    def insert_rows(self, rows, table_name):
        if len(rows) == 0:
            return
        if "." in table_name:
            cells = table_name.split('.')
            table_name = cells[-1]
        dataset_ref = self.bq_client.dataset("source")
        table_ref = dataset_ref.table(table_name)
        table = self.bq_client.get_table(table_ref)
        r = self.bq_client.insert_rows_json(table, rows)
        print("insert_logs=", r, "table=", table_name)
    def insert_rows_origin(self, rows):
        self.insert_rows(rows, self.opt["table"])
    def insert_rows_trend(self, rows):
        self.insert_rows(rows, self.opt["trend_table"])
    def insert_rows_sample(self, rows):
        self.insert_rows(rows, self.opt["trend_sample_table"])
    def filter_for_bq_timeline(self, rows):
        items = []
        for row in rows:
            item = {}
            print(row)
            for key in ["id", "screen_name", "text", "at_created", "by_year_month"]:
                item[key] = row[key]
            items.append(item)
        return items

    def post_status(self, text):
        self.tw_api.PostUpdate(text)

    def get_max_id(self):
        days3 = datetime.datetime.now() - datetime.timedelta(days=3)
        sql = "SELECT MAX(`id`) as max_id FROM `{}` WHERE by_year_month >= {}".format(self.opt["table"], strpt(days3))
        print("sql=", sql)
        max_id = 0
        for row in self.bq_client.query(sql).result():
            max_id = 0 if row['max_id'] is None else row['max_id']
        return max_id

    def get_timeline(self, max_id=None):
        LIMIT = 200

        statuses = self.tw_api.GetHomeTimeline(count=LIMIT,exclude_replies=True)
        rows = []
        for s in statuses:
            if max_id is not None and s.id <= max_id: continue
            at_created = self.parse_status_time(s.created_at)
            row = {"id":s.id, "screen_name":s.user.screen_name, "name":s.user.name, "text":html.unescape(s.text), "at_created":strdt(at_created), "by_year_month":strpt(at_created.date())}
            if hasattr(s.user, "profile_image_url"):
                row["profile_image_url"] = s.user.profile_image_url_https
            if hasattr(s, "media") and type(s.media) is list:
                row["media_urls"] = []
                for m in s.media:
                    if hasattr(m, "media_url_https"):
                        row["media_urls"].append(m.media_url_https)
            rows.append(row)
        return rows

    def get_timeline_from_bq(self):
        bq = json.load(open('./private/production.json', 'r'))
        days3 = datetime.datetime.now() - datetime.timedelta(days=3)
        sql = "SELECT at_created,screen_name,`text` FROM `{}` WHERE `by_year_month` >= {} ORDER BY at_created DESC LIMIT 30".format(bq["table"], strpt(days3))
        print("sql=", sql)
        tweets = []
        for row in bigquery.Client().query(sql).result():
            tweets.append({'at_created':strdt(row['at_created']), 'screen_name':row['screen_name'], 'text':row['text']})
        return tweets

    def get_trends(self):
        statuses = self.tw_api.GetTrendsWoeid(23424856)
        rows = []
        for s in statuses:
            at_created = self.parse_trend_time(s.timestamp)
            rows.append({"name":s.name, "volume":s.tweet_volume, "at_created":strdt(at_created)})
        return rows

    def get_search(self, keyword):
        statues = self.tw_api.GetSearch(raw_query="q={}%20&result_type=recent&locale=ja&count=30".format(urllib.parse.quote(keyword)))
        rows = []
        for s in statues:
            at_created = self.parse_status_time(s.created_at)
            user_at_created = self.parse_status_time(s.user.created_at)
            rows.append({"id":s.id, "keyword":keyword, "name":s.user.name, "screen_name":s.user.screen_name, "statuses_count":s.user.statuses_count,
                "text":html.unescape(s.text), "at_created":strdt(at_created),
                "user_description":html.unescape(s.user.description), "user_at_created":strdt(user_at_created)})
        return rows

    # 形態素解析する、いったんは使わない
    def decompose(self, rows):
        items = []
        for r in rows:
            try:
                for text in r['text'].split("。"):
                    if len(text) == 0: continue
                    text = self.re_rt.sub("", text)
                    text = self.re_url.sub("", text)
                    text = self.re_hash.sub("", text)
                    text = self.re_at.sub("", text)
                    text = self.remove_emoji(text)

                    node = self.mecab.parseToNode(text)
                    parts = []
                    while node:
                        word = node.surface
                        cells = node.feature.split(",")
                        pos = cells[0] if cells[1] == "*" else cells[1]
                        org = word if cells[6] == "*" else cells[6]
                        if pos != "BOS/EOS":
                            parts.append("{0}\t{1}\t{2}".format(word, pos, org))
                        node = node.next
                    items.append( {"id":r["id"], "screen_name":r["screen_name"], "text":"\n".join(parts), "at_created":r["at_created"], "by_year_month":r["by_year_month"]} )
            except Exception as ex:
                print(ex)
        return items


    

