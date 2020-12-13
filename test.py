from datetime import datetime
ts = int("1608519600000")/1000


print(datetime.utcfromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S'))