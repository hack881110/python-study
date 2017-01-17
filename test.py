# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import sys
import os
import os.path
import codecs

#reload(sys)  
#sys.setdefaultencoding('utf8')



baseurl= 'http://www.liaoxuefeng.com'

url = 'http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'

d=dict()

basepath=os.path.abspath('.')

def create_dir(dirname):
   
    abspath=os.path.normcase(basepath)
    print abspath
    
    path=os.path.join(abspath,dirname)
    print dirname
    print path
    if os.path.exists(path)==False:
        os.makedirs(path)
    return path


def get_content(u_url):
    try:
        request = urllib2.Request(u_url)
        response = urllib2.urlopen(request)
        content = response.read().decode('utf-8')

        pattern = re.compile('<h4>(.*?)</h4>.*?<div class="x-wiki-info"><span>(.*?)</span></div>.*?<div class="x-wiki-content">(.*?)</div>',re.S)
        items = re.findall(pattern,content)
        for  i  in  items:
            print  i[0],i[1],i[2]
        return i[2]
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
            

def  write_to_file(filename,content):

        f = codecs.open(filename+".md", 'w','utf-8-sig')
        f.write(content)
        f.close()


s_str=""
def  change_link(content):
    try:
        pattern = re.compile('<p><img src="(.*?)" alt=".*?"></p>',re.S)
        items = re.findall(pattern,content)
        for i in items:
            s_str=i;
            d_str=".."+s_str+".jpg"
            content=content.replace(s_str,d_str)
        return  content
    except urllib2.URLError, e:
            if hasattr(e,"code"):
                print e.code
            if hasattr(e,"reason"):
                print e.reason



     

def  get_picture(content):
    try:
        pattern = re.compile('<p><img src="(.*?)" alt=".*?"></p>',re.S)
        items = re.findall(pattern,content)
        for i in items:
            #path=os.path.abspath(i)
            #filename= os.path.basename(i)
            p,filename=os.path.split(i)
            pdir=p.replace('/','\\')
            path=basepath+pdir
            if os.path.exists(path)==False:
                os.makedirs(path)

            picurl=baseurl+i
            idir=i.replace('/','\\')
            picname=basepath+i+'.jpg'
            print picname
            conn=  urllib.urlopen(picurl)
            f=open(picname,'wb')
            f.write(conn.read())
            f.close()
            print "pic save"
    except urllib2.URLError, e:
            if hasattr(e,"code"):
                print e.code
            if hasattr(e,"reason"):
                print e.reason

fobj= codecs.open("SUMMARY.md",'w+','utf-8-sig')

def  do_work(url):

    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        content = response.read().decode('utf-8')
        print  "Read file....."

        pattern = re.compile('<li id=.*? style="(.*?)">.*?<a href="(.*?)">(.*?)</a>',re.S)
        items = re.findall(pattern,content)
        print  "Find file....."
        fileName1=""
        for  i  in  items:
            print i[0],i[1],i[2]
            if  "1em"  in i[0]:
                print  "working ..."
                fileName1 = re.sub('[\/:*?"<>|]','-',i[2])
                path=create_dir(fileName1)
                fobj.write("* [%s](%s/%s.md)\n" %(fileName1,fileName1,fileName1))
               # fobj.next()
                fobj.flush()
         
             
                os.chdir(path)
                url=baseurl+i[1]
                content=get_content(url)
                get_picture(content)
                content=change_link(content)
                write_to_file(fileName1,content)
                
            else:
                print  "hard working ..."
                fileName = re.sub('[\/:*?"<>|]','-',i[2])
                fobj.write("   * [%s](%s/%s.md)\n" %(fileName,fileName1,fileName))
                #fobj.next()
                fobj.flush()
              
                url=baseurl+i[1]
                content=get_content(url)
                get_picture(content)
                content=change_link(content)
                write_to_file(fileName,content)
                
       
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason

    fobj.close()
    print "work success..."
    sys.exit()


if  __name__ == "__main__":
    print "start...."
    do_work(url)
