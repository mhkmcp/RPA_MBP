import os

import pandas as pd
from googletrans import Translator
from difflib import SequenceMatcher
import traceback


dirname = os.path.dirname(__file__)

def similar(a, b):
	a = a.lower()
	b = b.lower()
	return SequenceMatcher(None, a, b).ratio()

def compare_this():
        # FILE_NID = r'F:\bank_asia_selenium\NIDs\done_nids.csv'
        FILE_NID = os.path.join(dirname, 'NIDs/done_nids.csv')
        # FILE_ERP = r'F:\bank_asia_selenium\info\info.csv'
        FILE_ERP = os.path.join(dirname, 'info/info.csv')

        translator = Translator()
        df1 = pd.read_csv(FILE_NID)
        df2 = pd.read_csv(FILE_ERP)
        df2['nid_upazila'] = ' '
        df2['erp_upazila'] = ' '
        df2['upazila % match'] = ' '
        df2['nid_district'] = ' '
        df2['erp_district'] = ' '
        df2['district % match'] = ' '
        df2['path'] = ' '


        # df2.to_csv(r'F:\bank_asia_selenium\final_info\compared.csv', index=False)
        df2.to_csv(os.path.join(dirname, 'final_info\compared.csv'), index=False)

        #df2 = pd.read_csv('new.csv')

        for index1, row1 in df1.iterrows():
                try:
                        name = row1['name'].strip().lower()
                        path = row1['path']
                        
                        upazila, district = (row1['address']).strip().split(',')[-2:]
                        upazila = translator.translate(upazila).text
                        
                        district = translator.translate(district).text
                        for index2, row2 in df2.iterrows():
                                if row2['cutomer_name'].strip().lower() == name:
                                        match_upazila = similar(upazila, row2['perm_upazila'])
                                        match_district = similar(district, row2['perm_district'])
                                        


                                        df2.at[index2, 'nid_upazila'] = upazila
                                        df2.at[index2, 'erp_upazila'] = row2['perm_upazila']
                                        df2.at[index2, 'upazila % match'] = match_upazila

                                        df2.at[index2, 'nid_district'] = district
                                        df2.at[index2, 'erp_district'] = row2['perm_district']
                                        df2.at[index2, 'district % match'] = match_district
                                        df2.at[index2, 'path'] = path




                                        # this won't work
                                        # row2['nid_district'] = district

                                        break
                                else:
                                        continue
                except Exception as e:
                        # print(traceback.format_exc())
                        print(e)
                        continue
        # df2.to_csv(r'F:\bank_asia_selenium\final_info\compared.csv', index=False)
        df2.to_csv(os.path.join(dirname, 'final_info/compared.csv'), index=False)
        return True

compare_this()

# for index, row in df2.iterrows():
# 	if row['name'].strip().lower() == 'sumon kumar':
# 		print('found')
# 		break
# 	else: 
# 		print('not found')





# for index, row in df2.iterrows():
# 	print((row['cutomer_name']).strip().lower())
