import subprocess
import sys

def fetch_logs_via_scp(date, remote_host, remote_user, port):
    """
    Pobiera logi z serwera za pomocą SCP.
    """
    try:
        log_patterns = [
            f"snap_SSMSB1_{date}_*.log",
            f"snap_SSMSB2_{date}_*.log",
            f"snap_SSMS3_{date}_*.log"
        ]
        
        for log_pattern in log_patterns:
            remote_path = f"{remote_user}@{remote_host}:/root/snap/{date[:6]}_*/{log_pattern}"

            scp_command = [
                "scp", "-P", str(port),
                "-o", "HostKeyAlgorithms=+ssh-rsa", 
                "-o", "MACs=hmac-md5", 
                f"{remote_user}@{remote_host}:/root/snap/{date[:6]}_*/{log_pattern}",
                "./"
            ]

            print(f"Pobieranie logu: {remote_path}")
            subprocess.run(scp_command, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas pobierania pliku: {e}")
        sys.exit(1)