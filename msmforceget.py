#-*-coding:utf-8-*-
#!/usr/bin/python
#test_find-and-copy-file.py


import os,re,math

T0 = 288.15
mu0 = 1.7894e-5
p0 = 1.013e5
Rg = 287

def T2MA(T):
  g_mu = (T/T0)**1.5*(T0+110.4)/(T+110.4)
  mu  = g_mu  * mu0
  a   = (1.4*287.14*T)**0.5
  print ("%8f %8f %8f %8f %8f %8f\n"%(roe, a, mu, 0, p, T))
  return roe, mu, a
  
def ReTMa2P(Re,T,mach):
  g_mu = (T/T0)**1.5*(T0+110.4)/(T+110.4)
  mu  = g_mu  * mu0
  a   = (1.4*287.14*T)**0.5
  v   = mach*a
  roe = Re/v*mu
  p   = roe*Rg*T

def pt2RMA(p,T):
  roe = p/Rg/T
  g_mu = (T/T0)**1.5*(T0+110.4)/(T+110.4)
  mu  = g_mu  * mu0
  a   = (1.4*287.14*T)**0.5
  print ("%8f %8f %.3e %8f %.3e %8f\n"%(roe, a, mu, 0, p, T))
  return roe, mu, a
  
def haiba2TP(haiba):
  if (haiba<11000.):
    T = T0 - haiba/1000.*6.5
  elif (haiba<20000.):
    T = 216.65
  else:
    T = 216.65 + (haiba-20000.)/1000.
  if (haiba<11000.):
    g_p   = g_roe**1.235
  else:
    g_p   = 0.752*g_roe
  p   = g_p   * p0
  print ("%8f %8f %8f\n"%(haiba, T, p))
  return T, p

def input2par(infile):
  with open(infile,'r') as fin:
    while 1:
      line = fin.readline()
      if re.search('IncomingType',line):
        IncomingType = float(fin.readline().split()[0])
      if re.search('p_bar',line):
                print(line)
        numlst = list(map(float, fin.readline().split()))
        renold = numlst[0]
        T      = numlst[1]
        p_bar  = numlst[2]
        altitu = numlst[3]*1000
                print(numlst)
        if IncomingType == 1:
          p_bar = ReT2P(renold, T)
          print ("Need new code for IncomingType=1 !")
          exit()
        elif IncomingType == 3:
          T, p_bar = haiba2TP(altitu)
        roe,mu,a = pt2RMA(p_bar, T)
      if re.search('R-mach',line):
        numlst = list(map(float, fin.readline().split()))
                print(numlst)
        mach = numlst[0]
        alph = numlst[1]
        beta = numlst[2]
        #strlst = fin.readline().split()
        fname = "Beita%s_Mach%s.plt"%(str(numlst[2]+0.0001)[:4],str(numlst[0]+0.0001)[:4])
                print(fname)
#      if re.search('length_ref',line):
#        for ii in range(1,4):
#          if ii==3:
#            print ("Not find 'area_ref' in '%s'"%line)
#            exit()
#          elif re.search('area_ref',line.split()[ii]):
#            isref = ii
#            break
#        numlst = list(map(float, fin.readline().split()))
#        print numlst
#        lref = numlst[0]
#        sref = numlst[isref]
      if re.search('BC n_patch',line):
        break
#  renold = roe*mach*a*lref/mu
  renold = roe*mach*a/mu
  v = mach*a
#  ps = 0.5*roe*v*v*sref
  return fname, renold, v, alph, roe

####   START   #######
#fname, renold, ps = input2par('input.par')
#print("%s %e %e"%(fname, renold,ps))
tmplst = input2par('input.par')
print(tmplst)
outname = tmplst[0]
v   = tmplst[2]
alph = tmplst[3]
roe  = tmplst[4]

fname0 = 'TSQSMS_origin0.dat'
fname1 = 'TSQSMS_origin1.dat'

workpath = (os.popen("pwd").read())
print (workpath)

