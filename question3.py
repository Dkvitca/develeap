#find number of completed transactions#

def count_completed_transactions(path):
    transaction_count = 0
    active_transactions = set()

    try:
        with open(path, 'r') as log_file:
            for line in log_file:
                if "transaction" in line:
                    if "begun" in line:
                        transaction_id = line.split()[-2]
                        active_transactions.add(transaction_id)
                    elif "done" in line:
                        transaction_id = line.split("=")[-1].strip()
                        if transaction_id in active_transactions:
                            transaction_count += 1
                            active_transactions.remove(transaction_id)
        return transaction_count
    except Exception as err:
        print(f"Error: {err}")
        return 0

path = 'exam.log'
print(f"Number of completed transactions: {count_completed_transactions(path)}")