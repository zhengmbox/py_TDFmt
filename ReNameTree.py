
import os,re,math

#Start
#srcname = []
#dstname = []
srcname = [
           'PaiQiGuan_RO','MSMPR','CW','DC_L','BeiQi_L',
           'PW_L','Wing','WeiQi_L','WeiQi','PaiQiGuan_LI',
           'JS_L','Wing_L','quanji','DC','CW_L',
           'MSMPL','BeiQi','PaiQiGuan_RI','PaiQiGuan_LO','JiangGu',
           'PW','JiangGu_L','JS',
          ]
dstname = [
           'PQGOR','MSMPR','CWR','DCL','BeiQiL',
           'PWL','WingR','WeiQiL','WeiQiR','PQGIL',
           'JSL','WingL','QJ','DCR','CWL',
           'MSMPL','BeiQiR','PQGIR','PQGOL','JiangGuR',
           'PWR','JiangGuL','JSR',
          ]
  
nName = len(srcname)

if (nName!=len(dstname)):
  print ('n1!=n2',nName,len(dstname))
  for i in range(nName):
    print ('%20s %20s'%(srcname[i],dstname[i]))
  exit()

searchdir = 'Force'

print (os.popen('pwd').read())
workdir = '.'

for fpathe,dirs,fs in os.walk(workdir):
  for nowdir in dirs:
    tttstr = fpathe.split('/')
    if tttstr[len(tttstr)-1] == searchdir :
      if nowdir in dstname:
        continue
      if nowdir not in srcname:
        srcname.append(nowdir)
        dstname.append(nowdir)
      if nowdir in srcname:
        jj = srcname.index(nowdir)
        print (fpathe,nowdir,dstname[jj])
        os.rename(fpathe+'/'+nowdir,fpathe+'/'+dstname[jj])

for i in range(nName,len(srcname)):
  print ('%20s %20s'%(srcname[i],dstname[i]))
  
with open('NewName.txt','w') as fout:
  for i in range(nName,len(srcname)):
    fout.write("%20s %20s\n"%(srcname[i],dstname[i]))
  for i in range(nName,len(srcname)):
    if (i==int(i/5)*5):
      fout.write("\n           ")
    fout.write("'%s',"%srcname[i])
  fout.write("\n\n\n")
  for i in range(nName,len(dstname)):
    if (i==int(i/5)*5):
      fout.write("\n           ")
    fout.write("'%s' "%dstname[i])
print ("\n Hello World")
exit()
  
