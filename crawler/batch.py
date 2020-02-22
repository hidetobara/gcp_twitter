import os,sys,string,traceback,random,glob,json,datetime,argparse

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './private/twitter-261302-f4efec35fd83.json'

import Manager

            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--trends', action='store_true')
    parser.add_argument('--timeline', action='store_true')
    args = parser.parse_args()
    m = Manager.Manager("./private/production.json")
    if args.trends:
        for row in m.get_trends():
            print(row)
    if args.timeline:
        for row in m.get_timeline():
            print(row)


