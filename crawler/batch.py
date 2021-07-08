import os,sys,string,traceback,random,glob,json,datetime,argparse

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './private/twitter-261302-f4efec35fd83.json'

import Manager

            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--trends', default=0, type=int)
    parser.add_argument('--timeline', default=0, type=int)
    parser.add_argument('--vrchat', action='store_true')
    parser.add_argument('--cluster', action='store_true')
    args = parser.parse_args()
    m = Manager.Manager("./private/production.json")
    if args.trends:
        for row in m.get_trends():
            for i, s in enumerate(m.get_search(row['name'])):
                if i >= args.trends: break
                print(s)
    if args.timeline:
        for i, row in enumerate(m.get_timeline()):
            if i >= args.timeline: break
            print(i, row)
    if args.vrchat:
        for i, row in enumerate(m.get_search(['#VRChat', '#VRC'])):
            print(i, row)
    if args.cluster:
        for i, row in enumerate(m.get_search('#Cluster')):
            print(i, row)


