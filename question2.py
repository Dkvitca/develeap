#findd the number of errors in the log file

path = 'exam.log'

def count_num_of_errors(path):
    num_of_errors = 0
    try:
        with open(path, 'r') as log_file:
            for line in log_file:
                parts = line.split(maxsplit=4)
                if parts[2] == "ERROR":
                    num_of_errors += 1
        return num_of_errors
    except Exception as err:
        print(f"Error: {err}")
        return 0

print(count_num_of_errors(path))