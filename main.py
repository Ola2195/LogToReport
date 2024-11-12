import argparse
import os
import glob
from scripts.data_fetcher import fetch_data
from scripts.document_writer import generate_document
from scripts.fetch_files import fetch_logs_via_scp
from datetime import date

def generate_report(report_date):
    """
    Generuje raport na podstawie pobranych danych.
    """
    data = fetch_data(report_date.strftime('%y%m%d'))
    generate_document(report_date.year, report_date.month, report_date.day, data)

def remove_downloaded_logs(date):
    """
    Usuwa pobrane pliki logów po zakończeniu operacji.
    """
    log_patterns = [
        f"snap_SSMSB1_{date}_*.log",
        f"snap_SSMSB2_{date}_*.log",
        f"snap_SSMS3_{date}_*.log"
    ]
    
    log_files = []
    for pattern in log_patterns:
        log_files.extend(glob.glob(os.path.join(os.getcwd(), pattern)))
    
    if not log_files:
        return
    
    for log_file in log_files:
        try:
            os.remove(log_file)
        except OSError as e:
            print(f"Błąd przy usuwaniu pliku {log_file}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generowanie dokumentu raportu.')
    parser.add_argument('year', type=int, help='Rok raportu')
    parser.add_argument('month', type=int, help='Miesiac raportu')
    parser.add_argument('day', type=int, help='Dzien raportu')
    parser.add_argument('--no-remove', action='store_true', help='Nie usuwaj pobranych plików logów')


    args = parser.parse_args()
    remote_host = "localhost"
    remote_user = "root"
    ssh_port = 2222
    report_date = date(args.year, args.month, args.day)
    fetch_logs_via_scp(report_date.strftime('%y%m%d'), remote_host, remote_user, ssh_port)
    generate_report(report_date)

    if not args.no_remove:
        remove_downloaded_logs(report_date.strftime('%y%m%d'))
