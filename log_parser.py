import re
from datetime import datetime
import logging

class LogParser:
    LOG_PATTERN = re.compile(
        r'(\d{1,3}(?:\.\d{1,3}){3}) - - \[(.*?)\] "(.*?)" (\d{3}) (\S+) "(.*?)" "(.*?)"'
    )

    def parse_line(self, log_line):
        match = self.LOG_PATTERN.match(log_line)
        if match:
            ip_address = match.group(1)
            timestamp = datetime.strptime(match.group(2), '%d/%b/%Y:%H:%M:%S %z')
            request = match.group(3).split()
            method = request[0] if len(request) > 0 else None
            path = request[1] if len(request) > 1 else None
            status_code = int(match.group(4))
            bytes_sent = int(match.group(5)) if match.group(5).isdigit() else 0
            referrer = None if match.group(6) == '-' else match.group(6)
            user_agent = None if match.group(7) == '-' else match.group(7)

            return {
                'ip_address': ip_address,
                'timestamp': timestamp,
                'method': method,
                'path': path,
                'status_code': status_code,
                'bytes_sent': bytes_sent,
                'referrer': referrer,
                'user_agent': user_agent
            }
        else:
            logging.warning(f"Malformed log line skipped: {log_line.strip()}")
            return None
