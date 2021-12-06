import pandas as pd
import os
import datetime

def converter(value):
    if value == '매우나쁨'  : score = 1  
    elif value == '나쁨' : score = 2  
    elif value == '보통' : score = 3
    elif value == '좋음' : score = 4
    elif value == '매우좋음' : score = 5
    return score

org = pd.read_excel('../INPUT/srorg.xlsx')
mod = pd.read_excel('../INPUT/srmod.xlsx')

arealist = ['송정해수욕장']

start= input("분석 월")
end = input("분석 월 +1 :")
start_date = datetime.date(2021, int(start), 1)
end_date   = datetime.date(2021, int(end), 1)

datelist = [ int((start_date + datetime.timedelta(n)).strftime("%Y%m%d")) for n in range(int ((end_date - start_date).days))]

total = pd.DataFrame(index = range(0), columns = ['O_LV5','O_LV4','O_LV3','O_LV2','O_LV1','M_LV5','M_LV4','M_LV3','M_LV2','M_LV1'])
for area in arealist:
    data = pd.DataFrame(index = range(len(org)), columns = ['구분','지역','예측날짜', '오전오후', '예측지수', '서비스지수'])
    data['구분'] = org[org['지역'] == area]['구분']
    data['지역'] = org[org['지역'] == area]['지역']
    data['예측날짜'] = org[org['지역'] == area]['예측날짜']
    data['오전오후'] = org[org['지역'] == area]['오전오후']
    data['예측지수'] = org[org['지역'] == area]['예보지수'].apply(converter)
    data['서비스지수'] = mod[mod['지역'] == area]['예보지수'].apply(converter)
    
    for date in datelist:
        if len(data[data['예측날짜'] == date]) ==2:
    #         print('해당날짜 다 있음')
            pass
        else:
            print("위 날짜 없음 "+ str(date))
            row = [data['구분'].iloc[0], area, date, 'AM', '', '']
            data= data.append(pd.Series(row, index=data.columns), ignore_index=True)
            row = [data['구분'].iloc[0], area, date, 'PM', '', '']
            data= data.append(pd.Series(row, index=data.columns), ignore_index=True)
    data = data.sort_values(by=['예측날짜'], axis=0)
    data.to_csv('../OUTPUT/GRAPH/'+area+'_SR.dat', header = None, index = False)
    
    index = ['매우좋음','좋음','보통','나쁨','매우나쁨']
    counts1 = pd.DataFrame(org['예보지수'].value_counts(),index = index)
    counts1 = round(counts1/counts1.sum()*100,1)
    counts1 = counts1.reindex(index)
    counts1.fillna(0, inplace=True)
    counts1= counts1.transpose()
    counts1.index.values[0] = area

    counts2 = pd.DataFrame(mod['예보지수'].value_counts(),index = index)
    counts2 = round(counts2/counts2.sum()*100,1)
    counts2 = counts2.reindex(index)
    counts2.fillna(0, inplace=True)
    counts2= counts2.transpose()
    counts2.index.values[0] = area

    merge = pd.concat([counts1,counts2],axis=1)
    merge.columns = ['O_LV5','O_LV4','O_LV3','O_LV2','O_LV1','M_LV5','M_LV4','M_LV3','M_LV2','M_LV1']
    total = total.append(merge)    
    
total.to_csv('../OUTPUT/TABLE/SR_PRETABLE.csv', encoding='euckr')