dirs = []
beg = 0
iread = 0
with open('forceget.par','r') as fr:
  for sstr in fr:
    if re.search('bllength_refout',sstr):
      iread = 1
    elif iread==1:
      numlst = list(map(float, sstr.split()))
            print(numlst)
      lref = numlst[0]
      bref = numlst[1]
      sref = numlst[2]
      iread = 0
    if beg==1 and sstr[0]!='#':
      dirs.append(sstr[:-1].replace('\r',''))
    if re.search('Dirname',sstr):
      beg = 1
print (dirs)

ps = 0.5*roe*v*v*sref

fs0=[]
for path in dirs:
  ff = os.path.join(path,fname0)
  if os.path.isfile(ff):
    fs0.append(ff)
if len(fs0) == 0:
  print ("%s is not exist"%fname0)
  exit()

msm = []
for ff in fs0:
  ss = os.popen("tail %s"%ff).readlines()
  f6 = ss[-1].split()
  ff6 = [0]
  for i in range(1,len(f6)):
    if i<4:
      ff6.append(-float(f6[i])/ps)
    if i==4 or i==6:
      ff6.append(-float(f6[i])/ps/bref)
    elif i==5:
      ff6.append(-float(f6[i])/ps/lref)
  
  print(ff)
  alph = alph * math.pi/180
  drag = ff6[1]*math.cos(alph)+ff6[3]*math.sin(alph)
  lift =-ff6[1]*math.sin(alph)+ff6[3]*math.cos(alph)
    wstr = '1  0.103  %.3f 0 %f %f 0 0 %f %f %f %f %f %f\n' % (
        alph, lift, drag, ff6[1], ff6[2], ff6[3], -ff6[4], ff6[5], -ff6[6])
  msm.append(wstr)

title1 = r'VARIABLES =  "Step"  "Mach"  "<greek>a</greek>"  "<greek>b</greek>"  "C<sub>L</sub>"  "C<sub>D</sub>"  "C<sub>dp</sub>"  "C<sub>dv</sub>"  "C<sub>A</sub>"  "C<sub>Y</sub>"  "C<sub>Nor</sub>"  "C<sub>mx</sub>"  "C<sub>m</sub>"  "C<sub>n</sub>" '
title2 = r'zone T= "<greek>b</greek>=0.00_ma=0.10"'

os.popen("mkdir Force")
os.popen("mkdir Force/MSMPL")
outf = "Force/MSMPL/" + outname
with open(outf,'w') as fw:
  fw.write("%s\n"%title1)
  fw.write("%s\n"%title2)
  fw.writelines(msm)
print (os.popen("cat %s"%outf).read())

fs1=[]
for path in dirs:
  ff = os.path.join(path,fname1)
  if os.path.isfile(ff):
    fs1.append(ff)
    print (ff)
if len(fs1) == 0:
  print ("%s is not exist"%fname1)
#  exit()

msm = []
for ff in fs1:
  ss = os.popen("tail %s"%ff).readlines()
  f6 = ss[-1].split()
  ff6 = [0]
  for i in range(1,len(f6)):
    if i<4:
      ff6.append(-float(f6[i])/ps)
    if i==4 or i==6:
      ff6.append(-float(f6[i])/ps/bref)
    elif i==5:
      ff6.append(-float(f6[i])/ps/lref)
      
  alph = alph * math.pi/180
  drag = ff6[1]*math.cos(alph)+ff6[3]*math.sin(alph)
  lift =-ff6[1]*math.sin(alph)+ff6[3]*math.cos(alph)
    wstr = '1  0.103  %.3f 0 %f %f 0 0 %f %f %f %f %f %f\n' % (
        alph, lift, drag, ff6[1], ff6[2], ff6[3], -ff6[4], ff6[5], -ff6[6])
  msm.append(wstr)

os.popen("mkdir Force/MSMPR")
outf = "Force/MSMPR/" + outname
with open(outf,'w') as fw:
  fw.write("%s\n"%title1)
  fw.write("%s\n"%title2)
  fw.writelines(msm)
print (os.popen("cat %s"%outf).read())


exit()

