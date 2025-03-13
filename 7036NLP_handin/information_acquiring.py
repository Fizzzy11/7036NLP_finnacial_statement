import requests,time,csv,os,re
import pandas as pd

if not os.path.exists("data.csv"):
        with open('data.csv', mode='a', newline='',encoding='utf8') as file:
            writer = csv.writer(file)
            writer.writerow(['title','year','cik','id'])   
    
def readTxt(file_name):# Read downloaded company codes
    if not os.path.exists(file_name):
        with open(file_name, "w") as f:
            f.write('')
    with open(file_name, "r") as f:
        data = f.read().splitlines()
        return data    

download_Progress = readTxt('Progress of Downloading Annual Report Information.txt')# 读取已下载年报信息下载进度

url = 'https://efts.sec.gov/LATEST/search-index'
params = {
    #'from':'100',data_json['hits']['total']["value"]
    'dateRange': 'all',
    'category': 'custom',
    'entityName': '0000927971',
    'forms': '10-K',
    'startdt': '2019-01-01',
    'enddt': '2025-02-03'
}

headers = {
    'User-Agent': 'MyConyBot/8.0 (contact@mycompany.com; +1234567890;;Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
   'referer':'https://www.sec.gov/edgar/search/?r=el',
   'cookie':'ak_bmsc=16EA8ADB26802FC6089547EBB0BA1ACE~000000000000000000000000000000~YAAQJNgjF4nd0FyRAQAArEpOZhitZWYAtNZkq2MM2nPMFC5mPIV7KOAB6Trhhwvacz1Di4I+OQHNlWtfpBxgs4WrP9lhQs0yXUkRdOTj0TNe/ml25V+srsjBezhuyfcml4jv0EI1wLD/CsrYyJ17xkBxYVNah13UCnejPuqaLvBAIcmXohBaJ0AqQxe/pujkbE4KHGLq/eBfyqKcgskFBJSh0e0e+D07utleZ2xytu6Nnj72Adu4H0dk1Gt48fxUC21IstSRBJ7Dvg9Yj2WjbdIC3F54s+yDmQMUpLkNyG6VVB26cNaGp/ahIznVAtxSNKsqqaLUo82sm7YHSUB0czb8bM6brRwhCEnAuv322wIxYM4HvIKPxXaJx5Ve0Z3IrB4JHYVFIe9cLk8QNhCVlr8XkfbXxw18xwqa3TGqTJ51QQHaWZv/x4pQEgTjsWaNYH7Y1IHIBRif; _4c_=%7B%22_4c_s_%22%3A%22dZJLT8MwDID%2FyuTz2uXVpukNDQlxAATicZy2JKwRrK3SsDKm%2FneS0DGGoJdWnz87ruM99JWuocScUCEKKkhe8Cm86F0H5R6sUeG1hRK4YpkUdJnkiuCErRBNCsZFojGjkvJ8yTCHKbzHWkIQTgXKOB%2BmoOpDDauV7sy6PvEyIihF3jOtG0UfITjDGUUUZSduJME9lFTwZ9z2x1IxkCFa0BM1Eq%2B29tep%2F6uyHdU9yEZpfzwWKS5SlDx3vg%2F34QkrEISijXqTbuF2bdB6vZp06sUHlN4aqRe9Ua6K%2BQQdaaXNunIBo1hFhd4A%2B6%2Fe1Krpv9ME%2BQG%2Fs0TOPF3Zpu90SJxXttnoCSbhYhp%2FofAUM0KvVj9ra6NWOdd25Wwm63Rl6nUqm83MG51xofVOy3TdbEfgF%2BOLJV%2Fs0QSqJvfzO8%2Bvf5Db%2Bc3ViC7OFg%2BX5%2FFvESKEMsLTcdh%2BSWA4zJqhsFFh6H6W7hXKImcoPMMwfAI%3D%22%7D; bm_sv=4CC2EEEE1CBDAE154B78ABAB93F4FE41~YAAQbL0oF9GSb2CRAQAAZRRSZhgiiDVaBRboaaDOXFKuIACJaicCAUjJdtGgcuNXqyfDxhibMUSZEEj10aNTDmxD0k66gLp8vLxa2o5tn01kNStquPlBnXo/oOwyLwBShxIWUo+xxYfxA/r7FyAzofX3nKy5Gbbx6qK4vCkLSOJAv7SOlbL7XhYyZouhTloUYVH/MIYP/TVZrdZfCDn8oeg6eXzpBq4yL7cd4KpgFeo5DS/yjkChIA8qUU9f~1; _gat_UA-30394047-1=1; _ga_CSLL4ZEK4L=GS1.1.1723998378.13.1.1723998627.0.0.0; _ga=GA1.2.1900223427.1722151390;',
   'Sec-Fetch-User':'?1'
}

def get_cik():
    result =  pd.read_excel('cik.xlsx')
    print(result)
 
    full_ciks = []
    ciks = []
    titls = []
   

    for cik,title in zip(result['cik'],result['security']):
        cik_ = str(cik)
       
        #sys.exit()
        if len( cik_) < 10:
            lenth = 10 - len( cik_)
            for i in range(lenth):
                    cik_ = "0" +  cik_
                    
        if not cik_ in ciks:        
            full_ciks.append(cik_)
            
        if not  cik in ciks:
            ciks.append(str(cik))
            
        if not title in titls:
            titls.append(title)
        #print(cik)
      
        
    return full_ciks,ciks,titls


full_ciks,ciks,titls = get_cik()    
   
for full_cik,cik,title in zip(full_ciks,ciks,titls):
    print(cik)
                       
    if cik in download_Progress:
        print(f'{cik}having obtained,skip')

        continue
  
    params['entityName'] = full_cik
    
    while True:
        try:
            all_data = []
            response = requests.get(url, params=params, headers=headers)
            text =response.text
            print(response.url)
            time.sleep(0.5)
            break
        except requests.exceptions.RequestException as e:
            print('Request failed. Retry in two minutes.',e)
            time.sleep(120)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()['hits']['hits']
        if not data:
            continue
        
        pattern = r'\((.*?)\)'
        all_data = []
        for x in data:
            name = x ["_source"]["display_names"][0]
            
            match = re.search(pattern, name)
            if match:
                name = match.group(1)
            else:
                name = 'miss'
            date =    x["_source"]["period_ending"]
            if date: 
                year = x["_source"]["period_ending"]
            else:
                continue
                    
                
            
            all_data.append([name,year,cik,x['_id']])
                   
        
            
    if all_data:
        with open('data.csv', mode='a', newline='',encoding='utf8') as file:
            writer = csv.writer(file)
            writer.writerows(all_data) 
            file.flush()
                
    with open('Progress of Downloading Annual Report Information.txt', mode='a', newline='') as file:
        file.write(cik + '\n')
        print(f'{cik}finished')
        



