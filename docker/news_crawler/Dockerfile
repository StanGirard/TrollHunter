FROM python:3.7
ADD ../../news_crawler /news_crawler
ADD ../../requirements.txt /news_crawler
WORKDIR /news_crawler
RUN pip install -r requirements.txt
CMD ["python", "news_crawler/news_entry.py"]