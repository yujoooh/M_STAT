import pandas as pd
import numpy as np
import datetime
import calendar

sdorg = pd.read_excel('../INPUT/sdorg.xlsx')
sdmod = pd.read_excel('../INPUT/sdmod.xlsx')



sdate = sdorg['생산일'][0]
sdate = datetime.datetime.strptime(str(sdate), '%Y%m%d')
sday  = sdate.day
edate = calendar.monthrange(sdate.year, sdate.month)[1]
edate = sdate.replace(day=edate)
eday  = edate.day

sdorg = sdorg[['권역', '지역', '예측일자', '예보지수']]
sdmod = sdmod[['권역', '지역', '예측일자', '예보지수']]

sdorg = sdorg.rename(columns={'예보지수': '예측지수'})
sdmod = sdmod.rename(columns={'예보지수': '서비스지수'})

df = sdorg.copy()
df['서비스지수'] = sdmod['서비스지수']

siteli = ['실미도','소야도','웅도','제부도','무창포',\
          '선재도','하섬','화도','진도','동섬',      \
          '소매물도','우도','대섬','서건도']
sitedict = \
{ '실미도'   : '황해중부' , \
  '소야도'   : '황해중부' , \
  '웅도'     : '황해중부' , \
  '제부도'   : '황해중부' , \
  '무창포'   : '황해중부' , \
  '선재도'   : '황해중부' , \
  '하섬'     : '황해남부' , \
  '화도'     : '황해남부' , \
  '진도'     : '황해남부' , \
  '동섬'     : '남해동부' , \
  '소매물도' : '남해동부' , \
  '우도'     : '남해서부' , \
  '대섬'     : '남해서부' , \
  '서건도'   : '제주도' }

changedict = {'매우좋음':'5', '좋음':'4', '보통':'3', '나쁨':'2', '매우나쁨':'1', '체험불가':np.nan}
keyli = ['매우좋음','좋음','보통','나쁨','매우나쁨']

dfcnt = pd.DataFrame(columns=['Route', 'Point', 'O_LV5', 'O_LV4', 'O_LV3', 'O_LV2', 'O_LV1', 'M_LV5', 'M_LV4', 'M_LV3', 'M_LV2', 'M_LV1', 'TOTAL', 'CORRECT'])
for site in siteli:
    print(site)
    dfsite = df[ df['지역'] == site ].copy()
    areaty = sitedict[site]

    ocd = dfsite['예측지수'].value_counts()   # org_counts_dict
    if len(ocd) != 5:
        for key in keyli:
            if not key in ocd.keys(): ocd[key] = 0
    mcd = dfsite['서비스지수'].value_counts() # mod_counts_dict
    if len(mcd) != 5:
        for key in keyli:
            if not key in mcd.keys(): mcd[key] = 0
    row = [ areaty, site, \
            ocd['매우좋음'], ocd['좋음'], ocd['보통'], ocd['나쁨'], ocd['매우나쁨'], \
            mcd['매우좋음'], mcd['좋음'], mcd['보통'], mcd['나쁨'], mcd['매우나쁨'], \
            ocd.values.sum(), \
            sum(dfsite['예측지수'] == dfsite['서비스지수'])                          ]
    dfcnt = dfcnt.append(pd.Series(row, index=dfcnt.columns), ignore_index=True)

    for idx in range(eday):
        day = str(idx+1).zfill(2)
        dt_date = int(datetime.datetime.strftime(sdate.replace(day=int(day)), '%Y%m%d'))
        length = len(dfsite[dfsite['예측일자'] == dt_date])
        if   length == 0:
            row = [areaty, site, dt_date, '체험불가', '체험불가']
            dfsite = dfsite.append(pd.Series(row, index=dfsite.columns), ignore_index=True)
            row = [areaty, site, dt_date, '체험불가', '체험불가']
            dfsite = dfsite.append(pd.Series(row, index=dfsite.columns), ignore_index=True)
        elif length == 1:
            row = [areaty, site, dt_date, '체험불가', '체험불가']
            dfsite = dfsite.append(pd.Series(row, index=dfsite.columns), ignore_index=True)
        elif length == 2:
            pass
        else:
            print('check(3일 이상 날짜 존재): ' + site + ' ', dt_date)
    dfsite = dfsite.sort_values(by=['예측일자'], axis=0)
    dfsite = dfsite.replace({'예측지수': changedict, '서비스지수': changedict})
    dfsite.to_csv(site+'.dat', encoding='euckr', index=False, header=False)

