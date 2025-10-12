# The most basic server types

| No | Server Type | Data Flow | Protocols |
|:----:|:----|:----|:----|
| 1 | Web Server | A client (e.g., web browser) sends an HTTP request (e.g., GET /index.html) to the web server, which processes the request and sends back an HTTP response (e.g., HTML page, image, JSON). Optionally, a proxy or load balancer may sit between the two. | HTTP, HTTP/2, HTTP/3 (QUIC), HTTPS, WebSocket (ws/wss) |
| 2 | Mail Server | User A wants to send an email to user B through the Internet. One or more mail servers stand between the two sides, processing and forwarding these messages. More precisely, a Mail User Agent (MUA) such as Outlook or Thunderbird connects to a Mail Transfer Agent (MTA) to send or receive emails. Emails are sent between MTAs across the Internet and delivered to the recipient’s mailbox. | SMTP (Send), POP3, IMAP (Receive), SMTPS, IMAPS, POP3S |
| 3 | DNS Server | A client (called a DNS resolver) queries a DNS server to translate a domain name (e.g., www.example.com) into an IP address. Recursive resolvers may contact root, TLD, and authoritative DNS servers in sequence. | DNS (UDP/TCP 53), DNS over TLS (DoT, TCP 853), DNS over HTTPS (DoH, HTTPS 443) |
| 4 | Proxy Server | A client connects to the proxy, which forwards requests to external servers on behalf of the client. The proxy may cache, filter, or log traffic. It is typically used for performance, anonymity, or content control. | HTTP, HTTPS, SOCKS5, FTP (proxying) |
| 5 | File Server | A client connects to a centralized server to store, retrieve, or manage files across the network. Often used in LANs or enterprise environments. | FTP/S, SFTP (SSH File Transfer), NFS, SMB/CIFS |
| 6 | Origin Server | The primary content source in a CDN or caching architecture. When a CDN edge server or proxy doesn’t have cached content, it forwards the request to the origin server, which holds the authoritative version of the website or data. | HTTP, HTTP/2, HTTP/3 (QUIC), HTTPS |
