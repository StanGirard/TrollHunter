CREATE TABLE public.trust_level
(
    id bigint NOT NULL,
    libelle character varying(50) COLLATE pg_catalog."default",
    CONSTRAINT trust_level_pkey PRIMARY KEY (id)
);

CREATE TABLE public.sitemap
(
    url character varying(255) COLLATE pg_catalog."default" NOT NULL,
    lastmod character varying(50) COLLATE pg_catalog."default",
    headers_url character varying[] COLLATE pg_catalog."default",
    id_trust bigint,
    CONSTRAINT sitemap_pkey PRIMARY KEY (url),
    CONSTRAINT fk_trust_level FOREIGN KEY (id_trust)
        REFERENCES public.trust_level (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

INSERT INTO trust_level values (1, 'Unverified');
INSERT INTO trust_level values (2, 'Malicious');
INSERT INTO trust_level values (3, 'Oriented');
INSERT INTO trust_level values (4, 'Verified');

INSERT INTO sitemap VALUES ('https://www.theguardian.com/sitemaps/news.xml', NULL, ARRAY['loc', 'lastmod', 'news:title', 'news:publication_date','news:keywords'], 4);
INSERT INTO sitemap VALUES ('https://www.washingtonpost.com/news-sitemaps/index.xml', NULL, ARRAY['loc', 'lastmod', 'news:title', 'news:publication_date','news:keywords'], 4);
INSERT INTO sitemap VALUES ('https://www.nytimes.com/sitemaps/new/news.xml.gz', NULL, ARRAY['loc', 'lastmod', 'news:title', 'news:publication_date','news:keywords'], 4);
INSERT INTO sitemap VALUES ('https://www.foxnews.com/sitemap.xml?type=news', NULL, ARRAY['loc', 'lastmod', 'news:title', 'news:publication_date','news:keywords'], 3);
INSERT INTO sitemap VALUES ('https://sputniknews.com/sitemap.xml', NULL, ARRAY['loc', 'lastmod', 'news:title', 'news:publication_date','news:keywords'], 3);
INSERT INTO sitemap VALUES ('https://time.com/news-sitemap.xml', NULL, ARRAY['loc', 'lastmod', 'news:title', 'news:publication_date','news:keywords'], 4);
INSERT INTO sitemap VALUES ('https://www.theonion.com/sitemap_news.xml', NULL, ARRAY['loc', 'lastmod', 'news:title', 'news:publication_date','news:keywords'], 5);
