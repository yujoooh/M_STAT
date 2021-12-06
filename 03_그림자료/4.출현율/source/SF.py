#[Geosystem Research : Department of Marine Forecast ]
#[Created by C.K. Park on 2018.10.23]
#[Edit 2019.03.05 by C.K. Park]

#2021년 10월 21일 전까지는 일 1회 바다낚시 서비스 지수 제공 그에따른 코드는 아래와 같음

import xlrd
import xlwt
import win32com.client
import os
import calendar
from datetime import date, timedelta
from datetime import datetime

ORG_FILE = '../INPUT/sforg.xlsx'
MOD_FILE = '../INPUT/sfmod.xlsx'
#산출된 예보지수자료 읽기-------------------------------------------------------------------------
ORG = xlrd.open_workbook(ORG_FILE)
org_sheet = ORG.sheet_by_index(0)

MOD = xlrd.open_workbook(MOD_FILE)
mod_sheet = MOD.sheet_by_index(0)

nxo = org_sheet.ncols
nyo = org_sheet.nrows
nxm = mod_sheet.ncols
nym = mod_sheet.nrows
ny = org_sheet.nrows
#print(nx,ny)

ii = 0
jj = 0
org = []
mod = []
org_list = []
mod_list = []
while ii < nxo:
	jj = 0
	while jj < nyo:
		org.append(str(org_sheet.col_values(ii)[jj]))
		jj += 1
	org.append(str('SD'))
	org_list.append(org)
	org = []
	ii += 1
	jj = 0
ii = 0
jj = 0
while ii < nxm:
	jj = 0
	while jj < nym:
		mod.append(str(mod_sheet.col_values(ii)[jj]))
		jj += 1
	mod_list.append(mod)
	mod = []
	ii += 1
	jj = 0

org_Route = org_list[2] #권역
org_Point = org_list[3] #지점
org_FDATE = org_list[4] #예측일자
org_FISH = org_list[5] #어종
org_INDEX = org_list[28] #지수

mod_Route = mod_list[2] #권역
mod_Point = mod_list[3] #지점
mod_FDATE = mod_list[4] #예측일자
mod_FISH = mod_list[5] #어종
mod_INDEX = mod_list[28] #지수
#print(org_Route, org_Point, org_FDATE, org_FISH, org_INDEX)

#지수 지점정보 파일 - 추가시 갱신필요
POINT_INFILE = open('./SF_INFO.txt','r')
STN = [str(INFO) for INFO in POINT_INFILE.readlines()]
NUM_STN = len(STN)
ii = 0
#출현율표 저장파일
PREVALENCE = open('../OUTPUT/TABLE/SF_PRETABLE.csv','w')
table = [] #출현율 저장 list

while ii < NUM_STN:
	STATION = STN[ii].split()
	POINT_NAME = STATION[0]
	FISH_NAME = STATION[1]
	num = '%02d'% ii
	OUTFILE = '../OUTPUT/GRAPH/'+POINT_NAME+'('+FISH_NAME+')'+'.dat' # 지점별 예측지수, 서비스지수 그래프 입력자료 저장파일
	print(OUTFILE)
	file = open(OUTFILE,'a')
	jj = 1
	kk = 1
	data = []
	cc = 0
	O_LV5 = 0 ; O_LV4 = 0 ; O_LV3 = 0 ; O_LV2 = 0 ; O_LV1 = 0; O_LV0 = 0 #예측지수 등급별 초기화
	M_LV5 = 0 ; M_LV4 = 0 ; M_LV3 = 0 ; M_LV2 = 0 ; M_LV1 = 0; M_LV0 = 0 #서비스지수 등급별 초기화
	correct = 0
	
	while jj < ny:
		O_Point = org_Point[jj].replace(" ","") # 띄어쓰기 삭제
		O_FISH = org_FISH[jj].replace(" ","") # 띄어쓰기 삭제
		O_DATE = int(float(org_FDATE[jj]))
		O_DATE = datetime.strptime(str(O_DATE), "%Y%m%d").date()
		O_DATE = datetime.strftime(O_DATE, "%Y-%m-%d")
		O_INDEX = str(org_INDEX[jj])

		M_Point = mod_Point[jj].replace(" ","") # 띄어쓰기 삭제
		M_FISH = mod_FISH[jj].replace(" ","") # 띄어쓰기 삭제
		#M_DATE = mod_FDATE[jj]
		M_DATE = int(float(mod_FDATE[jj]))
		M_DATE = datetime.strptime(str(M_DATE), "%Y%m%d").date()
		M_DATE = datetime.strftime(M_DATE, "%Y-%m-%d")
		M_INDEX = str(mod_INDEX[jj])

		tmp = int(float(org_FDATE[jj]))
		tmp = datetime.strptime(str(tmp), "%Y%m%d").date()
		tmp = datetime.strftime(tmp, "%Y-%m-%d").split('-')
		yr = int(tmp[0]); mn = int(tmp[1]); dy = int(tmp[2])
		edy = calendar.monthrange(yr,mn)[1]
		start_day = str(date(yr,mn,1))
		end_day = str(date(yr,mn,edy))
		#print(org_FDATE[jj], tmp, yr, mn, start_day, end_day)
		
		if POINT_NAME == O_Point and FISH_NAME == O_FISH: # SKEQ_INFO의 POINT_NAME과 예측지수의 포인트 정보가 같을 경우 계산시작
			after_day = str(date(yr,mn,kk))
			if kk == 1 : after_day = str(date(yr,mn,2))
			ody = O_DATE.split('-')[2]
			ady = after_day.split('-')[2]
			
			# 월별 자료 공백 채우기
			if kk == 1 and O_DATE != start_day:
				data.append([O_Point, O_FISH, str(date(yr,mn,1)), " ", " "])
				print(O_Point, O_FISH, str(date(yr,mn,1)), " ", " ")
				if kk+1 <= calendar.monthrange(yr,mn)[1] : kk += 1 ; after_day = str(date(yr,mn,kk))

			elif kk != 1 and ody != ady:
				data.append([O_Point, O_FISH, str(date(yr,mn,kk)), " ", " "])
				print(O_Point, O_FISH, str(date(yr,mn,kk)), " ", " ")
				if kk+1 <= calendar.monthrange(yr,mn)[1] : kk += 1 ; after_day = str(date(yr,mn,kk))
				
				if POINT_NAME == O_Point and POINT_NAME == M_Point and O_DATE == M_DATE:
					if O_INDEX == "매우좋음" : O_SCORE = 5 ; O_LV5 += 1 # 등급별 숫자 변환 및 카운팅
					if O_INDEX == "좋음"    : O_SCORE = 4 ; O_LV4 += 1
					if O_INDEX == "보통"    : O_SCORE = 3 ; O_LV3 += 1
					if O_INDEX == "나쁨"    : O_SCORE = 2 ; O_LV2 += 1
					if O_INDEX == "매우나쁨" : O_SCORE = 1 ; O_LV1 += 1
					if O_INDEX == "체험불가" : O_SCORE = 0 ; O_LV0 += 1
                        
					if M_INDEX == "매우좋음" : M_SCORE = 5 ; M_LV5 += 1
					if M_INDEX == "좋음"    : M_SCORE = 4 ; M_LV4 += 1
					if M_INDEX == "보통"    : M_SCORE = 3 ; M_LV3 += 1
					if M_INDEX == "나쁨"    : M_SCORE = 2 ; M_LV2 += 1
					if M_INDEX == "매우나쁨" : M_SCORE = 1 ; M_LV1 += 1
					if M_INDEX == "체험불가" : M_SCORE = 0 ; M_LV0 += 1


					if O_INDEX == M_INDEX and O_INDEX !=  "체험불가" :
						correct = correct + 1
					
					data.append([O_Point, O_FISH, O_DATE, O_SCORE, M_SCORE])
					print(O_Point, O_FISH, O_DATE, O_SCORE, M_SCORE)
					if kk+1 <= calendar.monthrange(yr,mn)[1] : kk += 1 ; after_day = str(date(yr,mn,kk))

			elif POINT_NAME == O_Point and POINT_NAME == M_Point and O_DATE == M_DATE :
				if O_INDEX == "매우좋음" : O_SCORE = 5 ; O_LV5 += 1 # 등급별 숫자 변환 및 카운팅
				if O_INDEX == "좋음"    : O_SCORE = 4 ; O_LV4 += 1 
				if O_INDEX == "보통"    : O_SCORE = 3 ; O_LV3 += 1 
				if O_INDEX == "나쁨"    : O_SCORE = 2 ; O_LV2 += 1 
				if O_INDEX == "매우나쁨" : O_SCORE = 1 ; O_LV1 += 1
				if O_INDEX == "체험불가" : O_SCORE = 0 ; O_LV0 += 1
                    
				if M_INDEX == "매우좋음" : M_SCORE = 5 ; M_LV5 += 1
				if M_INDEX == "좋음"    : M_SCORE = 4 ; M_LV4 += 1 
				if M_INDEX == "보통"    : M_SCORE = 3 ; M_LV3 += 1 
				if M_INDEX == "나쁨"    : M_SCORE = 2 ; M_LV2 += 1 
				if M_INDEX == "매우나쁨" : M_SCORE = 1 ; M_LV1 += 1
				if M_INDEX == "체험불가" : M_SCORE = 0 ; M_LV0 += 1

				if O_INDEX == M_INDEX and O_INDEX !=  "체험불가" :
					correct = correct + 1

				data.append([O_Point, O_FISH, O_DATE, O_SCORE, M_SCORE])
				print(O_Point, O_FISH, O_DATE, O_SCORE, M_SCORE)
				if kk+1 <= calendar.monthrange(yr,mn)[1] : 	kk += 1 ; after_day = str(date(yr,mn,kk))
		
		jj += 1
	# TOTAL COUNT
	O_TOTAL = O_LV5 + O_LV4 + O_LV3 + O_LV2 + O_LV1
	M_TOTAL = M_LV5 + M_LV4 + M_LV3 + M_LV2 + M_LV1
	
	# Ratio
	if O_TOTAL != 0 :
		OR_LV5 = round((float(O_LV5) / float(O_TOTAL) * 100),2)
		OR_LV4 = round((float(O_LV4) / float(O_TOTAL) * 100),2)
		OR_LV3 = round((float(O_LV3) / float(O_TOTAL) * 100),2)
		OR_LV2 = round((float(O_LV2) / float(O_TOTAL) * 100),2)
		OR_LV1 = round((float(O_LV1) / float(O_TOTAL) * 100),2)
	else:
		OR_LV5 = 0 ; OR_LV4 = 0 ; OR_LV3 = 0 ; OR_LV2 = 0 ; OR_LV1 = 0
		
	if M_TOTAL != 0 :
		MR_LV5 = round((float(M_LV5) / float(O_TOTAL) * 100),2)
		MR_LV4 = round((float(M_LV4) / float(O_TOTAL) * 100),2)
		MR_LV3 = round((float(M_LV3) / float(O_TOTAL) * 100),2)
		MR_LV2 = round((float(M_LV2) / float(O_TOTAL) * 100),2)
		MR_LV1 = round((float(M_LV1) / float(O_TOTAL) * 100),2)
	else:
		MR_LV5 = 0 ; MR_LV4 = 0 ; MR_LV3 = 0 ; MR_LV2 = 0 ; MR_LV1 = 0
#일치율
	if O_TOTAL != 0 :
		CORRECT_RATIO = correct / O_TOTAL * 100
	else :
		CORRECT_RATIO = 0
	
	table.append([POINT_NAME, FISH_NAME, OR_LV5, OR_LV4, OR_LV3, OR_LV2, OR_LV1, MR_LV5, MR_LV4, MR_LV3, MR_LV2, MR_LV1, O_TOTAL, correct, CORRECT_RATIO])
	print(POINT_NAME, FISH_NAME, OR_LV5, OR_LV4, OR_LV3, OR_LV2, OR_LV1, MR_LV5, MR_LV4, MR_LV3, MR_LV2, MR_LV1,O_TOTAL, correct, CORRECT_RATIO)	
	for i in data:
		file.write('{0},{1},{2},{3},{4}\n'.format(i[0],i[1],i[2],i[3],i[4]))
	file.close()

	ii += 1
PREVALENCE.write('Route, Point, O_LV5, O_LV4, R_LV3, O_LV2, O_LV1, M_LV5, M_LV4, M_LV3, M_LV2, M_LV1, TOTAL, CORRECT, RATIO\n') # 출현율 헤더
for i in table:
	PREVALENCE.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14}\n'.format(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11], i[12], i[13], i[14]))	