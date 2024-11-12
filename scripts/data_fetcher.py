import re
import math
import glob
import sys

def parse_file(file_path):
    """
    Przetwarza plik loga i wyciaga dane systemowe.
    Zwraca slownik z danymi dotyczacymi restartu, CPU, RAM i dyskow.
    """

    with open(file_path, 'r') as file:
        content = file.readlines()
    
    data = {
        "restart_date": "",
        "cpu_usage": "",
        "ram_total_mb": "",
        "ram_usage_percent": "",
        "ram_usage_mb": "",
        "disk": []
    }
    
    for line in content:
        line = line.strip()
        
        # Sekcja restart time - wyciaga date i godzine resetu systemu w formacie YYYY.MM.DD HH:MM
        if "BootTime" in line:
            match = re.search(r"BootTime:([A-Za-z]{3}) (\d{1,2}) (\d{2}:\d{2}):\d{2} CET (\d{4})", line)
            if match:
                month_str = match.group(1)
                day = match.group(2)
                time = match.group(3)
                year = match.group(4)
                
                month_map = {
                    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
                }
                month = month_map.get(month_str)
                
                if month:
                    formatted_datetime = f"{year}.{month}.{int(day):02d} {time}"
                    data["restart_date"] = formatted_datetime

        # Sekcja CPU - wyciaga uzycie CPU jako liczba calkowita w procentach
        if line.startswith("Total"):
            match = re.search(r"Total\s+\|\s+100%\s+\|\s+([\d\.]+)%", line)
            if match:
                data["cpu_usage"] = math.ceil(float(match.group(1)))

        # Sekcja RAM - wyciaga calkowita pamiec RAM oraz uzycie RAM w MB i procentach
        if line.startswith("System RAM:"):
            match = re.search(r"System RAM:.* (\d+)M \(\s*(\d+)\)", line)
            if match:
                data["ram_total_mb"] = int(match.group(1))

        if line.startswith("Total Used:"):
            match = re.search(r"Total Used:.* (\d+)M \(\s*(\d+)\)", line)
            if match:
                data["ram_usage_mb"] = int(match.group(1))
                data["ram_usage_percent"] = round(data["ram_usage_mb"]/data["ram_total_mb"]*100)       

        # Alternatywna sekcja RAM dla bezpośredniego uzycia procentowego
        if "Zajetosc pamieci" in line:
            match = re.search(r"Zajetosc pamieci\s*=\s*([\d\.]+)\s*procent", line)
            if match:
                data["ram_usage_percent"] = round(float(match.group(1)))

        # Sekcja dyskow - wyciaga szczegoly kazdego urzadzenia dyskowego
        if line.startswith("/dev/"):
            match = re.match(r"(/dev/\S+)\s+(\d+G)\s+(\d+G)\s+(\d+G)\s+(\d+)%\s+(\S+)", line)
            if match:
                data["disk"].append({
                    "filesystem": match.group(1),
                    "size": match.group(2),
                    "used": match.group(3),
                    "available": match.group(4),
                    "capacity": match.group(5)+"%",
                    "mounted_on": match.group(6)
                })
    
    return data

def fetch_data(date):
    """
    Wywoluje funkcje parse_file dla trzech plikow, zwraca przetworzone dane w zorganizowanej strukturze.
    """
    ssms1_log_pattern = f"snap_SSMSB1_{date}_*.log"
    ssms2_log_pattern = f"snap_SSMSB2_{date}_*.log"
    ssms3_log_pattern = f"snap_SSMS3_{date}_*.log"

    ssms1_log_files = glob.glob(ssms1_log_pattern)
    if not ssms1_log_files:
        print(f"No log files found for pattern: {ssms1_log_pattern}")
        sys.exit()

    ssms2_log_files = glob.glob(ssms2_log_pattern)
    if not ssms2_log_files:
        print(f"No log files found for pattern: {ssms2_log_pattern}")
        sys.exit()

    ssms3_log_files = glob.glob(ssms3_log_pattern)
    if not ssms3_log_files:
        print(f"No log files found for pattern: {ssms3_log_pattern}")
        sys.exit()

    ssms1 = parse_file(ssms1_log_files[0])
    ssms2 = parse_file(ssms2_log_files[0])
    ssms3 = parse_file(ssms3_log_files[0])

    data = {
        "restart_ssms1_date": ssms1['restart_date'],
        "restart_ssms2_date": ssms2['restart_date'],
        "restart_ssms3_date": ssms3['restart_date'],
        "computers": {
            "SSMS1": {
                "cpu_usage": f"< {ssms1['cpu_usage']}%",
                "ram_usage_percent": f"{ssms1['ram_usage_percent']}%",
                "ram_usage_mb": f"{ssms1['ram_usage_mb']}MB",
                "disk": ssms1['disk']
            },
            "SSMS2": {
                "cpu_usage": f"< {ssms2['cpu_usage']}%",
                "ram_usage_percent": f"{ssms2['ram_usage_percent']}%",
                "ram_usage_mb": f"{ssms2['ram_usage_mb']}MB",
                "disk": ssms2['disk']
            },
            "SSMS3": {
                "cpu_usage": f"< {ssms3['cpu_usage']}%",
                "ram_usage_percent": f"{ssms3['ram_usage_percent']}%",
                "ram_usage_mb": f"{ssms3['ram_usage_mb']}MB",
                "disk": ssms3['disk']
            }
        }
    }
    return data