row = [ '', '평균', \
        dfcnt['O_LV5'].sum(), dfcnt['O_LV4'].sum(), dfcnt['O_LV3'].sum(), dfcnt['O_LV2'].sum(), dfcnt['O_LV1'].sum(), \
        dfcnt['M_LV5'].sum(), dfcnt['M_LV4'].sum(), dfcnt['M_LV3'].sum(), dfcnt['M_LV2'].sum(), dfcnt['M_LV1'].sum(), \
        dfcnt['TOTAL'].sum(),   \
        dfcnt['CORRECT'].sum()  ]
dfcnt = dfcnt.append(pd.Series(row, index=dfcnt.columns), ignore_index=True)

dfcnt.loc[ dfcnt[dfcnt['TOTAL'] == 0].index, ['O_LV5', 'O_LV4', 'O_LV3', 'O_LV2', 'O_LV1'] ] = np.nan
dfcnt.loc[ dfcnt[dfcnt['TOTAL'] == 0].index, ['M_LV5', 'M_LV4', 'M_LV3', 'M_LV2', 'M_LV1'] ] = np.nan
dfcnt.loc[ dfcnt[dfcnt['TOTAL'] == 0].index, ['TOTAL', 'CORRECT'] ] = np.nan
dfcnt['RATIO'] = dfcnt['CORRECT'] / dfcnt['TOTAL'] *100

dfcnt.to_csv('cnt_SD_PRETABLE.csv', encoding='euckr', index=False)

dfrate = pd.DataFrame(columns=['Route', 'Point', 'O_LV5', 'O_LV4', 'O_LV3', 'O_LV2', 'O_LV1', 'M_LV5', 'M_LV4', 'M_LV3', 'M_LV2', 'M_LV1', 'TOTAL', 'CORRECT', 'RATIO'])
dfrate[['Route', 'Point', 'TOTAL', 'CORRECT', 'RATIO']] = dfcnt[['Route', 'Point', 'TOTAL', 'CORRECT', 'RATIO']]

dfrate['O_LV5']   = dfcnt['O_LV5'] / dfcnt['TOTAL'] *100
dfrate['O_LV4']   = dfcnt['O_LV4'] / dfcnt['TOTAL'] *100
dfrate['O_LV3']   = dfcnt['O_LV3'] / dfcnt['TOTAL'] *100
dfrate['O_LV2']   = dfcnt['O_LV2'] / dfcnt['TOTAL'] *100
dfrate['O_LV1']   = dfcnt['O_LV1'] / dfcnt['TOTAL'] *100

dfrate['M_LV5']   = dfcnt['M_LV5'] / dfcnt['TOTAL'] *100
dfrate['M_LV4']   = dfcnt['M_LV4'] / dfcnt['TOTAL'] *100
dfrate['M_LV3']   = dfcnt['M_LV3'] / dfcnt['TOTAL'] *100
dfrate['M_LV2']   = dfcnt['M_LV2'] / dfcnt['TOTAL'] *100
dfrate['M_LV1']   = dfcnt['M_LV1'] / dfcnt['TOTAL'] *100

dfrate.to_csv('../OUTPUT/TABLE/rate_SD_PRETABLE.csv', encoding='euckr', index=False)
dfrate.to_csv('../OUTPUT/TABLE/SD_PRETABLE.csv', encoding='euckr', index=False)
