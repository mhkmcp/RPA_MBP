#!/usr/bin/env python
# coding: utf-8

# In[17]:


import logging
import django
import urllib.request
from datetime import date
from datetime import datetime

from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer

from bots.factory import broadcast_log
from .comparison import compare_this
from .final_status import *
from .verification import *

dirname = os.path.dirname(__file__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rpa.settings")
django.setup()


class Event(LoggingEventHandler):
    print("hello")
    c = 1

    def dispatch(self, event):

        logs = []

        def gettinglogs(entry):
            now = datetime.now()
            logs.append("{0}-{1}".format(now, entry))
            broadcast_log("<div class=\"c-feed__item c-feed__item--success\"><p><strong>{0}</strong> - {1}</p></div>".format(now.strftime("%m/%d/%Y %H:%M:%S"), entry))

        today = date.today()
        if self.c == 1 or self.c % 2 != 0:
            username = 'citybank'
            password = 'abcd4321'
            print("world")
            time.sleep(2)
            # inputFile = r'F:\bank_asia_selenium\info\info.csv'
            inputFile = os.path.join(dirname, 'info/info.csv')
            print(dirname)
            print(os.path.join(dirname, 'chromedriver'))
            # browser = webdriver.Chrome(os.path.join(dirname, 'chromedriver.exe'))
            browser = webdriver.Chrome('/usr/lib64/chromium/chromedriver')
            df = pd.read_csv(inputFile)  # or pd.read_excel(filename) for xls file
            browser.get(r'http://nid.techcomengine.com/')
            gettinglogs("going to the nid website")
            browser.find_element_by_xpath(r'//*[@id="wrapper"]/h3/a').click()
            browser.find_element_by_xpath(r'//*[@id="id_username"]').send_keys(username)
            browser.find_element_by_xpath(r'//*[@id="pwd"]').send_keys(password)
            browser.find_element_by_xpath(r'//*[@id="wrapper"]/div/form/div[4]/div/button').click()
            gettinglogs("logging in to nid website")
            done_nid = []
            entry_no = []
            address_arr = []
            name_arr = []
            nid_img = []
            nid_df = pd.DataFrame()
            months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', "AUG", 'SEP', 'OCT', 'NOV', 'DEC']
            for index, row in df.iterrows():
                gettinglogs("doing nid check for account no {0}".format(row['acnt_no']))
                try:
                    browser.find_element_by_xpath(r'//*[@id="nid"]').send_keys(row['document_no'])
                    date1 = str(row['d_o_b'])
                    formated = date1.split("-")

                    mon = months.index(str(formated[1]))
                    if mon + 1 < 10:
                        actual = "0" + str(mon + 1)
                    else:
                        actual = (mon + 1)

                    if int(formated[2]) < 19:
                        formatted1 = "20" + str(formated[2])
                    else:
                        formatted1 = "19" + str(formated[2])

                    new = str(formated[0]) + "-" + str(actual) + "-" + formatted1

                    browser.find_element_by_xpath(r'//*[@id="dob"]').send_keys(new)
                    browser.find_element_by_xpath(r'//*[@id="nid_form"]/div[3]/div/button').click()
                    address = browser.find_element_by_xpath('//*[@id="nidResults"]/div[2]/dd[6]')
                    address_str = address.text
                    address_arr.append(address_str)

                    name = browser.find_element_by_xpath('//*[@id="nidResults"]/div[2]/dd[2]')
                    name_str = name.text
                    name_arr.append(name_str)

                    img = browser.find_element_by_xpath('//*[@id="nidResults"]/div[2]/dd[7]/img')
                    src = img.get_attribute('src')
                    # directory = r'F:\bank_asia_selenium\NIDs\{0}'.format(today)
                    directory = os.path.join(dirname, 'NIDs/{0}').format(today)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    image_name = r"{0}\{1}.png".format(directory, row['acnt_no'])
                    nid_img.append(image_name)
                    urllib.request.urlretrieve(src, image_name)
                    done_nid.append(row['document_no'])
                    entry_no.append(index)
                    gettinglogs("done nid check and saved nid image of account no {0}".format(row['acnt_no']))


                except:
                    print("Nid Validation error")
                    name_arr.append(str(row['name']))
                    address_arr.append("nid_error")
                    done_nid.append(row['document_no'])
                    nid_img.append("no image found")
                    entry_no.append(index)
                    gettinglogs("tried nid chck for account no {0} and found error".format(row['acnt_no']))

            self.c = self.c + 1
        else:
            print("error _ fix it")
            self.c = self.c + 1
        try:
            nid_df['done_nid'] = done_nid
            nid_df['entry_no'] = entry_no
            nid_df['address'] = address_arr
            nid_df['name'] = name_arr
            nid_df['path'] = nid_img
            gettinglogs("done nid check saved it into a csv")
            # nid_df.to_csv(r"F:\bank_asia_selenium\NIDs\done_nids.csv")
            nid_df.to_csv(os.path.join(dirname, 'NIDs/done_nids.csv'))
        except:
            print("error")

        compare_this()
        gettinglogs("done comparing address and name from NID and erp and saved to a it to a CSV")

        write_to_final_csv()
        gettinglogs("making a final CSV of all the checks")

        gettinglogs("started final verification")
        verify()
        gettinglogs("Done final verification")

        with open("{0}_log.txt".format(today), "a") as txt_file:
            for line in logs:
                txt_file.write("".join(line) + "\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # path = r'F:\bank_asia_selenium\info'
    path = os.path.join(dirname, 'info')
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
