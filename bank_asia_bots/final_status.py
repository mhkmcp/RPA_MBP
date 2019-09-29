import os

import pandas as pd
from googletrans import Translator
from difflib import SequenceMatcher
import traceback


dirname = os.path.dirname(__file__)

# FILE_TO_WRITE_TO = r'F:\bank_asia_selenium\final_info\final_status.csv'

# FILE_TO_READ_FROM = r'F:\bank_asia_selenium\final_info\compared.csv'

FILE_TO_WRITE_TO = os.path.join(dirname, 'final_info/final_status.csv')

FILE_TO_READ_FROM = os.path.join(dirname, 'final_info/compared.csv')


def set_columns(dataframe, colList=[]):
	for item in colList:
		dataframe[item] = ' '


# columns in info.csv
ACC_NO               = 'acnt_no'
ACC_HOLDER_NAME      = 'name'
AML_STATUS           = 'aml_sts'
NAME_CHECK           = 'namecheck'
FACE_MATCH_SIGN_CARD = 'sincrd_face_match'
FACE_MATCH_NID       = 'nid_face_match'
NOMINEE_MATCH        = 'nominee_match'
SECTOR_CODE_MATCH    = 'sector_code_match'
UPAZILA_PERC         = 'upazila % match'
DISTRICT_PERC        = 'district % match'
NOMINEE_GENDER_MATCH = 'nom_gender_check'
URLS                 = 'urls'
NID_PATH             = 'path'



df_all_info = pd.read_csv(FILE_TO_READ_FROM)


aml_check            = df_all_info[AML_STATUS]
name_check           = df_all_info[NAME_CHECK]
face_match_sign_card = df_all_info[FACE_MATCH_SIGN_CARD]
face_match_nid       = df_all_info[FACE_MATCH_NID]
nominee_match        = df_all_info[NOMINEE_MATCH]
sector_code_match    = df_all_info[SECTOR_CODE_MATCH]
upzila_match         = df_all_info[UPAZILA_PERC]
district_match       = df_all_info[DISTRICT_PERC]
nominee_gender_match = df_all_info[NOMINEE_GENDER_MATCH]
list_urls            = df_all_info[URLS]
nid_path             = df_all_info[NID_PATH]

# columns in final_status.csv
cols_to_set = [
		'ACC_NO',
		'ACC_HOLDER_NAME',
		'AML_STATUS',
		'NAME_CHECK',
		'FACE_MATCH_SIGN_CARD',
		'FACE_MATCH_NID',
		'NOMINEE_MATCH',
		'SECTOR_CODE_MATCH',
		'ADDRESS_MATCH',
        'NOMINEE_GENDER_MATCH',
        'URLS',
        'NID_PATH'
		]


def init_final_status():
	try:
		df_final_status = pd.read_csv(FILE_TO_WRITE_TO)
		col_index = 0
		for col in cols_to_set:
			if col not in df_final_status.columns:
				df_final_status.insert(col_index, col, ' ')
				# df_final_status[col] = ' '
			col_index+=1
	except FileNotFoundError as e:
		print('file does not exist. creating file...')
		df_final_status = pd.DataFrame()
		set_columns(df_final_status, cols_to_set)
		df_final_status.to_csv(FILE_TO_WRITE_TO, index=False)

	return df_final_status


def copy():
	data = {}
	data['ACC_NO'] = df_all_info[ACC_NO]
	data['ACC_HOLDER_NAME'] = df_all_info[ACC_HOLDER_NAME]
	data['AML_STATUS'] = df_all_info[AML_STATUS]
	data['NAME_CHECK'] = df_all_info[NAME_CHECK]
	data['FACE_MATCH_SIGN_CARD'] = df_all_info[FACE_MATCH_SIGN_CARD]
	data['FACE_MATCH_NID'] = df_all_info[FACE_MATCH_NID]
	data['NOMINEE_MATCH'] = df_all_info[NOMINEE_MATCH]
	data['ACC_HOLDER_NAME'] = df_all_info[ACC_HOLDER_NAME]
	data['SECTOR_CODE_MATCH'] = df_all_info[SECTOR_CODE_MATCH]

	data['UPAZILA_PERC'] = df_all_info[UPAZILA_PERC]
	data['DISTRICT_PERC'] = df_all_info[DISTRICT_PERC]
	data['NOMINEE_GENDER_MATCH']= df_all_info[NOMINEE_GENDER_MATCH]
	data['URLS']= df_all_info[URLS]
	data['NID_PATH']= df_all_info[NID_PATH]
	return data



def address_match(data):
	d = data
	addr_match = []
	upazila_perc = list(d['UPAZILA_PERC'])
	district_perc = list(d['DISTRICT_PERC'])

	for i, j in zip(upazila_perc, district_perc):
		try:
			if float(i) > 0.6 and float(j) > 0.6: 
				addr_match.append('address matched')
				# print('address matched')
			else:
				addr_match.append('address does not match')
				# print('address does not match')
		except ValueError as e:
			addr_match.append('address not found')
			continue
	return addr_match


def write_to_final_csv():
	# returns a dict
	cols = copy()
	
	# returns a list
	addr = address_match(cols)
	df = init_final_status()

	df['ACC_NO'] = cols['ACC_NO']
	df['ACC_HOLDER_NAME'] = cols['ACC_HOLDER_NAME']
	df['AML_STATUS'] = cols['AML_STATUS']
	df['NAME_CHECK'] = cols['NAME_CHECK']
	df['FACE_MATCH_SIGN_CARD'] = cols['FACE_MATCH_SIGN_CARD']
	df['FACE_MATCH_NID'] = cols['FACE_MATCH_NID']
	df['NOMINEE_MATCH'] = cols['NOMINEE_MATCH']
	df['ACC_HOLDER_NAME'] = cols['ACC_HOLDER_NAME']
	df['SECTOR_CODE_MATCH'] = cols['SECTOR_CODE_MATCH']
	df['NOMINEE_GENDER_MATCH'] = cols['NOMINEE_GENDER_MATCH']
	df['URLS'] = cols['URLS']
	df['NID_PATH'] = cols['NID_PATH']

	df['ADDRESS_MATCH'] = addr

	df.to_csv(FILE_TO_WRITE_TO, index=False)


write_to_final_csv()

# print(address_match(copy))
# print(copy())
