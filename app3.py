#! /usr/bin/python

def generate_html_pie(suc,spam,spoof):
 with open("pie","rb") as f:
  pie=f.read()
 final_pie=pie.replace("spam_calls",str(spam))
 final_pie=final_pie.replace("spoof_calls",str(spoof))
 final_pie=final_pie.replace("genuine_calls",str(suc))
 with open("index.html","wb") as f:
  f.write(final_pie)

def contact(number):
 with open("contacts","rb") as f:
  for i in f:
   if i.split()[0]==number:
    return i.split()[1]
    break
  else: return("unknown")

def gentable(index,num,day,time):
# print index,num,day,time
 a="<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n"%(index+1,num,contact(num),day,time)
 return a

def generate_html_calllog(loglist):
 tableentry=""
 with open("table","rb") as f:
  table=f.read()
 loglist.reverse()
 for i in enumerate(loglist):
  log=i[1].split()
  tableentry=gentable(i[0],log[0],log[2]+log[3]+log[4],log[5])+tableentry
 content=table.replace("table_write",tableentry)
 with open("index.html","ab+") as f:
  f.write(content)

def generate_dict(list):
 dict={}
 a=[i.split()[2] for i in list]
 for i in sorted(set(a)):
  dict[i]=a.count(i)
 return dict

def datelist(list):
 a=[i.split()[2] for i in list]
 a=map(int,a)
 return a

def maxmin(a,b,c,d):
 a=datelist(a)
 b=datelist(b)
 c=datelist(c)
 d=datelist(d)
 return max(a), min(a), max([b.count(max(b,key=b.count)),c.count(max(c,key=c.count)),d.count(max(d,key=d.count))])

def getdictvalue(dict,i):
 try:
  return dict[str(i)]
 except:
  return(0)

def generate_html_graph(list,success,spam,spoof):
 with open("graph","rb") as f:
  graph=f.read()
 final_entry=""
 max,min,maxval=maxmin(list,success,spam,spoof)
 dictsucc=generate_dict(success)
 dictspam=generate_dict(spam)
 dictspoof=generate_dict(spoof)
# print dictsucc,dictspam,dictspoof
 for i in range(min,max+1):
  entry="{\"day\": %d,\"genuine\": %d,\"spam\": %d,\"spoof\":%d },\n"%(i,getdictvalue(dictsucc,i),getdictvalue(dictspam,i),getdictvalue(dictspoof,i))
  final_entry=final_entry+entry
# print final_entry
 final_graph=graph.replace("graph_data",final_entry)
 final_graph=final_graph.replace("max_value",str(maxval+1))
 with open("index.html","ab") as fa:
  fa.write(final_graph)

def mainprog():
 success=[]
 spam=[]
 spoof=[]
 with open("calllogs","rb") as f:
  loglist=f.readlines()
 loglen=len(loglist)
 for i in loglist:
  check=i.split()
  if check[1]=="success": success.append(i)
  elif check[1]=="spam": spam.append(i)
  elif check[1]=="spoof": spoof.append(i)
 generate_html_pie(len(success),len(spam),len(spoof))
 generate_html_calllog(success)
 generate_html_graph(loglist,success,spam,spoof)
# generate_html_calllog(success)


if __name__=="__main__":
 mainprog()
