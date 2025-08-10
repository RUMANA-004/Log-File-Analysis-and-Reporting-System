import argparse
import configparser
import logging
from log_parser import LogParser
from mysql_handler import MySQLHandler
from tabulate import tabulate

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    parser = argparse.ArgumentParser(description="Log Analyzer CLI")
    subparsers = parser.add_subparsers(dest="command")

    process_parser = subparsers.add_parser("process_logs")
    process_parser.add_argument("file_path", type=str)
    process_parser.add_argument("--batch_size", type=int, default=500)

    report_parser = subparsers.add_parser("generate_report")
    report_subparsers = report_parser.add_subparsers(dest="report_type")

    top_ips_parser = report_subparsers.add_parser("top_n_ips")
    top_ips_parser.add_argument("n", type=int)

    report_subparsers.add_parser("status_code_distribution")
    report_subparsers.add_parser("hourly_traffic")

    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read("config.ini")
    db_config = dict(config["mysql"])

    db_handler = MySQLHandler(db_config)
    db_handler.create_tables()

    if args.command == "process_logs":
        parser_obj = LogParser()
        batch = []
        inserted, skipped = 0, 0
        skipped_lines = []

        with open(args.file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                parsed = parser_obj.parse_line(line)
                if parsed:
                    batch.append(parsed)
                    inserted += 1
                    if len(batch) >= args.batch_size:
                        db_handler.insert_batch_log_entries(batch)
                        batch = []
                else:
                    skipped += 1
                    if len(skipped_lines) < 5:
                        skipped_lines.append(line.strip())

        if batch:
            db_handler.insert_batch_log_entries(batch)

        logging.info(f" Inserted: {inserted} lines |  Skipped: {skipped} lines")

        if skipped_lines:
            logging.warning("Sample skipped lines:")
            for l in skipped_lines:
                logging.warning(l)

    elif args.command == "generate_report":
        if args.report_type == "top_n_ips":
            results = db_handler.get_top_n_ips(args.n)
            print(tabulate(results, headers=["IP Address", "Request Count"], tablefmt="grid"))
        elif args.report_type == "status_code_distribution":
            results = db_handler.get_status_code_distribution()
            print(tabulate(results, headers=["Status Code", "Count", "Percentage"], tablefmt="grid"))
        elif args.report_type == "hourly_traffic":
            results = db_handler.get_hourly_traffic()
            print(tabulate(results, headers=["Hour", "Request Count"], tablefmt="grid"))

    db_handler.close()

if __name__ == "__main__":
    main()
