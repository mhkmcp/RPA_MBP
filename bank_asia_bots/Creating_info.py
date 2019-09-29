import time
from datetime import datetime
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import urllib.request
import cv2
import os
import csv
import boto3
import numpy as np
import pandas as pd

from bots.factory import broadcast_log


def execute_the_whole_thing():
    dirname = os.path.dirname(__file__)
    print("trying to execute, probably will fail")
    logs = []
    today = date.today()
    def gettinglogs(entry):
        now = datetime.now()
        logs.append("{0}-{1}".format(now, entry))
        broadcast_log(
            "<div class=\"c-feed__item c-feed__item--success\"><p><strong>{0}</strong> - {1}</p></div>".format(
                now.strftime("%m/%d/%Y %H:%M:%S"), entry))

    urls = []
    browser = webdriver.Chrome(os.path.join(dirname,r"chromedriver"))
    # browser = webdriver.Chrome('/usr/lib64/chromium/chromedriver')
    browser.maximize_window()
    browser.get(r'http://localhost/Login.html')
    log_in_user = r'//*[@id="P101_USERNAME"]'

    log_in_psw = r'//*[@id="P101_PASS"]'
    captcha = r'//*[@id="P101_CAPTCHA"]'
    log_in_button = r'//*[@id="B72277838335750912"]'
    ok_button = r'//*[@id="apexConfirmBtn"]/span'

    try:
        browser.find_element_by_xpath(log_in_user).send_keys("user")
        browser.find_element_by_xpath(log_in_psw).send_keys("password")
        browser.find_element_by_xpath(captcha).send_keys("NNFA6")
        browser.find_element_by_xpath(log_in_button).click()
        print("2")
    except:
        browser.find_element_by_xpath(ok_button)
        browser.find_element_by_xpath(ok_button).click()

        browser.find_element_by_xpath(log_in_psw).send_keys("password")
        browser.find_element_by_xpath(captcha).send_keys("NNFA6")
        browser.find_element_by_xpath(log_in_button).click()

    gettinglogs("logged in to erp system")

    browser.get(r'http://localhost/Account_Verificatio_list.html')
    verification_list = browser.window_handles[0]
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    # Account Info
    acnt_no_arr = []
    acnt_title_arr = []
    agent_boothname_arr = []
    sector_code_arr = []
    aml_token_arr = []

    # Personal Info
    name_arr = []
    gender_arr = []
    d_o_b_arr = []
    occupation_arr = []
    father_name_arr = []
    mother_name_arr = []
    maritual_status_arr = []
    spouse_name_arr = []

    # Contact Info
    mobile_no_arr = []
    mail_id_arr = []

    # Related Document
    document_type_arr = []
    document_no_arr = []

    # Accouny_Operator
    cutomer_id_arr = []
    cutomer_name_arr = []
    cutomer_dob_arr = []

    # Address Details

    perm_district_arr = []
    perm_upazila_arr = []
    perm_union_arr = []
    perm_village_arr = []
    pres_district_arr = []
    pres_upazila_arr = []
    pres_union_arr = []
    pres_village_arr = []

    # Nominee Info

    nom_name_arr = []
    nom_father_arr = []
    nom_mother_arr = []
    nom_dob_arr = []
    nom_rel_arr = []
    nom_percent_arr = []
    nom_doc_type_arr = []
    nom_doc_no_arr = []
    nom_img_arr = []
    nom_frnt_arr = []
    nom_bck_arr = []
    nom_gender = []

    # images

    live_pic_path = []
    added_pic_path = []
    signcard_pic_path = []
    nid_back_pic_path = []
    nom_image_path = []

    # verification
    name_check = []
    aml_sts = []
    nid_face_match = []
    sincrd_face_match = []
    nominee_match = []
    sector_code_match = []
    top_sign_check = []
    top_sign_mean = []
    nom_gender_check = []

    sign_resp = []

    table_id = browser.find_element(By.XPATH, '//*[@id="report_R44001444593139622"]')
    rows = table_id.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
    for row in rows:
        # Get the columns (all the column 2)
        try:
            col = row.find_elements(By.TAG_NAME, "td")[-1]  # note: index start from 0, 1 is col 2
            link = col.get_attribute('innerHTML')
            urls.append(link.split('"')[1])
            gettinglogs("taking the urls of all entries from verification list page")
        except:
            print("empty")
            gettinglogs("verification list page empty or no urls found")

    browser.execute_script("window.open('about:blank', 'details');")
    browser.switch_to.window("details")
    n = "#"
    i = 0  # loop counter
    length = len(urls)  # list length
    while i < length:
        if (urls[i] == n):
            urls.remove(urls[i])
            # as an element is removed
            # so decrease the length by 1
            length = length - 1
            # run loop again to check element
            # at same index, when item removed
            # next item will shift to the left
            continue
        i = i + 1

    # print list after removing given element
    print("list after removing elements:")
    print(urls)
    gettinglogs("traversing the links collected from ")
    for item in urls:
        browser.get(item)
        gettinglogs("going to{0}".format(str(item)))
        # Account Info
        acnt_no = browser.find_element_by_xpath(r'//*[@id="P826_AC_NO"]')
        acnt_no_str = acnt_no.text
        acnt_no_arr.append(acnt_no_str)

        acnt_title = browser.find_element_by_xpath(r'//*[@id="P826_ACC_TITLE"]')
        acnt_title_str = acnt_title.text
        acnt_title_arr.append(acnt_title_str)

        agent_boothname = browser.find_element_by_xpath(r'//*[@id="P826_AGENT_BOOTH_NAME"]')
        agent_boothname_str = agent_boothname.text
        agent_boothname_arr.append(agent_boothname_str)

        sector_code = browser.find_element_by_xpath(r'//*[@id="P826_SECTOR_CODE"]')
        sector_code_str = sector_code.text
        sector_code_arr.append(sector_code_str)

        aml_token = browser.find_element_by_xpath(r'//*[@id="P826_TOKEN_DISPLAY"]')
        aml_token_str = aml_token.text
        aml_token_arr.append(aml_token_str)

        # personal Info
        name = browser.find_element_by_xpath(r'//*[@id="P826_FIRST_NAME"]')
        name_str = name.text
        name_arr.append(name_str)

        gender = browser.find_element_by_xpath(r'//*[@id="P826_GENDER"]')
        gender_str = gender.text
        gender_arr.append(gender_str)

        d_o_b = browser.find_element_by_xpath(r'//*[@id="P826_CUST_DOB"]')
        d_o_b_str = d_o_b.text
        d_o_b_arr.append(d_o_b_str)

        occupation = browser.find_element_by_xpath(r'//*[@id="P826_OCCUPATION_CODE"]')
        occupation_str = occupation.text
        occupation_arr.append(occupation_str)

        father_name = browser.find_element_by_xpath(r'//*[@id="P826_FATHER_NAME"]')
        father_name_str = father_name.text
        father_name_arr.append(father_name_str)

        mother_name = browser.find_element_by_xpath(r'//*[@id="P826_MOTHER_NAME"]')
        mother_name_str = mother_name.text
        mother_name_arr.append(mother_name_str)

        maritual_status = browser.find_element_by_xpath(r'//*[@id="P826_MARITUAL_STATUS"]')
        maritual_status_str = maritual_status.text
        maritual_status_arr.append(maritual_status_str)

        spouse_name = browser.find_element_by_xpath(r'//*[@id="P826_SPOUSE_NAME"]')
        spouse_name_str = spouse_name.text
        spouse_name_arr.append(spouse_name_str)

        # Contact Info
        mobile_no = browser.find_element_by_xpath(r'//*[@id="P826_MOBILE_NO"]')
        mobile_no_str = mobile_no.text
        mobile_no_arr.append(mobile_no_str)

        mail_id = browser.find_element_by_xpath(r'//*[@id="P826_MAIL_ID"]')
        mail_id_str = mail_id.text
        mail_id_arr.append(mail_id_str)

        # Related Document
        document_type = browser.find_element_by_xpath(
            r'//*[@id="report_R51601459985692709"]/tbody[2]/tr/td/table/tbody/tr/td[1]')
        document_type_str = document_type.text
        document_type_arr.append(document_type_str)

        document_no = browser.find_element_by_xpath(
            r'//*[@id="report_R51601459985692709"]/tbody[2]/tr/td/table/tbody/tr/td[2]')
        document_no_str = document_no.text
        document_no_arr.append(document_no_str)

        # Accouny_Operator
        cutomer_id = browser.find_element_by_xpath(
            r'//*[@id="report_R62497158322150695"]/tbody[2]/tr/td/table/tbody/tr/td[1]')
        cutomer_id_str = cutomer_id.text
        cutomer_id_arr.append(cutomer_id_str)

        cutomer_name = browser.find_element_by_xpath(
            r'//*[@id="report_R62497158322150695"]/tbody[2]/tr/td/table/tbody/tr/td[2]')
        cutomer_name_str = cutomer_name.text
        cutomer_name_arr.append(cutomer_name_str)

        cutomer_dob = browser.find_element_by_xpath(
            r'//*[@id="report_R62497158322150695"]/tbody[2]/tr/td/table/tbody/tr/td[3]')
        cutomer_dob_str = cutomer_dob.text
        cutomer_dob_arr.append(cutomer_dob_str)

        # Address Details
        perm_district = browser.find_element_by_xpath(
            r'//*[@id="report_R51606549056692720"]/tbody[2]/tr/td/table/tbody/tr[1]/td[2]')
        perm_district_str = perm_district.text
        perm_district_arr.append(perm_district_str)

        perm_upazila = browser.find_element_by_xpath(
            r'//*[@id="report_R51606549056692720"]/tbody[2]/tr/td/table/tbody/tr[1]/td[3]')
        perm_upazila_str = perm_upazila.text
        perm_upazila_arr.append(perm_upazila_str)

        perm_union = browser.find_element_by_xpath(
            r'//*[@id="report_R51606549056692720"]/tbody[2]/tr/td/table/tbody/tr[1]/td[4]')
        perm_union_str = perm_union.text
        perm_union_arr.append(perm_union_str)

        perm_village = browser.find_element_by_xpath(
            r'//*[@id="report_R51606549056692720"]/tbody[2]/tr/td/table/tbody/tr[1]/td[6]')
        perm_village_str = perm_village.text
        perm_village_arr.append(perm_village_str)

        pres_district = browser.find_element_by_xpath(
            r'//*[@id="report_R51606549056692720"]/tbody[2]/tr/td/table/tbody/tr[2]/td[2]')
        pres_district_str = pres_district.text
        pres_district_arr.append(pres_district_str)

        pres_upazila = browser.find_element_by_xpath(
            r'//*[@id="report_R51606549056692720"]/tbody[2]/tr/td/table/tbody/tr[2]/td[3]')
        pres_upazila_str = pres_upazila.text
        pres_upazila_arr.append(pres_upazila_str)

        pres_union = browser.find_element_by_xpath(
            r'//*[@id="report_R51606549056692720"]/tbody[2]/tr/td/table/tbody/tr[2]/td[4]')
        pres_union_str = pres_union.text
        pres_union_arr.append(pres_union_str)

        pres_village = browser.find_element_by_xpath(
            r'//*[@id="report_R51606549056692720"]/tbody[2]/tr/td/table/tbody/tr[2]/td[6]')
        pres_village_str = pres_village.text
        pres_village_arr.append(pres_village_str)

        # Nominee Info

        nom_name = browser.find_element_by_xpath(
            r'//*[@id="report_R51682743462638959"]/tbody[2]/tr/td/table/tbody/tr/td[1]')
        nom_name_str = nom_name.text
        nom_name_arr.append(nom_name_str)
        nom_father = browser.find_element_by_xpath(
            r'//*[@id="report_R51682743462638959"]/tbody[2]/tr/td/table/tbody/tr/td[2]')
        nom_father_str = nom_father.text
        nom_father_arr.append(nom_father_str)
        nom_mother = browser.find_element_by_xpath(
            r'//*[@id="report_R51682743462638959"]/tbody[2]/tr/td/table/tbody/tr/td[3]')
        nom_mother_str = nom_mother.text
        nom_mother_arr.append(nom_mother_str)
        nom_dob = browser.find_element_by_xpath(
            r'//*[@id="report_R51682743462638959"]/tbody[2]/tr/td/table/tbody/tr/td[4]')
        nom_dob_str = nom_dob.text
        nom_dob_arr.append(nom_dob_str)
        nom_rel = browser.find_element_by_xpath(
            r'//*[@id="report_R51682743462638959"]/tbody[2]/tr/td/table/tbody/tr/td[5]')
        nom_rel_str = nom_rel.text
        nom_rel_arr.append(nom_rel_str)
        nom_percent = browser.find_element_by_xpath(
            r'//*[@id="report_R51682743462638959"]/tbody[2]/tr/td/table/tbody/tr/td[6]')
        nom_percent_str = nom_percent.text
        nom_percent_arr.append(nom_percent_str)
        nom_doc_type = browser.find_element_by_xpath(
            r'//*[@id="report_R51682743462638959"]/tbody[2]/tr/td/table/tbody/tr/td[7]')
        nom_doc_type_str = nom_doc_type.text
        nom_doc_type_arr.append(nom_doc_type_str)
        nom_doc_no = browser.find_element_by_xpath(
            r'//*[@id="report_R51682743462638959"]/tbody[2]/tr/td/table/tbody/tr/td[8]')
        nom_doc_no_str = nom_doc_no.text
        nom_doc_no_arr.append(nom_doc_no_str)
        nom_img = browser.find_element_by_xpath(
            r'//*[@id="report_R51682743462638959"]/tbody[2]/tr/td/table/tbody/tr/td[9]/img')
        if nom_img:
            nom_img_arr.append("present")
        else:
            nom_img_arr.append("not_present")
        nom_frnt = browser.find_element_by_xpath(
            r'//*[@id="report_R51682743462638959"]/tbody[2]/tr/td/table/tbody/tr/td[10]/img')
        if nom_frnt:
            nom_frnt_arr.append("present")
        else:
            nom_frnt_arr.append("not_present")
        nom_bck = browser.find_element_by_xpath(
            r'//*[@id="report_R51682743462638959"]/tbody[2]/tr/td/table/tbody/tr/td[11]/img')
        if nom_bck:
            nom_bck_arr.append("present")
        else:
            nom_bck_arr.append("not_present")

        gettinglogs("collected all text data from account number {0} verification detail page".format(acnt_no_str))
        # images
        live_img = browser.find_element_by_xpath(
            '//*[@id="report_R47260151525825765"]/tbody[2]/tr/td/table/tbody/tr/td/img')
        src = live_img.get_attribute('src')
        urllib.request.urlretrieve(src, os.path.join(dirname,r"data/live_pic/{0}live_pic.jpg".format(acnt_no_str)))
        live_pic_path.append(os.path.join(dirname,r"data/live_pic/{0}live_pic.jpg".format(acnt_no_str)))

        sign_img = browser.find_element_by_xpath(
            '//*[@id="report_R40084013193953156"]/tbody[2]/tr/td/table/tbody/tr/td/img')
        src = sign_img.get_attribute('src')
        urllib.request.urlretrieve(src, os.path.join(dirname,r"data/sign_Card/{0}sign_pic.jpg".format(acnt_no_str)))

        nid_frnt = browser.find_element_by_xpath(
            '//*[@id="report_R51601459985692709"]/tbody[2]/tr/td/table/tbody/tr/td[6]/img')
        src = nid_frnt.get_attribute('src')
        urllib.request.urlretrieve(src, os.path.join(dirname,r"data/nid_front/{0}nid_frnt.jpg".format(acnt_no_str)))

        nid_back = browser.find_element_by_xpath(
            '//*[@id="report_R51601459985692709"]/tbody[2]/tr/td/table/tbody/tr/td[7]/img')
        src = nid_back.get_attribute('src')
        urllib.request.urlretrieve(src, os.path.join(dirname,r"data/nid_back/{0}nid_back.jpg".format(acnt_no_str)))

        src = nom_img.get_attribute('src')
        urllib.request.urlretrieve(src, os.path.join(dirname,r"data/nom_img/{0}nom_img.jpg".format(acnt_no_str)))
        nom_image_path.append(os.path.join(dirname,r"data/nom_img/{0}nom_img.jpg".format(acnt_no_str)))

        nid_back_pic_path.append(os.path.join(dirname,r"data/nid_back/{0}nid_back.jpg".format(acnt_no_str)))

        img1 = cv2.imread(os.path.join(dirname,r"data/nid_front/{0}nid_frnt.jpg".format(acnt_no_str)))
        img2 = cv2.imread(os.path.join(dirname,r"data/sign_Card/{0}sign_pic.jpg".format(acnt_no_str)))

        gettinglogs("getting required images from account no -{0} ".format(acnt_no_str))

        def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
            w_min = min(im.shape[1] for im in im_list)
            im_list_resize = [
                cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                for im in im_list]
            return cv2.vconcat(im_list_resize)

        gettinglogs("concatinating images for  call of account no {0} ".format(acnt_no_str))

        im_v_resize = vconcat_resize_min([img1, img2])
        gettinglogs("concatinating images for call of account no {0} ".format(acnt_no_str))
        cv2.imwrite((os.path.join(dirname,r"data/full/{0}added.jpg".format(acnt_no_str))), im_v_resize)
        signcard_pic_path.append(os.path.join(dirname,r"data/sign_Card/{0}sign_pic.jpg".format(acnt_no_str)))
        os.remove(os.path.join(dirname,r"data/nid_front/{0}nid_frnt.jpg".format(acnt_no_str)))
        added_pic_path.append(os.path.join(dirname,r"data/full/{0}added.jpg".format(acnt_no_str)))

        gettinglogs("saving joined image of of account no {0} and saving the path to an array ".format(acnt_no_str))

        # with open(r'D:/Bank_Asia_poc/New folder/info.csv', 'a', newline='') as csvfile:
        #     spamwriter = csv.writer(csvfile, delimiter=',',
        #                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #     spamwriter.writerow([namr_str,gender_str,d_o_b_str,n_i_d_str])'''
        browser.refresh()

    # Define a dictionary containing Students data
    data = {"acnt_no": acnt_no_arr,
            "acnt_title": acnt_title_arr,
            "agent_boothname": agent_boothname_arr,
            "sector_code": sector_code_arr,
            "aml_token": aml_token_arr,
            "name": name_arr,
            "gender": gender_arr,
            "d_o_b": d_o_b_arr,
            "occupation": occupation_arr,
            "father_name": father_name_arr,
            "mother_name": mother_name_arr,
            "maritual_status": maritual_status_arr,
            "spouse_name": spouse_name_arr,
            "mobile_no": mobile_no_arr,
            "mail_id": mail_id_arr,
            "document_type": document_type_arr,
            "document_no": document_no_arr,
            "cutomer_id": cutomer_id_arr,
            "cutomer_name": cutomer_name_arr,
            "cutomer_dob": cutomer_dob_arr,
            "perm_district": perm_district_arr,
            "perm_upazila": perm_upazila_arr,
            "perm_union": perm_union_arr,
            "perm_village": perm_village_arr,
            "pres_district": pres_district_arr,
            "pres_upazila": pres_upazila_arr,
            "pres_union": pres_union_arr,
            "pres_village": pres_village_arr,
            "nom_name": nom_name_arr,
            "nom_father": nom_father_arr,
            "nom_mother": nom_mother_arr,
            "nom_dob": nom_dob_arr,
            "nom_rel": nom_rel_arr,
            "nom_percent": nom_percent_arr,
            "nom_doc_type": nom_doc_type_arr,
            "nom_doc_no": nom_doc_no_arr,
            "nom_img": nom_img_arr,
            "nom_frnt": nom_frnt_arr,
            "nom_bck": nom_bck_arr,
            "live_pic_path": live_pic_path,
            "added_pic_path": added_pic_path,
            "nid_back_pic_path": nid_back_pic_path,
            "signcard_pic_path": signcard_pic_path,
            "nom_image_path": nom_image_path
            }

    # Convert the dictionary into DataFrame
    df = pd.DataFrame(data)
    gettinglogs("saving all the collected information to a pandas dataframe ")

    # df.to_csv(r'F:/bank_asia_selenium/info/info.csv', index=False, )
    browser.execute_script("window.open('about:blank', 'aml');")
    browser.switch_to.window("aml")
    browser.get(r"http://localhost/aml_login.html")
    aml_user = browser.find_element_by_xpath(r'//*[@id="P101_USERNAME"]')
    aml_user.send_keys("user")
    aml_pass = browser.find_element_by_xpath(r'//*[@id="P101_PASSWORD"]')
    aml_pass.send_keys("user")
    aml_login_btn = browser.find_element_by_xpath(r'//*[@id="B218261236373174328"]')
    aml_login_btn.click()
    gettinglogs("going to aml checking page ")

    # doing aml check
    for index, row in df.iterrows():
        from_date = browser.find_element_by_xpath(r'//*[@id="P90_FROMDATE"]')
        from_date.clear()
        from_date.send_keys("28-AUG-10")
        to_date = browser.find_element_by_xpath(r'//*[@id="P90_DATETO"]')
        to_date.clear()
        to_date.send_keys("28-AUG-19")
        approv_stats = browser.find_element_by_xpath(r'// *[ @ id = "P90_APPROVAL_STATUS"] / option[1]')
        approv_stats.click()
        '''cutomer_id =  browser.find_element_by_xpath(r'//*[@id="P90_CUSTOMER_ID_lov_btn"]')
        cutomer_id.click()'''
        browser.get(r'http://localhost/Blacklist Screeningsearch_v2.html')
        aml_search_button = browser.find_element_by_xpath(r'//*[@id="P90_CUSTOMER_ID_lov_btn"]')
        aml_search_button.click()
        browser.switch_to_frame(0)
        aml_search_box = browser.find_element_by_xpath(r'//*[@id="SEARCH"]')
        aml_search_box.send_keys(row['acnt_no'])
        first_name = browser.find_element_by_xpath(r'/html/body/form/div[2]/a[2]')
        first_name.click()
        time.sleep(2)
        browser.switch_to_default_content()
        aml_close = browser.find_element_by_xpath(r'//*[@id="mymodal"]/div[2]/div[1]/button/span[1]')
        aml_close.click()
        aml_status = browser.find_element_by_xpath(
            r'//*[@id="report_R7989425346393805"]/div/div[1]/table/tbody/tr/td[11]/a')
        aml_status_str = aml_status.get_attribute("innerHTML")
        print(aml_status_str)
        aml_sts.append(aml_status_str)
        gettinglogs("going to aml checking page for account no {0} and getting the aml status".format(row['acnt_no']))
    df['aml_sts'] = aml_sts
    gettinglogs("saving all the aml status to the dataframe")
    # Checking Name
    gettinglogs("doing the name check for all the entries")
    for index, row in df.iterrows():
        if row['acnt_title'] == row['name'] and row['name'] == row['cutomer_name']:
            name_check.append("checked")
        else:
            name_check.append("not_checked")
    df["namecheck"] = name_check
    gettinglogs("name check done")
    # AWS info

    with open(os.path.join(dirname, r'credentials.csv'), 'r')as input:
        next(input)
        reader = csv.reader(input)
        for line in reader:
            access_key_id = line[2]
            secret_access_key = line[3]
    client = boto3.client('rekognition',
                          aws_access_key_id=access_key_id,
                          aws_secret_access_key=secret_access_key,
                          region_name='ap-south-1')

    # Face comparison using AWS
    gettinglogs("doing  face comparion ofr the entries")
    for index, row in df.iterrows():
        sim_arr = []

        img1 = row["added_pic_path"]
        img2 = row["live_pic_path"]

        with open(img1, 'rb')as source_image1:
            source_bytes1 = source_image1.read()

        with open(img2, 'rb')as source_image2:
            source_bytes2 = source_image2.read()

        response = client.compare_faces(
            SourceImage={'Bytes': source_bytes2},
            TargetImage={'Bytes': source_bytes1})

        for items in response['FaceMatches']:
            sim_arr.append(items['Similarity'])
            sign_resp.append(items)

        try:
            sincrd_face_match.append(sim_arr[0])
        except:
            sincrd_face_match.append("couldnt find face")

        try:
            nid_face_match.append(sim_arr[1])
        except:
            nid_face_match.append("couldnt find face")
        print("done")
        gettinglogs("done face compation for account no {0}".format(row["acnt_no"]))

    try:
        df["sincrd_face_match"] = sincrd_face_match
    except:
        df["sincrd_face_match"] = "couldnt find face"
    try:
        df["nid_face_match"] = nid_face_match
    except:
        df["nid_face_match"] = "couldnt find face"

    gettinglogs("compared faces and saved resuts to the dataframe")
    # nominee check

    gettinglogs("started nominee gender check using facial analysis")
    for index, row in df.iterrows():

        facial_analysis = boto3.client('rekognition',
                                       aws_access_key_id=access_key_id,
                                       aws_secret_access_key=secret_access_key,
                                       region_name='ap-south-1')
        with open(row["nom_image_path"], 'rb') as source_image1:
            source_bytes1 = source_image1.read()

        response_facial_analysis = client.detect_faces(
            Image={'Bytes': source_bytes1},
            Attributes=[
                'ALL'
            ])
        gettinglogs("done gender check for account no {0}".format(row["acnt_no"]))

        nom_gender.append(response_facial_analysis["FaceDetails"][0]["Gender"]["Value"].lower())

        gettinglogs("doing nominee relation check for account no {0}".format(row["acnt_no"]))

        if row["nom_rel"] == "Wife" or row["nom_rel"] == "Husband":
            if row["spouse_name"].lower() == row["nom_name"].lower():
                nominee_match.append("matched")
            else:
                nominee_match.append("not_matched")
        elif row["nom_rel"] == "Mother":
            if row["mother_name"].lower() == row["nom_name"].lower():
                nominee_match.append("matched")
            else:
                nominee_match.append("not_matched")
        elif row["nom_rel"] == "Father":
            if row["father_name"].lower() == row["nom_name"].lower():
                nominee_match.append("matched")
            else:
                nominee_match.append("not_matched")
        elif row["nom_rel"] == "Brother" or row["nom_rel"] == "Sister":
            if row["father_name"].lower() == row["nom_father"].lower() or row["mother_name"].lower() == row[
                "nom_mother"].lower():
                nominee_match.append("matched")
            else:
                nominee_match.append("not_matched")
        elif row["nom_rel"] == "Daughter" or row["nom_rel"] == "Son":
            if row["name"].lower() == row["father_name"].lower() or row["name"].lower() == row["mother_name"].lower():
                nominee_match.append("matched")
            else:
                nominee_match.append("not_matched")
        else:
            nominee_match.append("call_nominee")
    df["nominee_match"] = nominee_match
    df["nomine_gender"] = nom_gender

    female_nominee = ["wife", "mother", "sister", "aunt", "daughter"]
    male_nominee = ["husband", "father", "brother", "uncle", "son"]

    for index, row in df.iterrows():
        if row["nomine_gender"] == "female" and row["nom_rel"].lower() in female_nominee:
            nom_gender_check.append("correct")
        elif row["nomine_gender"] == "male" and row["nom_rel"].lower() in male_nominee:
            nom_gender_check.append("correct")
        elif row["nom_rel"].lower() == "cousin":
            nom_gender_check.append("correct")
        else:
            nom_gender_check.append("not_correct")

    df["nom_gender_check"] = nom_gender_check
    print("nom_gender_check", nom_gender_check)
    print("nom_gender", nom_gender)
    gettinglogs("done nominee check ")
    # sector code check

    for index, row in df.iterrows():
        gettinglogs("doing the sbs code check for account no {0}".format(row["acnt_no"]))
        if str(row["occupation"]) in str(row["sector_code"]):
            sector_code_match.append("correct")
        elif str(row["occupation"]) == "Housewife" and str(row["sector_code"]) == "915001-Housewives":
            sector_code_match.append("correct")
        elif str(row["occupation"]) == "Private Employment" and "Service Holder " in str(row["sector_code"]):
            sector_code_match.append("correct")
        elif str(row["occupation"]) == "Business" and str(row["sector_code"]) == "903009-Businessmen/Industrialist":
            sector_code_match.append("correct")
        else:
            gettinglogs("change in sbs code detected for account no {0}".format(row["acnt_no"]))
            browser.get(r'http://localhost/9.html')
            sbs_acnt_no = browser.find_element_by_xpath(r'//*[@id="P566_ACCOUNT_NO"]')
            sbs_customer_id = browser.find_element_by_xpath('//*[@id="P566_CUSTOMER_ID"]')
            sbs_acnt_no.send_keys(row['acnt_no'])
            sbs_customer_id.send_keys((row['cutomer_id']))
            browser.find_element_by_xpath(
                r'//*[@id="report_R38746871740511702"]/tbody[2]/tr/td/table/tbody/tr/td[8]/span/a/img').click()
            if str(row["occupation"]) == 'Housewife':
                browser.find_element_by_xpath(r'//*[@id="wwvFlowForm"]/div[1]/input[1]').send_keys('915001-Housewives')
            elif str(row["occupation"]) == 'Private Employment':
                browser.find_element_by_xpath(r'//*[@id="wwvFlowForm"]/div[1]/input[1]').send_keys(
                    '911000-Service Holder ( Working In Country)')
            elif str(row["occupation"]) == 'Business':
                browser.find_element_by_xpath(r'//*[@id="wwvFlowForm"]/div[1]/input[1]').send_keys(
                    '903009-Businessmen/Industrialist')
            sector_code_match.append("changed")
    gettinglogs("done sbs check and added to data frame")
    df['sector_code_match'] = sector_code_match

    # Signature in signcard check
    gettinglogs("started signature check for the sign card")
    for index, row in df.iterrows():

        path = (str(row["signcard_pic_path"]))
        img = cv2.imread(path)

        x_strt = int(img.shape[0] * (1.15 / 3))
        x_end = int(img.shape[0] * (1.7 / 3))
        y_strt = int(img.shape[1] * (0.8 / 3))
        y_end = int(img.shape[1]) - (int(img.shape[1]) * 2.5 / 6)
        width = int(x_end - x_strt)
        height = int(y_end - y_strt)

        crop_img = img[int(y_strt):int(y_end), int(x_strt):int(x_end + width)]
        cv2.imwrite((os.path.join(dirname,r"data/cropped/{0}cropped.jpg").format(row['acnt_no'])), crop_img)

        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        # --- Performing inverted binary threshold ---
        retval, thresh_gray = cv2.threshold(gray, 0, 255, type=cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        cv2.imwrite((os.path.join(dirname, r'data/thresh/{0}thresh.jpg').format(row['acnt_no'])), thresh_gray)

        norm_image = cv2.normalize(thresh_gray, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        sum_arr = np.sum(norm_image, axis=1)

        sign_cst = np.mean(sum_arr)

        top_sign_mean.append(sign_cst)
        if int(sign_cst) < 13:
            top_sign_check.append("no signature")
        else:
            top_sign_check.append("checked")
        gettinglogs("done signature check for account no{0}".format(row["acnt_no"]))

    df['top_sign_mean'] = top_sign_mean
    df['top_sign_check'] = top_sign_check
    gettinglogs("done all signature check")
    df['urls'] = urls

    # Saving to a CSV
    df.to_csv(os.path.join(dirname, r'info/info.csv'))
    gettinglogs("saving data from the data frame  to a csv file")
    browser.close()
    try:
        browser.switch_to.window("details")
        browser.close()
        browser.close()
    except:
        print("nope.. wont do that")

    with open("{0}_log.txt".format(today), "w") as txt_file:
        for line in logs:
            txt_file.write("".join(line) + "\n")

