import requests
import csv
from datetime import datetime

PROMETHEUS_URL = 'http://localhost:9090/api/v1/query'

def get_metric(query):
    response = requests.get(PROMETHEUS_URL, params={'query': query})
    results = response.json()['data']['result']
    return float(results[0]['value'][1]) if results else 0.0

cpu_query = '100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
ram_query = '(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100'

cpu_usage = get_metric(cpu_query)
ram_usage = get_metric(ram_query)
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open('cloud_performance_report.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    if file.tell() == 0:
        writer.writerow(["Timestamp", "CPU Usage (%)", "RAM Usage (%)"])
    writer.writerow([timestamp, round(cpu_usage, 2), round(ram_usage, 2)])

print(f"Report Generated! CPU: {round(cpu_usage, 2)}% | RAM: {round(ram_usage, 2)}%")
