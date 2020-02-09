# -*- coding: utf-8 -*-

# v3: now automatically name pdf files!
# v3b: changed structure.

import urllib.request,os,time
import math

diag_mode=False

if diag_mode:
    print('diagnostic mode ON. verbose personality ON.')
    
find_name_flag=True
print('find_name_flag = ',find_name_flag,'\nT/F to toggle name_flag.\n')



print('''usage: enter one of the following: \n
1. yymm.nnnnn
   the arxiv number.
2. nnnnn
   omit the current year and month.
   or, further, nnnn for 0nnnn, nnn for 00nnn, nn for 000nn.
3. http(s)://arxiv.org/pdf/yymm.nnnnn(.pdf)
   if you copied it from the arxiv website.
''')




def namer(arxivNo):
    if diag_mode:
        print('diag_mode:','checking out name of ',arxivNo,end='')
        
    path='https://www.arxiv.org/abs/'+arxivNo
    #path= "http://export.arxiv.org/api/query?search_query=all:"+arxivNo
    #print ( "----------------------------------------")
    #print ("looking up:", path)
    #page=urllib.urlopen(path)
    try:
        data=urllib.request.urlopen(path)
        #data=urllib.urlopen(path).read()
    except Exception as e:

        print( 'net error')
        print( str(Exception))
        print( str(e))
        winsound.Beep(1200,1200)
        print('beeped')
        return ''

    begins= False

    try:
        for line in data:
            #print (">>",line)
            line=line.decode("utf-8")
            if line.find('<title>') >=0:
                res=line
                break
    except Exception as e:
        print ('net error')
        print (str(e))
        return ""

    #res=beginner
    #print( "res = ", res)

    while True:
        if len(res)<=1:
            return res
        else:
            if res[0]==' ':
                res=res[1:]
            else:
                break
    finish_flag = False

    while (not finish_flag) and (len(res)>0):
        if res[:7]=='<title>':
            res=res[7:]

        if ord(res[0]) in range(48,58) or res[0] in ['.','v','[',' ']:
            #res[0] =0,1,..9
            res=res[1:]
        if res[0]==']':
            res=res[1:]
            finish_flag=True
    if res.find('</title>') >=0:
        res=res[:-8]
    illegal='\/:*?"<>|'    #illegal chars to remove
    for ichar in illegal:
        res  = res.replace(ichar, '_')
    while res[-1] in ' _':
        res=res[:-1]
    if diag_mode:
        print('diag_mode:','namer res=',res)
    return res  #which is the name.



def Schedule(a,b,c):
    '''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
    '''
    per = 100.0 * a * b / c
 
    #print('chunks=',a, 'progress={0}%'.format(per))
    if a==0:
        if diag_mode:
            print('diag_mode:','schedule starting at',a,b,c)
            
        if c>1000000:
            sizestr='{0:.2f} MB'.format(c/1000000) 
        else:
            sizestr='{0:.2f} KB'.format(c/1000)
        if diag_mode:
            print('diag_mode:','str=',sizestr)
            
        print("#chunks={0}, file size={1}".format(math.ceil(c/b), sizestr))
    elif a%10==0:
        print(' ')
        
    print('#',end='')


def oncall():    
    target=input('\n \nEnter arXiv target:')

    target=target.lstrip().rstrip()
    if target=='':
        print ('Enter ''e'' to exit.')
        return 0
    
    if target in ['f','F']:
        find_name_flag=False
        print('find name flag OFF.')
    elif target in ['t','T']:
        find_name_flag=True
        print('find name flag ON.')
    elif len(target)==1:
        return 1
    
    [url,filename]=determine_url(target)
    downloader(url,filename)    
    return 0

def determine_url(name):
    if diag_mode:
            print('diag_mode:','determine url via name=',name)
            
    std=len("http://arxiv.org/pdf/")

    url='null_url'
    filename="null_name"
    
    if len(name)<=5:
        if [char in '0123456789' for char in name]:
            if diag_mode:
                print('diag_mode:','determine path a')
            name='0'*(5-len(name))+name
            curtime=time.localtime()
            curyear=str(curtime.tm_year)[-2:]
            curmon= '{0:0>2}'.format(curtime.tm_mon)
            #print(curyear,curmon)
            name= curyear+curmon+'.'+name

            
    if len(name)>=std+4:
        if diag_mode:
            print('diag_mode:','determine path b')
        s1="http://arxiv.org/pdf/"
        s2="https://arxiv.org/pdf/"
        if name[:len(s1)]==s1:
            filename=name[len(s1):]
        elif name[:len(s2)]==s2:
            filename=name[len(s2):]
        
        url=name
        #filename=name[std:]
        if not filename[-4:]=='.pdf':
            filename=filename+'.pdf' 
    elif all(char in '0123456789v.' for char in name):
        if diag_mode:
            print('diag_mode:','determine path c')
        url = 'https://arxiv.org/pdf/'+name
        filename=name+'.pdf'
    else:
        print('buggy url=',name)
        return ['','']
        
    print("url:",url)

    if diag_mode:
        print('diag_mode: ',"file name:",filename)

    if filename[-4:]=='.pdf':
        arxivNo=filename[:-4]
    else:
        arxivNo=filename
        
    if find_name_flag==True:
        arxivName=' '+namer(arxivNo)        
        print(arxivName)
    else:
        arxivName=''         

    if diag_mode:
        print('diag_mode:','downloader:',url, arxivName)
        
    return [url, arxivNo+arxivName+'.pdf']
    

def downloader(url,filename):
    try:
        #print('downloading',url)
        filename=os.path.join('C:\\downloads\\',filename)
        urllib.request.urlretrieve(url, filename ,Schedule)
    except Exception as e:
        print(e)
        return -1
    return 0



if __name__=='__main__':
    res=0
    while res==0:
        res=oncall()
        
