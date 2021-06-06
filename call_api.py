import requests
import json
from datetime import datetime, timedelta, date
#from pandas import DataFrame
import pandas
import matplotlib.pyplot as plotG
import numpy as np
from textwrap import wrap

requests.packages.urllib3.disable_warnings()    # due to API have no cert so we won"t verify SSL certificate and this is to disable warning msg
requests.adapters.DEFAULT_RETRIES = 3


today_date = date.today()
APIs = {
    "covid_today": "https://covid19.ddc.moph.go.th/api/open/today"
    , "covid_sum": "https://covid19.ddc.moph.go.th/api/open/cases/sum"
    , "covid_trend": "https://covid19.ddc.moph.go.th/api/open/timeline"
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

today_data = ["Confirmed", "Hospitalized", "Recovered", "Deaths"]
for d in today_data:
    print(gen_today_data(d))
print("Updated date: " + str(today_resp_json["UpdateDate"]))
"""

### get sum data ### # Province, Nation, Gender
def gen_covid_cases(sum_by, case_index, case_value, plot_title, top):
    sum_resp_json[sum_by].sort(key = lambda x:x["Count"], reverse=True) # sort DESC
    column = []
    value = []
    for each_gender in sum_resp_json[sum_by][:top]:
        if each_gender[case_index] == "หญิง":
            each_gender[case_index] = "Women"
        elif each_gender[case_index] == "ชาย":
            each_gender[case_index] = "Men"
        elif each_gender[case_index] == "ไทย":
            each_gender[case_index] = "Thailand"
        column.append(each_gender[case_index])
        value.append(each_gender[case_value])
    #plot bar graph
    if sum_by == "Gender":
        plot_gender = plotG.figure(1)
    elif sum_by == "Nation":
        plot_nation = plotG.figure(2)
    elif sum_by == "Province":
        plot_province = plotG.figure(3)
    column = [ '\n'.join(wrap(l, 7)) for l in column]       ######### plt.xticks(rotation = 45) #####
    plotG.bar(column, value)
    """for index, value in enumerate(case_value):
        plotG.text(value, index,
                str(value))"""
    for i in range(len(column)):
        plotG.text(i,value[i],value[i], ha = 'center')
    plotG.title(plot_title)

sum_resp_json = api_caller("covid_sum")
#print(sum_resp_json["Gender"])
"""
gen_covid_cases("Gender", "Gender", "Count", "Today's COVID cases by gender", 3)
gen_covid_cases("Nation", "Nation", "Count", "Today's COVID cases by Nation", 10)
gen_covid_cases("Province", "ProvinceEn", "Count", "Today's COVID cases by Thailand province", 20)

plotG.show()
"""



#######################
"""
    "Date": "01/03/2021",
    "Confirmed": 7694,
    "Hospitalized": 3278,
    "Recovered": 4352,
    "Deaths": 64
"""
### get trend data ###
"""
dataf_sum_gender = DataFrame(sum_gender,columns=['Women','Men','Unknown'])
print(dataf_sum_gender)
plotG.plot(dataf_sum_gender)
plotG.show()

bar(x, height[, width, bottom, align, data])
"""



last_90_days_since = (today_date - timedelta(days=90))
#print(last_90_days_since)

trend_resp_json = api_caller("covid_trend")
print("Update date: " + trend_resp_json["UpdateDate"])

trend_resp_json["Data"].sort(key = lambda x:datetime.strptime(x["Date"], '%m/%d/%Y').date(), reverse=True) # sort date DESC
#print(trend_resp_json["Data"])
"""Date = []
Confirmed = []
Hospitalized = []
Recovered = []
Deaths = []"""
trend_data = {
    "Date": []
    , "Confirmed": []
    , "Hospitalized": []
    , "Recovered": []
    , "Deaths": []
    }
for each_day in trend_resp_json["Data"]:
    if datetime.strptime(each_day["Date"], '%m/%d/%Y').date() >= last_90_days_since:
        trend_data["Date"].append(each_day["Date"])
        trend_data["Confirmed"].append(each_day["Confirmed"])
        trend_data["Hospitalized"].append(each_day["Hospitalized"])
        trend_data["Recovered"].append(each_day["Recovered"])
        trend_data["Deaths"].append(each_day["Deaths"])
#print(Date)
#print(trend_data)
#dataF = DataFrame(trend_data,columns=["Confirmed", "Hospitalized", "Recovered", "Deaths"])
df2 = pandas.DataFrame(trend_data, columns=["Confirmed", "Hospitalized", "Recovered", "Deaths"])
ax = df2.plot(lw=4, colormap="jet", marker=".", markersize=10, title="Trend of COVID case in Thailand (last 90 days)")
#dataF.plot(kind="line", title=)
ax.set_xlabel("Date (last X days)")
ax.set_ylabel("Case count")
#plotG.plot(Date ,Confirmed ,Hospitalized ,Recovered ,Deaths)
plotG.show()


"""
Data = {'April': [111,531,58,421,256,90,147,500,40,150], 'May': [150,40,500,147,90,256,421,58,531,111] }
dataF = DataFrame(Data,columns=['April','May'])
plotG.plot(dataF)
#plotG.show()
"""
"""
    #plot_trend = plotG.figure(4)
print(Confirmed)
print(Hospitalized)
print(Recovered)
print(Deaths)"""
"""print("## response: " + str(response))
print("## response content: " + str(response.content))
print("## response json: " + str(today_resp_json))
#print(response.content[Confirmed])
print(today_resp_json["Confirmed"])
for key, value in today_resp_json.items():
    print(str(key) + ": " + str(value))"""
