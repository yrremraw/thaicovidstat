import requests
import json
from datetime import datetime, timedelta, date
from pandas import DataFrame
import matplotlib.pyplot as plotG
import numpy as np
from textwrap import wrap

requests.packages.urllib3.disable_warnings()    # due to API have no cert so we won"t verify SSL certificate and this is to disable warning msg
requests.adapters.DEFAULT_RETRIES = 3

APIs = {
    "covid_today": "https://covid19.ddc.moph.go.th/api/open/today"
    , "covid_sum": "https://covid19.ddc.moph.go.th/api/open/cases/sum"
}

def api_caller(endpoint):
    resp_json = ""
    response = requests.get(APIs[endpoint], verify=False)
    calling_time = str(datetime.now())
    resp_status_code = str(response.status_code)
    print("Calling: " + endpoint + " at time: "+ calling_time + ", Got response code: "+ resp_status_code)
    if (resp_status_code == "200"):
        resp_json = json.loads(response.content)
        return(resp_json)
    else:
        print("Please retry as a response code is not 200, it is: "+ resp_status_code + " at " + calling_time)

def gen_today_data(data_type):
    compare = "+" if today_resp_json["New" + data_type] >= 0 else "-"
    result = "Total " + data_type + " case: " + str(today_resp_json[data_type]) + " (" + compare + str(today_resp_json["New" + data_type]) + ")"
    return result

### get today data ###
"""
today_resp_json = api_caller("covid_today")

today_data = ["Confirmed", "Recovered", "Hospitalized", "Deaths"]
for d in today_data:
    print(gen_today_data(d))
print("Updated date: " + str(today_resp_json["UpdateDate"]))
"""

### get sum data ### # Province, Nation, Gender
def gen_covid_cases(sum_by, case_index, case_value, plot_title, top):
    sum_resp_json[sum_by].sort(key = lambda x:x["Count"], reverse=True) # sort DESC
    col = []
    val = []
    for each_gender in sum_resp_json[sum_by][:top]:
        if each_gender[case_index] == "หญิง":
            each_gender[case_index] = "Women"
        elif each_gender[case_index] == "ชาย":
            each_gender[case_index] = "Men"
        elif each_gender[case_index] == "ไทย":
            each_gender[case_index] = "Thailand"
        col.append(each_gender[case_index])
        val.append(each_gender[case_value])
    plot_covid_case(col, val, plot_title)

def plot_covid_case(case_index, case_value, plot_title):
    case_index = [ '\n'.join(wrap(l, 7)) for l in case_index]
    plotG.bar(case_index, case_value)
    """for index, value in enumerate(case_value):
        plotG.text(value, index,
                str(value))"""
    for i in range(len(case_index)):
        plotG.text(i,case_value[i],case_value[i], ha = 'center')
    plotG.title(plot_title)
    plotG.show()

sum_resp_json = api_caller("covid_sum")
print(sum_resp_json["Gender"])
#gen_covid_cases("Gender", "Gender", "Count", "Today's COVID cases by gender",3)
#gen_covid_cases("Nation", "Nation", "Count", "Today's COVID cases by Nation",10)
#gen_covid_cases("Province", "ProvinceEn", "Count", "Today's COVID cases by Thailand province",20)



"""
dataf_sum_gender = DataFrame(sum_gender,columns=['Women','Men','Unknown'])
print(dataf_sum_gender)
plotG.plot(dataf_sum_gender)
plotG.show()

bar(x, height[, width, bottom, align, data])
"""

""" # TREND
Data = {'April': [111,531,58,421,256,90,147,500,40,150], 'May': [150,40,500,147,90,256,421,58,531,111] }
dataF = DataFrame(Data,columns=['April','May'])
plotG.plot(dataF)
plotG.show()
"""



"""print("## response: " + str(response))
print("## response content: " + str(response.content))
print("## response json: " + str(today_resp_json))
#print(response.content[Confirmed])
print(today_resp_json["Confirmed"])
for key, value in today_resp_json.items():
    print(str(key) + ": " + str(value))"""
