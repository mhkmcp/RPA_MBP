#!/usr/bin/env python
# coding: utf-8

import os
import time
from datetime import datetime

# In[5]:
import django
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from bots.factory import broadcast_log, email_results

dirname = os.path.dirname(__file__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rpa.settings")
django.setup()


def verify():
    dirname = os.path.dirname(__file__)

    df_final_status = pd.read_csv(os.path.join(dirname, r'final_info/final_status.csv'))
    file = os.path.join(dirname, r'final_info/final_status.csv')

    # browser = webdriver.Chrome(os.path.join(dirname, 'chromedriver.exe'))
    browser = webdriver.Chrome('/usr/lib64/chromium/chromedriver')
    # browser = webdriver.Chrome('/usr/bin/chromedriver')

    browser.maximize_window()

    actions = ActionChains(browser)

    total_remarks = []

    aml_button_xpath = r'//*[@id="P826_AML_CHECK_0"]'
    live_pic_button_xpath = r'//*[@id="P826_PHOTO_CHECK_0"]'
    sign_card_button_xpath = r'//*[@id="P826_SIG_CHECK_0"]'
    nom_img_xpath = r'//*[@id="P826_NOM_CHECK_0"]'
    nid_xpath = r'//*[@id="P826_NID_CHECK_0"]'

    for index, row in df_final_status.iterrows():
        browser.get(row["URLS"])
        remarks = []
        remarks.append(row["ACC_NO"])
        if row['AML_STATUS'].lower() == "already checked":
            browser.find_element_by_xpath(aml_button_xpath).click()
        else:
            remarks.append("AML not checked")

        browser.find_element_by_xpath(live_pic_button_xpath).click()
        if row["FACE_MATCH_SIGN_CARD"].lower() != "couldnt find face" or row["SIGN_CARD"] == "checked":
            browser.find_element_by_xpath(sign_card_button_xpath).click()
        else:
            remarks.append("sign card error")

        try:

            if row["FACE_MATCH_NID"] != "couldnt find face":
                actions.send_keys(Keys.PAGE_DOWN).perform()
                time.sleep(1)
                browser.find_element_by_id("P826_NID_CHECK_0").click()
            else:
                remarks.append("bad NID picture")
            if row["NOMINEE_MATCH"].lower() == "matched" and row["NOMINEE_GENDER_MATCH"] == "correct":
                actions.send_keys(Keys.PAGE_DOWN).perform()
                time.sleep(1)
                browser.find_element_by_id("P826_NOM_CHECK_0").click()
            else:
                remarks.append("nominee didnt match")
        except:
            print("hitting footer")

        if row["NAME_CHECK"] != "checked":
            remarks.append("name not checked")
        try:
            browser.find_element_by_id('P826_BROWSE').send_keys(row["NID_PATH"])
        except:
            remarks.append("no nid image")

        total_remarks.append(remarks)

    browser.get(r'http://localhost/Account_Verificatio_list.html')

    for i in range(len(total_remarks)):
        account_no = browser.find_element_by_xpath(
            '//*[@id="report_R44001444593139622"]/tbody[2]/tr/td/table/tbody/tr[{0}]/td[1]'.format(index + 1))
        print(account_no.text)
        try:
            if i + 1 < 10:
                remarks = browser.find_element_by_xpath('//*[@id="f02_000{0}"]'.format(i + 1))
                total_remarks[i].pop(0)
                remarks.send_keys(' and '.join(total_remarks[i]))
                if len(total_remarks[i]) != 0:
                    need_change = browser.find_element_by_xpath(r'//*[@id="f03_000{0}_0001"]'.format(i + 1))
                    need_change.click()
                else:
                    no_change = browser.find_element_by_xpath(r'//*[@id="f03_000{0}_0002"]'.format(i + 1))
                    no_change.click()

                print(' and '.join(total_remarks[i]))
            else:
                remarks = browser.find_element_by_xpath('//*[@id="f02_00{0}"]'.format(i + 1))
                total_remarks[i].pop(0)
                remarks.send_keys(' and '.join(total_remarks[i]))
                print(' and '.join(total_remarks[i]))
                if len(total_remarks[i]) != 0:
                    need_change = browser.find_element_by_xpath(r'//*[@id="f03_00{0}_0001"]'.format(i + 1))
                    need_change.click()
                else:
                    no_change = browser.find_element_by_xpath(r'//*[@id="f03_00{0}_0002"]'.format(i + 1))
                    no_change.click()
        except:
            pass

    remarks = browser.find_element_by_xpath('//*[@id="f02_0014"]')
    remarks.send_keys(' and '.join(total_remarks[-1]))
    print(' and '.join(total_remarks[-1]))
    if len(total_remarks[-1]) != 0:
        need_change = browser.find_element_by_xpath(r'//*[@id="f03_0014_0001"]')
        need_change.click()
    else:
        no_change = browser.find_element_by_xpath(r'//*[@id="f03_0014_0002"]')
        no_change.click()

    # browser.quit()
    print(total_remarks)
    submit = browser.find_element_by_xpath(r'//*[@id="B35815888295108623"]/span')
    # submit.click()
    df_final_status["final_remarks"] = total_remarks
    df_final_status.to_csv(file)
    time.sleep(2)
    browser.quit()

    now = datetime.now()

    broadcast_log(
        "<div class=\"c-feed__item c-feed__item--success\"><p><strong>{0}</strong> - {1}</p></div>".format(
            now.strftime("%m/%d/%Y %H:%M:%S"), "All the process are completed"))
    broadcast_log(
        "<div class=\"c-feed__item c-feed__item--success\"><p><strong>{0}</strong> - {1}</p></div>".format(
            now.strftime("%m/%d/%Y %H:%M:%S"), "Sending Email"))

    email_results()

# In[6]:
