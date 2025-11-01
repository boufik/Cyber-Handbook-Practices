# Log Types

Logs are records of system, network and application activities. They help us track, monitor and analyze system health, performance and security events.

---

## 1. System and Access Logs
| No | Log Type | Description |
|:--:|:--|:--|
| 1 | **System Logs** | Contain information about **operating system** operations, errors and warnings. |
| 2 | **Access Logs** | Record **successful or failed attempts** to access systems, files or applications. |
| 3 | **Event Logs (Windows/Linux)** | Track system **events like startup, shutdown**, crashes or software installations. |
| 4 | **Authentication Logs** | Capture user **login attempts** and authentication results. |

---

## 2. Network and Communication Logs
| No | Log Type | Description |
|:--:|:--|:--|
| 1 | **Network Traffic Logs** | Monitor incoming and outgoing network packets for analysis and troubleshooting. |
| 2 | **DNS Logs** | Record domain name resolution requests and responses. Useful for detecting suspicious lookups. |
| 3 | **Email Logs** | Track mail flow, delivery issues, and spam or phishing attempts. |
| 4 | **Proxy & Web Logs** | Log web traffic activity, URLs accessed, and user browsing behavior. |
| 5 | **Web Application Firewall (WAF) Logs** | Capture and block malicious HTTP requests targeting web applications. |

---

## 3. Security and Compliance Logs
| No | Log Type | Description |
|:--:|:--|:--|
| 1 | **Security Logs** | Record security-related events like intrusion attempts, malware detections, and policy violations. |
| 2 | **Physical Access Logs** | Log entries from physical security systems such as keycards or biometrics. |
| 3 | **Certificate / PKI Logs** | Track certificate creation, renewal, and revocation to ensure trust chain integrity. |
| 4 | **IAM Logs** | Store identity and access management activities like permission changes and user provisioning. |

---

## 4. Configuration and Maintenance Logs
| No | Log Type | Description |
|:--:|:--|:--|
| 1 | **Configuration (Change) Logs** | Record system configuration changes, helping identify misconfigurations. |
| 2 | **Backup Logs** | Provide information about scheduled backups, their success, and any errors. |
| 3 | **Patch Management Logs** | Track updates and patches applied to systems and applications. |
| 4 | **Software Installation Logs** | Record details of software installations, updates, and removals. |

---

## 5. Advanced and Endpoint Logs
| No | Log Type | Description |
|:--:|:--|:--|
| 1 | **Cloud Logs** | Capture activity within cloud environments such as AWS, Azure, or GCP. |
| 2 | **Endpoint Detection Logs** | Contain endpoint activity data, such as malware detections or suspicious processes. |
| 3 | **Advanced / Specialized Log Types** | Logs tailored for specific technologies, environments, or regulatory needs. |
| 4 | **Time Synchronization Logs (NTP)** | Keep track of clock synchronization across systems for consistent timestamps. |

---

> **Tip:** Centralized log management (via tools like SIEM or ELK stack) makes it easier to correlate and analyze data across these categories.
