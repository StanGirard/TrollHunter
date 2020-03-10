create table if not exists NEWS_PROVIDERS (
    id INTEGER PRIMARY KEY NOT NULL,
    url_provider TEXT NOT NULL,
    site_map_path TEXT NOT NULL
);

create table if not exists PROVIDERS_CONTENT (
    provider_id INTEGER NOT NULL,
    date_timestamp INTEGER NOT NULL,
    titre TEXT NOT NULL,
    url TEXT PRIMARY KEY NOT NULL,
    keywords TEXT NOT NULL,
    FOREIGN KEY(provider_id) REFERENCES NEWS_PROVIDERS(id)
);