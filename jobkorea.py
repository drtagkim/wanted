# -*- coding:utf-8 -*-
# ==================================== 
# Job Korea API
# Wanted Inc.
# Taekyung Kim PhD @ Suwon Univ.
# 2015. 02.
# jobkorea.py
# ==================================== 

# = Import External Module
import requests
from bs4 import BeautifulSoup as BS

# = URLs

class JobKoreaJobSeeking:
    def __init__(self):
        self.url_base = "http://www.jobkorea.co.kr/List_GG/GG_ADV_Search_List.asp?page=%d&ps=50#ListTop"
    def getPageSoup(self,page_no):
        page_url = self.url_base % (page_no,)
        try:
            r = requests.get(page_url)
            r.encoding = 'euc-kr'
        except:
            return []
        soup = BS(r.text,'html.parser')
        try:
            table_origin = soup.select("table.GGList > tr")
        except:
            return []
        table_data = [table_origin[i] for i in range(0, len(table_origin), 2)]
        return table_data
    def analyzePage(self,page_item_list):
        assert isinstance(page_item_list,list),"Input type must be a list."
        rv = []
        append_output = rv.append
        for sample in page_item_list:
            try:
                year_of_birth = re.findall('[0-9]{4}',sample.select("td.age span")[0]['title'])[0]
            except:
                year_of_birth = "NA"
            try:
                gender = re.findall('[^0-9 ()]+',sample.select("td.age")[0].text)[0]
            except:
                gender = "NA"
            try:
                personal_info_url = "%s%s"%(job_korea_url,sample.select('td.title > a')[0]['href'])
            except:
                personal_info_url = "NA"
            try:
                personal_id = re.findall("No=([0-9]+)",personal_info_url)[0]
            except:
                personal_id = ""
            try:
                resources = [s.text.strip() for s in sample.select("table.ability a.open_vst")]
            except:
                resources = []
            try:
                place_of_work = sample.select('td.area')[0].text
            except:
                place_of_work = ""
            try:
                salary = sample.select("span.salary_sum")[0].text
            except:
                salary = ""
            

class JobKoreaJobPosting:
'''
|  Job Korea API
|  Under testing
'''
    def __init__(self):
        self.seek_applicant_url_base = "http://www.jobkorea.co.kr/Recruit/Search/Detail?Oem_Code=C1/"
        self.company_big = "%s%d&schstat=1&psTab=50&Page=%s#JobList" % (seek_applicant_url_base,3,"%d")
        self.company_big_child = "%s%d&schstat=1&psTab=50&Page=%s#JobList" % (seek_applicant_url_base,4,"%d")
        self.company_small = "%s%d&schstat=1&psTab=50&Page=%s#JobList" % (seek_applicant_url_base,1,"%d")
        self.company_medium = "%s%d&schstat=1&psTab=50&Page=%s#JobList" % (seek_applicant_url_base,2,"%d")
        self.company_venture = "%s%d&schstat=1&psTab=50&Page=%s#JobList" % (seek_applicant_url_base,5,"%d")
        self.company_foreign_inv = "%s%d&schstat=1&psTab=50&Page=%s#JobList" % (seek_applicant_url_base,6,"%d")
        self.company_foreign_pub = "%s%d&schstat=1&psTab=50&Page=%s#JobList" % (seek_applicant_url_base,8,"%d")
        self.company_public = "%s%d&schstat=1&psTab=50&Page=%s#JobList" % (seek_applicant_url_base,7,"%d")
        self.company_ngo_domestic = "%s%d&schstat=1&psTab=50&Page=%s#JobList" % (seek_applicant_url_base,9,"%d")
        self.company_ngo_foreign = "%s%d&schstat=1&psTab=50&Page=%s#JobList" % (seek_applicant_url_base,10,"%d")
    def getInfoItem(self, in_item):
    '''
        |  Retreiving information from job lists by each item
        |  Par 1 : input item
    '''
            out_item = {}
            try:    
                out_item['comp_info_url'] = "%s%s"%(job_korea_url,in_item.select("a.emp1")[0].attrs['href']) # title
                out_item['comp_name'] = in_item.select("a.emp1")[0].text
                out_item['recruit_doc_url'] = "%s%s"%(job_korea_url,in_item.select("a.emp1")[1].attrs['href'])
                out_item['recruit_doc_title'] = in_item.select("a.emp1")[1].text
                out_item['desc_short'] = in_item.select("p.txtDesc")[0].text
                out_item['apply_condition'] = in_item('td')[2].next.strip()
                out_item['apply_schooling'] = in_item('td')[2].next.next.text.strip()
                out_item['work_conditions'] = [i.text.strip() for i in in_item('td')[3].select('span.txt')]
            except Exception:
                print "Error"
            return out_item
    def retreive_jobs_listed(self,type_name,upto=-1, timeout_wait=60, retry=5, lagged=30):
        # variables:
        page = 1
        iteration_control = True
        rv = []
        rv_append = rv.append
        # determine a type
        if type_name == "big":
            base_url = self.company_big
        elif type_name == "big_child":
            base_url = self.company_big_child
        elif type_name == "small":
            base_url = self.company_small
        elif type_name == "medium":
            base_url = self.company_medium
        elif type_name == "venture":
            base_url = self.company_venture
        elif type_name == "foreign_inv":
            base_url = self.company_foreign_inv
        elif type_name == "foreign_pub":
            base_url = self.company_foreign_pub
        elif type_name == "public":
            base_url = self.company_public
        elif type_name == "ngo_domestic":
            base_url = self.company_ngo_domestic
        elif type_name == "ngo_foreign"
            base_url = self.company_ngo_foreign
        else:
            return rv
            # nothing to return cause of wrong type inputted
        while iteration_control:
            now_url = base_url % (page,)
            # TODO: try-except BEGIN
            r = requests.get(now_url)
            soup = BS(r.text)
            # END
            eles = soup.select("div.lgiTplList")
            try:
                items = eles[0]("tr")
                for item in items:
                    rv_append(getInfoItem(item))
            except
                iteration_control = False
            if upto <= 0:
                page = page + 1
            else:
                if page >= upto:
                    iteration_control = False
                else:
                    page = page + 1
        return rv