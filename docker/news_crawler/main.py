from TrollHunter.news_crawler import scheduler_news, scheduler_keywords
from threading import Thread
import nltk

if __name__ == "__main__":
    nltk.download('punkt')

    crawler = Thread(target=scheduler_news)
    update_keywords = Thread(target=scheduler_keywords)

    crawler.start()
    update_keywords.start()

    crawler.join()
    update_keywords.join()
