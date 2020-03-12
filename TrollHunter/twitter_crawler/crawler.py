import getopt
import sys
from TrollHunter.twitter_crawler.twint import twint
from TrollHunter.twitter_crawler.twint_api.request_twint import get_twint_config

def print_help():
    print("""
    args:
    tweet:          set to 0 to avoid tweet (default: 1)
    follow:         set to 0 to avoid follow (default: 1)
    limit:          set the number of tweet to retrieve (Increments of 20, default: 100)
    follow_limit    set the number of following and followers to retrieve 
    since:          date selector for tweets (Example: 2017-12-27)
    until:          date selector for tweets (Example: 2017-12-27)
    retweet:        set to 1 to retrieve retweet (default: 0)
    search:         search terms)""")
def run(argv):
    opts = None
    dict_args = {"tweet":1,"follow":1,"limit":100,"follow_limit":-1,"since":None,"until":None,"retweet":0,"search":None}
    try:
        opts, args = getopt.getopt(argv, "ht:f:l:rs:u:", ["help", "tweet=","follow=","limit=","retweet","since=","until=","follow_limit=","search="])

    except getopt.GetoptError as e:
        print_help()
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
        elif opt in ("-t", "--tweet"):
            dict_args["tweet"] = arg
        elif opt in ("-f", "--follow"):
            dict_args["follow"] = arg
        elif opt in ("-l","--limit"):
            dict_args["limit"] = arg
        elif opt in ("--follow_limit"):
            dict_args["follow_limit"] = arg
        elif opt in ("-s","--since"):
            dict_args["since"] = arg
        elif opt in ("-u", "--until"):
            dict_args["until"] = arg
        elif opt in ("-r","--retweet"):
            dict_args["retweet"] = 1
        elif opt in ("--search"):
            dict_args["follow"] = arg
    crawl(dict_args)

def crawl(args):
    print(args)

if __name__ == '__main__':
    run(sys.argv[1:])