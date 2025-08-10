import mysql.connector
from tabulate import tabulate
import logging

class MySQLHandler:
    def __init__(self, config):
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()

    def create_tables(self, sql_file='sql/create_tables.sql'):
        with open(sql_file, 'r') as f:
            commands = f.read().split(';')
            for command in commands:
                if command.strip():
                    self.cursor.execute(command)
        self.conn.commit()

    def insert_user_agent(self, user_agent):
        if not user_agent:
            return None

        self.cursor.execute(
            "SELECT id FROM user_agents WHERE user_agent_string = %s", (user_agent,))
        result = self.cursor.fetchone()
        if result:
            return result[0]

        os, browser, device_type = "Unknown", "Unknown", "Desktop"
        if "Windows" in user_agent: os = "Windows"
        elif "Mac" in user_agent: os = "macOS"
        elif "Linux" in user_agent: os = "Linux"
        if "Chrome" in user_agent: browser = "Chrome"
        elif "Firefox" in user_agent: browser = "Firefox"
        elif "Safari" in user_agent: browser = "Safari"
        if "Mobile" in user_agent: device_type = "Mobile"

        self.cursor.execute(
            "INSERT INTO user_agents (user_agent_string, os, browser, device_type) VALUES (%s, %s, %s, %s)",
            (user_agent, os, browser, device_type)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_batch_log_entries(self, log_data_list):
        values = []
        for log in log_data_list:
            user_agent_id = self.insert_user_agent(log['user_agent'])
            values.append((
                log['ip_address'], log['timestamp'], log['method'], log['path'],
                log['status_code'], log['bytes_sent'], log['referrer'], user_agent_id
            ))

        self.cursor.executemany(
            "INSERT INTO log_entries (ip_address, timestamp, method, path, status_code, bytes_sent, referrer, user_agent_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            values
        )
        self.conn.commit()

    def get_top_n_ips(self, n):
        self.cursor.execute(
            "SELECT ip_address, COUNT(*) AS count FROM log_entries GROUP BY ip_address ORDER BY count DESC LIMIT %s", (n,))
        return self.cursor.fetchall()

    def get_status_code_distribution(self):
        self.cursor.execute("""
            SELECT status_code, COUNT(*) AS count,
            (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM log_entries)) AS percentage
            FROM log_entries GROUP BY status_code ORDER BY count DESC
        """)
        return self.cursor.fetchall()

    def get_hourly_traffic(self):
        self.cursor.execute("""
            SELECT DATE_FORMAT(timestamp, '%H:00') AS hour_of_day, COUNT(*) AS request_count
            FROM log_entries
            GROUP BY hour_of_day
            ORDER BY hour_of_day ASC
        """)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

