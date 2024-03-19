from pathlib import Path
import os
import time
import argparse
from sync import Synchronizer
import logging
import sys
""" Naive Solution """


def configure_parser() -> argparse.ArgumentParser:
    """ Configure the parser """
    parser = argparse.ArgumentParser(description="Veeam Folder Synchronizer")
    parser.add_argument("-s", "--source", help="Source folder to perform backup.", required=True, type=str)
    parser.add_argument("-b", "--backup", help="Backup folder path.",required=True, type=str)
    parser.add_argument("-l", "--log", help="Log file path.", required=True, type=str)
    parser.add_argument("-i", "--interval", help="Interval in seconds. Default is 60s.", required=False, default=60, type=int)
    return parser
def configure_logger(log_path: str, log_name) -> logging.Logger:
    """ Configure the logger """
    logger = logging.getLogger(log_name)
    logging.basicConfig(filename=log_path, encoding='utf-8', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(logging.Formatter("\n%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(stdout_handler)
    return logger

def main() -> None:
    """ Main function """
    parser = configure_parser()
    args = parser.parse_args()
    source = Path(args.source)
    backup = Path(args.backup)
    log = Path(args.log)
    logger = configure_logger(log_path=log, log_name="Sync")

    if not source.exists():
        print("\nSource folder does not exist")
        return
    if not backup.exists():
        print("\nBackup folder does not exist")
        return
    if not log.exists() or not log.is_file():
        print("\nLog file path is invalid")
        return

    print(f"Source: {source}\nbackup: {backup}\nInterval: {args.interval}\nLog: {log}")

    while True:
        sync = Synchronizer(source, backup, logger)
        sync.synchronize()
        time.sleep(args.interval)

if __name__ == "__main__":
    main()

