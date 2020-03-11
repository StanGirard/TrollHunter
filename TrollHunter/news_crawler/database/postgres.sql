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