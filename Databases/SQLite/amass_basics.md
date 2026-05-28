Imagine that we utilize the output of the OSINT tool `amass` that creates `.sqlite` files. Run:

```
$ sqlite3 amass.sqlite

Output:
SQLite version 3.46.1 2024-08-13 09:16:08
Enter ".help" for usage hints.
```


```
sqlite> .tables

Output:
assets    gorp_migrations    relations  
```
```
sqlite> .schema assets

Output:
CREATE TABLE assets(
    id INTEGER PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    type TEXT,
    content TEXT, last_seen DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE INDEX idx_fqdn_content_name ON assets (content->>'name' COLLATE NOCASE) WHERE type = 'FQDN';
CREATE INDEX idx_assets_type ON assets (type);
CREATE INDEX idx_as_created_at ON assets (created_at);
CREATE INDEX idx_as_last_seen ON assets (last_seen);
```

```
sqlite> SELECT type, content FROM assets WHERE type='FQDN' LIMIT 10;

Output:
FQDN|{"name":"example1.com"}
FQDN|{"name":"example2.net"}
FQDN|{"name":"example3.net"}
FQDN|{"name":"example4.net"}
FQDN|{"name":"example5.com"}
FQDN|{"name":"com-example6.net"}
FQDN|{"name":"www.example7.net"}
FQDN|{"name":"example8.net"}
FQDN|{"name":"example9.net"}
```

```
sqlite> SELECT json_extract(content, '$.name') AS subdomain FROM assets WHERE type='FQDN' LIMIT 10;

Output:
example1.com
example2.net
example3.net
example4.net
example5.com
com-example6.net
www.example7.net
example8.net
example9.net
```
