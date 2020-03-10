FROM python:3.7
WORKDIR /news_crawler
COPY . .
RUN pip install TrollHunter
RUN pip install -r requirements.txt

CMD ["python", "./main.py"]