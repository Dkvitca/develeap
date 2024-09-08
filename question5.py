#transaction time average#


from datetime import datetime

def calculate_average_transaction_time(path):
    active_transactions = {}
    total_time = 0
    transaction_count = 0

    try:
        with open(path, 'r') as log_file:
            for line in log_file:
                if "transaction" in line:
                    parts = line.split()
                    timestamp = datetime.strptime(f"{parts[0]} {parts[1]}", "%d-%m-%Y %H:%M:%S.%f")
                    if "begun" in line:
                        transaction_id = parts[-2]
                        active_transactions[transaction_id] = timestamp
                    elif "done" in line:
                        transaction_id = line.split("=")[-1].strip()
                        if transaction_id in active_transactions:
                            start_time = active_transactions[transaction_id]
                            duration = (timestamp - start_time).total_seconds() * 1000
                            total_time += duration
                            transaction_count += 1
                            del active_transactions[transaction_id]
        
        if transaction_count > 0:
            average_time = total_time / transaction_count
            return average_time
        else:
            return 0
    except Exception as err:
        print(f"Error: {err}")
        return 0

path = 'exam.log'
average_time = calculate_average_transaction_time(path)
print(f"Average transaction time: {average_time} ms")