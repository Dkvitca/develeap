
#return the first line of the log file

def return_first_line(path):
    try:
        with open(path, 'r') as log_file:
            first_line = log_file.readline()
            if (first_line):
                return first_line
            else:
                return 'Error reading first line'
    except Exception as err:
        print(f"Error: {err}")
path = 'exam.log'
#print(return_first_line(path))
