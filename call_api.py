import requests
import json
from datetime import datetime, timedelta, date
import pandas
import matplotlib.pyplot as plt
import numpy as np

requests.packages.urllib3.disable_warnings()    # due to API have no cert so we won"t verify SSL certificate and this is to disable warning msg
fig = plt.figure() # create figure of graph

APIs = {
    "covid_today": "https://covid19.ddc.moph.go.th/api/open/today"
    , "covid_sum": "https://covid19.ddc.moph.go.th/api/open/cases/sum"
    , "covid_trend": "https://covid19.ddc.moph.go.th/api/open/timeline"
}

# today data
today_field = []
today_value = []
today_case_type = ["Confirmed", "Hospitalized", "Recovered", "Deaths"]
# trend data
today_date = date.today()
last_90_days_since = (today_date - timedelta(days=90))  #for trend data
trend_column = ["Date","Confirmed", "Hospitalized", "Recovered", "Deaths"]

def api_caller(endpoint):
    resp_json = ""
    response = requests.get(APIs[endpoint], verify=False)
    calling_time = str(datetime.now())
    resp_status_code = str(response.status_code)
    print("Calling: " + endpoint + " at time: "+ calling_time + ", Got response code: "+ resp_status_code)
    if (resp_status_code == "200"):
        resp_json = json.loads(response.content)
        print(" (" + endpoint + " data last updated on: " + resp_json["UpdateDate"] + ")")
        return(resp_json)
    else:
        print("Please retry as a response code is not 200, it is: "+ resp_status_code + " at " + calling_time)

def gen_today_data(data_type):
    compare = "+" if today_resp_json["New" + data_type] >= 0 else "-"
    today_field.append(data_type + " case")
    today_value.append(str(today_resp_json[data_type]) + " (" + compare + str(today_resp_json["New" + data_type]) + ")")

def plot_today_graph(today_field, today_value, today_title):
    fig.add_subplot(331)
    table = plt.table(cellText=[[today_field[0],today_value[0]],[today_field[1],today_value[1]],[today_field[2],today_value[2]],[today_field[3],today_value[3]]],
                        colLabels=["Total case", "Number"],
                        rowLoc='center',
                        loc='center'
                        )
    table.auto_set_font_size(False)
    table.set_fontsize(15)
    plt.title(today_title, 
                fontweight ="bold")
# case summary
def gen_covid_cases(sum_by, case_index, case_value, plot_title, top):
    sum_resp_json[sum_by].sort(key = lambda x:x["Count"], reverse=True) # sort DESC
    column = []
    value = []
    for each_field in sum_resp_json[sum_by][:top]:
        index = each_field[case_index]
        if index == "หญิง":
            index = "Women"
        elif index == "ชาย":
            index = "Men"
        elif index == "ไทย":
            index = "Thailand"
        if len(index) > 15:
            index = index[:15]    # trim if len > 15
        column.append(index)
        value.append(each_field[case_value])
    #plot bar graph
    if sum_by == "Gender":
        fig.add_subplot(332)
        plt.bar(column, value)
    elif sum_by == "Nation":
        fig.add_subplot(333)
        plt.bar(column, value)
        plt.xticks(rotation = 20)   # rotate x-axis text in case it's province na,e
    elif sum_by == "Province":
        fig.add_subplot(312)
        plt.barh(column, value)

    for i in range(len(column)):
        plt.text(i,value[i],value[i], ha = 'center')    # each bar label
    plt.title(plot_title, fontweight ="bold")

# trend data
def gen_covid_trend(trend_resp_json):
    trend_resp_json["Data"].sort(key = lambda x:datetime.strptime(x["Date"], '%m/%d/%Y').date(), reverse=True) # sort date DESC
    trend_data = {}
    for i in trend_column:
        trend_data[i] = []
    for each_day in trend_resp_json["Data"]:
        if datetime.strptime(each_day["Date"], '%m/%d/%Y').date() >= last_90_days_since:
            for c in trend_column:
                trend_data[c].append(each_day[c])
    # plot graph
    fig.add_subplot(313)
    df = pandas.DataFrame(trend_data, columns=trend_column[1:])
    ax = df.plot(ax=plt.gca(),lw=4, colormap="jet", marker=".", markersize=5, title="Trend of COVID case in Thailand (last 90 days)")
    #ax.legend(loc=2)   # upper left
    ax.set_xlabel("Date (last X days)")
    ax.set_ylabel("Case count")
    
### get today data ###
today_resp_json = api_caller("covid_today")
for d in today_case_type:
    gen_today_data(d)
plot_today_graph(today_field, today_value, "Number of COVID case today")

### get sum data ### # Province, Nation, Gender
sum_resp_json = api_caller("covid_sum")
gen_covid_cases("Gender", "Gender", "Count", "Today's COVID cases by gender", 3)
gen_covid_cases("Nation", "Nation", "Count", "Today's COVID cases by Nation (top 10)", 10)
gen_covid_cases("Province", "ProvinceEn", "Count", "Today's COVID cases by Thailand province (top 15)", 15)

### get trend data ###
trend_resp_json = api_caller("covid_trend")
gen_covid_trend(trend_resp_json)

# show graphs
fig.canvas.draw()
#fig.tight_layout(pad=30)

plt.subplots_adjust(left=0.08, right=0.98, bottom=0.05, top=0.97, wspace=0.20, hspace=0.2)

mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
plt.show()