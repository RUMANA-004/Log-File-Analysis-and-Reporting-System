#  Log File Analysis & Reporting System

A Python-powered tool to **parse, store, and analyze Apache web server logs** with automated reporting capabilities.  
This system extracts meaningful insights from raw log data, helping in **security analysis, troubleshooting, and performance monitoring**.

---

##  Features

### Intelligent Log Parsing
- Supports **Apache Common & Combined Log Formats**.
- Regex-based extraction of:
  - IP addresses
  - Timestamps
  - HTTP methods, URLs, and protocols
  - Status codes
  - Bytes sent
  - Referrer URLs & user agents
- Cleans and normalizes extracted data for accurate storage.

###  MySQL-Powered Storage
- Optimized relational schema for efficient queries.
- Separate **user-agent table** to avoid redundancy.
- **Batch inserts** for high-volume log processing.
- **Uniqueness constraints** to prevent duplicate entries.

###  Reporting & Insights
- **Top N IP addresses** (most active or suspicious).
- **Most requested URLs**.
- **Status code distribution** (error vs. success).
- **Hourly traffic trends**.
- **Error occurrence patterns**.
- **User-Agent analytics** (OS & browser breakdowns).

###  Performance & Reliability
- Memory-efficient processing for large log files.
- Configurable **batch size** for speed optimization.
- Comprehensive error handling for malformed lines.
- Modular code structure for easy feature extension.

---

##  System Architecture

```plaintext
Log Source (Apache/Nginx) → Log Parser (Regex) → MySQL Database → Reporting Engine (CLI/Streamlit)


