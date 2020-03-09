---
title: "Introduction to Troll hunter"
keywords: TrollHunter, troll, hunter
tags: [getting_started]
sidebar: mydoc_sidebar
permalink: index.html
summary: Everything we need to save
---


  

# Kibana

Link is [http://kibana.trollhunter.guru](http://kibana.trollhunter.guru)
Login: elastic, mdp: changeme

# Server

Link is [http://server.trollhunter.guru](http://server.trollhunter.guru)

## SSH
`ssh root@142.93.170.234`


# Twint

`twint -s pineapple --since "2020-02-26 20:00:00" -es elastic:changeme@142.93.170.234:9200`

# Postgres
http://server.trollhunter.guru:8080/ for adminer
login: postgres
mdp: trollhunter

# Twitter crawler
## Launch worker
  celery -A request worker --loglevel=info --app=twitter_crawler.celeryapp
