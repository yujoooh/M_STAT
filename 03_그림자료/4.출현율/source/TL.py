import pandas as pd
import numpy as np
import datetime
import calendar

tlorg = pd.read_excel('../INPUT/tlorg.xlsx')
tlmod = pd.read_excel('../INPUT/tlmod.xlsx')

sdate = tlorg['생산일'][0]
sdate = datetime.datetime.strptime(str(sdate), '%Y%m%d')
sday  = sdate.day
edate = calendar.monthrange(sdate.year, sdate.month)[1]
edate = sdate.replace(day=edate)
eday  = edate.day

tlorg = tlorg[['권역', '지역', '예측일자', '예보지수']]
tlmod = tlmod[['권역', '지역', '예측일자', '예보지수']]

tlorg = tlorg.rename(columns={'예보지수': '예측지수'})
tlmod = tlmod.rename(columns={'예보지수': '서비스지수'})

df = tlorg.copy()
df['서비스지수'] = tlmod['서비스지수']

siteli = ['백미리마을','월하성마을','선감마을','병술만마을','만돌마을',\
          '하전마을','돌머리마을','신시도마을','죽림마을','마시안','둔장마을','백사마을',      \
          '장양마을','거차마을','문항마을','다대마을','냉천마을']
sitedict = \
{ '백미리마을'   : '황해중부' , \
  '월하성마을'   : '황해중부' , \
  '선감마을'     : '황해중부' , \
  '병술만마을'   : '황해중부' , \
  '만돌마을'   : '황해남부' , \
  '하전마을'   : '황해남부' , \
  '돌머리마을'     : '황해남부' , \
  '신시도마을'     : '황해남부' , \
  '죽림마을'     : '황해남부' , \
  '마시안'     : '황해중부' , \
  '둔장마을'     : '황해남부' , \
  '백사마을'     : '남해서부' , \
  '장양마을' : '남해서부' , \
  '거차마을'     : '남해서부' , \
  '문항마을'     : '남해동부' , \
  '다대마을'     : '남해동부' , \
  '냉천마을'   : '남해동부' }

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
        else:
            pass
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

dfcnt.to_csv('../OUTPUT/TABLE/cnt_TL_PRETABLE.csv', encoding='euckr', index=False)

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

dfrate.to_csv('../OUTPUT/TABLE/rate_TL_PRETABLE.csv', encoding='euckr', index=False)
dfrate.to_csv('../OUTPUT/TABLE/TL_PRETABLE.csv', encoding='euckr', index=False)
