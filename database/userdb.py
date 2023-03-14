import pandas as pd
from direct_redis import DirectRedis

emp_list = ['204469', '204468', '204478']

r = DirectRedis(host='localhost', port=8080)

col = ['EMp_id', 'password', 'sessionid', 'startime', 'endtime', 'start_loc', 'end_loc','Empname','dept',
       'phone', 'mail_id']
fdb = pd.DataFrame(columns=col)
fdb.set_index('EMp_id', inplace=True)



class UserData():

    def __int__(self):
        pass

    @classmethod
    def login_access(self, user,passw):
        x = r.get("fleet")
        y = x.query(f"EMp_id=='{user}' & password=='{passw}'")
        if y.empty:
            return False
        else:
            data = {
                "EMp_id": y.iloc[0]['EMp_id'],
                "password": y.iloc[0]['password']
            }
            return data
    @classmethod
    def register(self,data):
        x = r.get("fleet")
        df = pd.DataFrame(data, index=[data.get('EMp_id')])
        y = pd.concat([x, df], axis=0)
        r.set("fleet", y)
        return r.get("fleet")
    @classmethod
    def auth(self,data):
        df = r.get("fleet")
        emp_id = [j for j in emp_list if data.get('EMp_id')]
        reg = df[df.index.isin(emp_list)]
        if emp_id != [] and len(reg.index) == 0:
            return True
        else:
            return False
    @classmethod
    def fleet_details(self,data):
        pass



# x = r.get("fleet")
# print(x)
# data = {
#     "Empname": "vinoth",
#     "mail_id": "xxx@gmail.com",
#     "EMp_id": "204469",
#     "dept": "operation",
#     "phone": "7209643537",
#     "password": "zxcvbn",
# }
#
#
# x = UserData.auth(data)
# print(x)
