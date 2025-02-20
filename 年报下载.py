import csv, requests, os, time,threading
import concurrent.futures
headers = {
    'User-Agent': 'MyCompanyBot/1.0 (contact@mycompany.com; +1234567890;;Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
   'referer':'https://www.sec.gov/edgar/search/?r=el',
   #'cookie':'ak_bmsc=16EA8ADB26802FC6089547EBB0BA1ACE~000000000000000000000000000000~YAAQJNgjF4nd0FyRAQAArEpOZhitZWYAtNZkq2MM2nPMFC5mPIV7KOAB6Trhhwvacz1Di4I+OQHNlWtfpBxgs4WrP9lhQs0yXUkRdOTj0TNe/ml25V+srsjBezhuyfcml4jv0EI1wLD/CsrYyJ17xkBxYVNah13UCnejPuqaLvBAIcmXohBaJ0AqQxe/pujkbE4KHGLq/eBfyqKcgskFBJSh0e0e+D07utleZ2xytu6Nnj72Adu4H0dk1Gt48fxUC21IstSRBJ7Dvg9Yj2WjbdIC3F54s+yDmQMUpLkNyG6VVB26cNaGp/ahIznVAtxSNKsqqaLUo82sm7YHSUB0czb8bM6brRwhCEnAuv322wIxYM4HvIKPxXaJx5Ve0Z3IrB4JHYVFIe9cLk8QNhCVlr8XkfbXxw18xwqa3TGqTJ51QQHaWZv/x4pQEgTjsWaNYH7Y1IHIBRif; _4c_=%7B%22_4c_s_%22%3A%22dZJLT8MwDID%2FyuTz2uXVpukNDQlxAATicZy2JKwRrK3SsDKm%2FneS0DGGoJdWnz87ruM99JWuocScUCEKKkhe8Cm86F0H5R6sUeG1hRK4YpkUdJnkiuCErRBNCsZFojGjkvJ8yTCHKbzHWkIQTgXKOB%2BmoOpDDauV7sy6PvEyIihF3jOtG0UfITjDGUUUZSduJME9lFTwZ9z2x1IxkCFa0BM1Eq%2B29tep%2F6uyHdU9yEZpfzwWKS5SlDx3vg%2F34QkrEISijXqTbuF2bdB6vZp06sUHlN4aqRe9Ua6K%2BQQdaaXNunIBo1hFhd4A%2B6%2Fe1Krpv9ME%2BQG%2Fs0TOPF3Zpu90SJxXttnoCSbhYhp%2FofAUM0KvVj9ra6NWOdd25Wwm63Rl6nUqm83MG51xofVOy3TdbEfgF%2BOLJV%2Fs0QSqJvfzO8%2Bvf5Db%2Bc3ViC7OFg%2BX5%2FFvESKEMsLTcdh%2BSWA4zJqhsFFh6H6W7hXKImcoPMMwfAI%3D%22%7D; bm_sv=4CC2EEEE1CBDAE154B78ABAB93F4FE41~YAAQbL0oF9GSb2CRAQAAZRRSZhgiiDVaBRboaaDOXFKuIACJaicCAUjJdtGgcuNXqyfDxhibMUSZEEj10aNTDmxD0k66gLp8vLxa2o5tn01kNStquPlBnXo/oOwyLwBShxIWUo+xxYfxA/r7FyAzofX3nKy5Gbbx6qK4vCkLSOJAv7SOlbL7XhYyZouhTloUYVH/MIYP/TVZrdZfCDn8oeg6eXzpBq4yL7cd4KpgFeo5DS/yjkChIA8qUU9f~1; _gat_UA-30394047-1=1; _ga_CSLL4ZEK4L=GS1.1.1723998378.13.1.1723998627.0.0.0; _ga=GA1.2.1900223427.1722151390;',
   'Sec-Fetch-User':'?1'
}
url = 'https://www.sec.gov/Archives/edgar/data/'

def readTxt(file_name):  # 读取已下载的公司代码
    if not os.path.exists(file_name):
        with open(file_name, "w") as f:
            f.write('')
    with open(file_name, "r") as f:
        data = f.read().splitlines()
        return data    

download_Progress = readTxt('年报下载进度.txt')  # 读取已下载进度

if not os.path.exists("年报"):
    os.mkdir('年报')

# 假设CSV文件路径
csv_file = 'data.csv'

def get_data(download_Progress):
    # 打开CSV文件进行读取
    with open(csv_file, mode='r', newline='', encoding='utf8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader if row['id'] not in download_Progress]

def download(rows, lock, num):
    # 逐行读取数据，每行返回一个字典
    for row in rows:
        tem = row['id'].split(':')
        target_url = url + row['cik'] + '/' + tem[0].replace('-', '') + '/' + tem[1]
       
        print(target_url)
        while True:
            try:
                res = requests.get(headers=headers, url=target_url)
                time.sleep(num / 5)
                break
            except Exception as e:
                print('请求失败,两分钟后重试', e)
                time.sleep(120)
      
        if res.status_code == 200:
            html = res.text
            
            file_name = '年报/' + row['标题'] + '-' + row['截止时间'] + '-' + row["cik"] + '.html'            
            with open(file_name, mode='w', encoding='utf8') as file:
                file.write(html)
                    
            with lock:
                with open('年报下载进度.txt', mode='a', newline='') as file:
                    file.write(row['id'] + '\n')
                    file.flush()

file_dir_lst = get_data(download_Progress)
file_num = len(file_dir_lst)
cpu_count = 5

total_group = cpu_count
remainder = file_num % cpu_count
group_count = file_num // total_group

if __name__ == '__main__':
    lock = threading.Lock()  # 使用线程锁
    with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_count) as executor:
        futures = []
        # 使用线程池下载
        for num in range(total_group):
            futures.append(executor.submit(download, file_dir_lst[num * group_count:(num + 1) * group_count], lock, num))

        # 处理余数部分
        if remainder != 0:
            futures.append(executor.submit(download, file_dir_lst[total_group * group_count:], lock, total_group))

        executor.shutdown(wait=True)

