import pandas as pd

from job import get_all_staff 

def list_to_dict(array, key):
    res = {}
    for a in array:
        res[a[key]] = a
    return res

excel = pd.read_excel("issues_202205051131.xlsx")
staffs = get_all_staff()
staff_dict = list_to_dict(staffs,"id")
excel["staff_email"] =""
excel["Name"] =""
excel["Người tạo"] = ""

for i, row in excel.iterrows():
    unique_id = i
    exchange = row['staff_id']
    # print(int(exchange))
    # print(staff_dict.get(int(exchange)))
    if staff_dict.get(int(exchange)):
        excel.loc[excel.staff_id==exchange, "staff_email"] = staff_dict[int(exchange)]["email"]
        excel.loc[excel.staff_id==exchange, "Name"] =staff_dict[int(exchange)]["full_name"]

    created = row["created"]
    if staff_dict.get(int(created)):
        excel.loc[excel.staff_id==created, "Người tạo"] =staff_dict[int(created)]["full_name"]
        excel.loc[excel.staff_id==created, "Email tạo"] =staff_dict[int(created)]["email"]

excel.loc[excel.processing==0, "processing"] = "Mở"
excel.loc[excel.processing==1, "processing"] = "Đóng"
excel.loc[excel.review==1, "review"] = "Hoàn thành"
excel.loc[excel.review==0, "review"] = "Nghiệm tu"
excel.loc[excel.review==-1, "review"] = "Chưa hoàn thành"



excel.to_excel("output.xlsx")
for staff_id in excel["staff_id"]:
    print(staff_id)
# Trạng thái nghiệm thu, 0 nghiệm thu, 1 hoàn thành, -1 là ko hoàn thành
# , 1 đóng, 0 là mở