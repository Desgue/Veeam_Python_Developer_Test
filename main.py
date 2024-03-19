from pathlib import Path
import os
import time
import argparse

from sync import Synchronizer
""" Naive Solution """


def configure_parser() -> argparse.ArgumentParser:
    """ Configure the parser """
    parser = argparse.ArgumentParser(description="Veeam Folder Synchronizer")
    parser.add_argument("-s", "--source", help="Source folder to perform backup.", required=True, type=str)
    parser.add_argument("-b", "--backup", help="Backup folder path.",required=True, type=str)
    parser.add_argument("-l", "--log", help="Log file path.", required=True, type=str)
    parser.add_argument("-i", "--interval", help="Interval in seconds. Default is 60s.", required=False, default=60, type=int)
    return parser

def main() -> None:
    """ Main function """
    parser = configure_parser()
    args = parser.parse_args()
    source = Path(args.source)
    backup = Path(args.backup)
    log = Path(args.log)

    if not source.exists():
        print("source folder does not exist")
        return
    if not backup.exists():
        print("Backup folder does not exist")
        return
    if not log.exists():
        print("Log file does not exist")
        return

    print(f"Source: {source}\nbackup: {backup}\nInterval: {args.interval}\nLog: {log}")

    while True:

        sync = Synchronizer(source, backup)
        sync.synchronize()

        time.sleep(args.interval)

if __name__ == "__main__":
    main()

