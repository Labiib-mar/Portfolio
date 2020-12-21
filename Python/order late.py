import csv
from datetime import datetime

path = 'delivery_orders_march.csv'
file = open(path, newline='')
reader = csv.reader(file)

header = next(reader)
print(header)
data = []
for row in reader:
    # row [orderId, shopId, userId, EventTime]
    orderId = int(row[0])
    pick = int(row[1])
    attempt1 = float(row[2])
    attempt2 = float(row[3])
    buyer_loc = row[4]
    seller_loc = row[5]

    data.append([orderId, pick, attempt1, attempt2, buyer_loc, seller_loc])

print(data[1])
##result_path = 'brush_orders.csv'
##file = open(result_path, 'w')
##writer =csv.writer(file)
##writer.writerow(['shopid','userid'])
##file.close()
##
##unique_shop = []
##unique_order = []
##
##for i in range(len(data)-1):
##    current_row = data[i]
##    row_shopId = current_row[1]
##    row_userId = current_row[2]
##    row_orderId = current_row[0]
##    row_eventTime = current_row[3]
##    next_row = data[i+1]
##    if row_shop
##print(unique_shop)
##
####test_path = 'test.csv'
####file = open(test_path,'w')
####writer.writerows(unique_shop)
####writer.writerows(unique_order)
####file.close()



            
