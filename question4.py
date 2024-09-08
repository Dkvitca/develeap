# find fastest transaction and its id#

from datetime import datetime

def find_fastest_transaction(path):
    active_transactions = set()
    fastest_time = float('inf')
    fastest_id = None

    try:
        with open(path, 'r') as log_file:
            for line in log_file:
                if "transaction" in line:
                    parts = line.split()
                    timestamp = datetime.strptime(f"{parts[0]} {parts[1]}", "%d-%m-%Y %H:%M:%S.%f")
                    if "begun" in line:
                        transaction_id = parts[-2]
                        active_transactions.add((transaction_id, timestamp))
                    elif "done" in line:
                        transaction_id = line.split("=")[-1].strip()
                        for start_id, start_time in active_transactions:
                            if start_id == transaction_id:
                                duration = (timestamp - start_time).total_seconds() * 1000
                                if duration < fastest_time:
                                    fastest_time = duration
                                    fastest_id = transaction_id
                                active_transactions.remove((start_id, start_time))
                                break
        return fastest_id, fastest_time
    except Exception as err:
        print(f"Error: {err}")
        return None, None

path = 'exam.log'
fastest_id, fastest_time = find_fastest_transaction(path)
print("fastest transaction:", fastest_id, "time:", fastest_time)