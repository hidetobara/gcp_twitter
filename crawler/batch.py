import os,sys,string,traceback,random,glob,json,datetime,argparse

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './private/twitter-261302-f4efec35fd83.json'

import Manager

            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--tobq', action='store_true')
    parser.add_argument('--mecab', action='store_true')
    args = parser.parse_args()
    if args.mecab:
        m = Manager.Manager("./private/production.json")
        rows = m.get_timeline()
        for item in m.decompose(rows):
            print(item)


