import os,psutil
import html2text
import multiprocessing 
from bs4 import BeautifulSoup
def task(file_dir_lst,lock):

    for root,file in file_dir_lst:
        if file in download_Progress:
            print(file,':having changed')
            continue  
        
        with open(root + '/' + file,mode = 'r',encoding='utf8') as f:
            html = f.read()
            soup = BeautifulSoup(html, 'html.parser')
            

            for hidden_tag in soup.find_all('ix:header'):
                hidden_tag.decompose()
                
            for img_tag in soup.find_all('img'):
                img_tag.decompose()


            # Converting HTML content to plain text using html2text
            text_content = html2text.html2text(str(soup))
            with open(save_path + file[:-4] + 'txt',mode='w+',encoding="utf8") as f:
                    f.write(text_content)
                    f.flush()
                    print('success',file)
                   
            with lock:
                with open('progress of conversion.txt', mode='a', newline='') as f:
                        f.write(file  +  '\n')
                        f.flush()

 
 
 
def readTxt(file_name):
    if not os.path.exists(file_name):
        with open(file_name, "w") as f:
            f.write('')
    with open(file_name, "r") as f:
        data = f.read().splitlines()
        return data    

download_Progress = readTxt('progress of conversion.txt')
              
save_path = 'txt/'
if not os.path.exists(save_path):
    os.makedirs(save_path)
    
def hande(error):
    print(error)
                 
if __name__ == "__main__":
    file_dir_lst = []
    
    for root, dirs, files in os.walk('annual report'):
        file_dir_lst.extend([(root + '/',file) for file in files if file.endswith('html')])
    file_num = len(file_dir_lst) 
    cpu_count = psutil.cpu_count()+1
    total_group = cpu_count
    remainder = file_num % cpu_count
    group_count = file_num // total_group
    lock = multiprocessing.Manager().Lock()
    pool = multiprocessing.Pool(processes = cpu_count)#Use of multiple processes to improve statistical speed
    for  num in range(total_group):
       pool.apply_async(task, 
                        (file_dir_lst[num* group_count:(num+1)*group_count],lock ),error_callback=hande )#
       
            
    if remainder != 0:
        pool.apply_async(task,
                                (file_dir_lst[total_group*(group_count):],lock),error_callback=hande)#
        
    pool.close()
    pool.join()
   