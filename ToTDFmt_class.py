import os, re, math, sys


def delete_tail(ln):
    return ln.replace('\n', '').replace('\r', '')


class TDDataConverter:
    def __init__(self):
        self.specialname()
        self.parameter = {self.snhalfm: -1, self.snprefi: 'TTTT', self.sncheci: '0000', self.snaltit: 0,
                          self.snlengt: 1.0, self.snruddl: '0 0 0 0 0', self.snorgfo: './',
                          self.snpltna: '', self.snorgNp: 1, self.snorgpa: ['quanji'],
                          self.snoutfo: './TDFormat/', self.snoutNA: 1, self.snoutAs: ['QJ'],
                          self.snoutPa: [['quanji']], self.snoutpo: '.dat'}

    def specialname(self):
        self.snhalfm = 'halfmodel'
        self.snprefi = 'prefix'
        self.sncheci = 'checi'
        self.snaltit = 'altitude'
        self.snlengt = 'length'
        self.snruddl = 'ruddleangle'
        self.snorgfo = 'orgfolder'
        self.snpltna = 'pltname'
        self.snorgNp = 'orgNpart'
        self.snorgpa = 'orgpartnames'
        self.snoutfo = 'outfolder'
        self.snoutNA = 'outNAssem'
        self.snoutAs = 'outAssemName'
        self.snoutPa = 'outPartNames'
        self.snoutpo = 'outpostfix'

    def run(self, infile):
        self.readparameter(infile)
        self.show()
        self.ToTDFmt()
        self.TDFmt_check(infile)
        if self.parameter[self.snhalfm]:
            self.QJ_postdeal()

    def updatebyname(self, name, value):
        self.parameter[name] = value

    def show(self):
        for k, v in self.parameter.items():
            print(k, " = ", v)
        # print(self.parameter.items())

    def getvalue(self):
        return self.parameter[self.snprefi], self.parameter[self.sncheci], self.parameter[self.snaltit], \
               self.parameter[self.snlengt], self.parameter[self.snruddl], self.parameter[self.snorgfo], \
               self.parameter[self.snpltna], self.parameter[self.snorgNp], self.parameter[self.snorgpa], \
               self.parameter[self.snoutfo], self.parameter[self.snoutNA], self.parameter[self.snoutAs], \
               self.parameter[self.snoutPa], self.parameter[self.snoutpo]

    def readparameter(self, infile):
        self.updatebyname(self.snprefi, infile[-11:-7])
        self.updatebyname(self.sncheci, infile[-7:-3])

        with open(infile, 'r') as fin0:
            while 1:
                line = fin0.readline()
                lnlst = line.split()
                # print(lnlst)
                if (lnlst[0] == '#'):
                    # print(line)
                    if (len(lnlst) > 1 and lnlst[1] == self.snhalfm):
                        halfmodel = bool(delete_tail(fin0.readline()))
                        self.updatebyname(self.snhalfm, halfmodel)
                    elif (len(lnlst) > 1 and lnlst[1] == self.snaltit):
                        altiline = delete_tail(fin0.readline())
                        highlist = altiline.split()
                        self.updatebyname(self.snaltit, float(highlist[0]))
                        self.updatebyname(self.snlengt, float(highlist[-1]))
                    elif (len(lnlst) > 1 and lnlst[1] == 'df'):
                        dfline = delete_tail(fin0.readline())
                        self.updatebyname(self.snruddl, dfline)
                    elif (len(lnlst) > 1 and lnlst[1] == self.snoutfo):
                        outfolder = delete_tail(fin0.readline())
                        self.updatebyname(self.snoutfo, outfolder)
                    elif (len(lnlst) > 1 and lnlst[1] == self.snorgfo):
                        orgfolder = delete_tail(fin0.readline())
                        self.updatebyname(self.snorgfo, orgfolder)
                    elif (len(lnlst) > 1 and lnlst[1] == self.snpltna):
                        pltname = delete_tail(fin0.readline())
                        self.updatebyname(self.snpltna, pltname)
                    elif (len(lnlst) > 1 and lnlst[1] == 'name_outfile'):
                        namelines = []
                        while True:
                            nameline = delete_tail(fin0.readline())
                            if (nameline[:5] == '# FIN'):
                                break
                            elif nameline.strip() == '':
                                continue
                            elif (nameline[0] == '#'):
                                print("Error end of file!")
                                exit()
                            else:
                                namelines.append(nameline)
                        break

                else:
                    print("Error Format: %s " % infile)
                    exit()

        print('\n read %s over\n' % infile)

        self.updatebyname(self.snoutNA, len(namelines))
        if namelines[0].split()[0] == "QJ":
            quanjiname = namelines[0].split()[1]
        else:
            exit("错误：第一个输出部件必须是‘QJ'")
        if not self.parameter[self.snpltna]:
            for ffile in os.listdir(os.path.join(orgfolder, quanjiname)):
                if os.path.splitext(ffile)[1] == '.plt':
                    self.updatebyname(self.snpltna, ffile)
                    break

        self.updatebyname(self.snoutNA, len(namelines))
        outAssemNames = []
        outPartNames = []
        for nameline in namelines:
            namestr = nameline.split()
            outAssemNames.append(namestr[0])

            if (len(namestr) < 2):
                print('error !!! nrfile isnot right')
                exit()
            outPartName = []
            for partname in namestr[1:]:
                outPartName.append(partname)
            outPartNames.append(outPartName)

        self.updatebyname(self.snoutAs, outAssemNames)
        self.updatebyname(self.snoutPa, outPartNames)
        self.updatebyname(self.snorgpa, os.listdir(orgfolder))
        self.updatebyname(self.snorgNp, len(os.listdir(orgfolder)))

    def PnTByFormula(self):
        T0 = 288.15
        p0 = 101325.2
        altitude = 0.001 * self.parameter[self.snaltit]

        H = altitude / (1. + altitude / 6.356766e3)
        if altitude < 11.0191:
            W = 1. - H / 44.3308
            T = T0 * W
            g_p = W ** 5.2559
        elif altitude < 20.0631:
            W = math.e ** ((14.9647 - H) / 6.3416)
            T = 216.65
            g_p = 0.11953 * W
        elif altitude < 32.1619:
            W = 1 + (H - 24.9021) / 221.552
            T = 221.552 * W
            g_p = 2.5158e-2 * W ** (-34.1629)
        elif altitude < 47.3501:
            W = 1 + (H - 39.7499) / 89.4107
            T = 250.350 * W
            g_p = 2.8338e-3 * W ** (-12.2011)
        elif altitude < 51.4125:
            W = math.e ** ((48.6252 - H) / 7.9223)
            T = 270.650
            g_p = 8.9155e-4 * W
        elif altitude < 71.8020:
            W = 1 - (H - 59.4390) / 88.2218
            T = 247.021 * W
            g_p = 2.1671e-4 * W ** 12.2011
        elif altitude < 86.0000:
            W = 1 - (H - 78.0303) / 100.2950
            T = 200.590 * W
            g_p = 1.2274e-5 * W ** 17.0016
        elif altitude < 91.0000:
            W = math.e ** ((87.2848 - H) / 5.4700)
            T = 186.870
            g_p = (2.2730 + 1.042e-3 * H) * e - 4 * W
        else:
            print("altitude should be in 0--91 Km !")
            exit()

        p = g_p * p0

        return p, T

    def ToTDFmt(self):

        dfstr = self.parameter[self.snruddl].split()

        np = 13

        p, T = self.PnTByFormula()
        a = math.sqrt(1.4 * 287. * T)
        roe = p / T / 287.
        mu0 = 1.7894e-5
        mu = mu0 * math.pow(T / 288.15, 1.5) * (288.15 + 110.4) / (T + 110.4)
        print("%8f %8f %8f %8f %8f %8f %8f\n" % (self.parameter[self.snaltit], roe, a, mu,
                                                 self.parameter[self.snlengt], p, T))

        for i in range(self.parameter[self.snoutNA]):
            if i == 0:
                wfile = self.parameter[self.snoutfo] + self.parameter[self.snprefi] + \
                        self.parameter[self.sncheci] + self.parameter[self.snoutpo]
            else:
                wfile = self.parameter[self.snoutfo] + self.parameter[self.snprefi] + \
                        self.parameter[self.sncheci] + self.parameter[self.snoutAs][i] + \
                        self.parameter[self.snoutpo]
            print(wfile)

            rfile = []
            for j in range(len(self.parameter[self.snoutPa][i])):
                rfile.append(os.path.join(self.parameter[self.snorgfo],
                                          self.parameter[self.snoutPa][i][j] + os.sep +
                                          self.parameter[self.snpltna]))
                print(rfile[j])

            ma = []
            alph = []
            beta = []
            cl = []
            cd0 = []
            tt = []
            ca = []
            cy = []
            cnor = []
            Crol = []
            cm = []
            cn = []
            try:
                with open(rfile[0], 'r') as fr0:
                    lns = fr0.readlines()
            except:
                print("error! open to read file: %s" % rfile[0])
                exit(3)
            nw = len(lns)
            if lns[0].split()[-1].replace('"', '') == 'C<sub>n</sub>':
                moment = 1
            else:
                moment = -1
            for jr in range(2, nw):
                tmpstr = lns[jr].split()
                if len(tmpstr) == 13:
                    tmpstr.insert(0, '1')
                numlst = list(map(float, tmpstr))
                ma.append(numlst[1])
                alph.append(numlst[2])
                beta.append(numlst[3])
                cl.append(numlst[4])
                cd0.append(numlst[5])
                tt.append(numlst[6])
                tt.append(numlst[7])
                ca.append(numlst[8])
                cy.append(numlst[9])
                cnor.append(numlst[10])
                Crol.append(numlst[11] * moment)
                cm.append(numlst[12])
                cn.append(numlst[13] * moment)

            for ir in range(1, len(self.parameter[self.snoutPa][i])):
                print(rfile[ir])
                with open(rfile[ir], 'r') as fr0:
                    lns = fr0.readlines()
                nw2 = len(lns)
                print(nw2)
                if (not nw2 == nw):
                    print("nw2!=nw")
                    exit()
                for jr in range(2, nw):
                    print(lns[jr])
                    tmpstr = lns[jr].split()
                    if len(tmpstr) == 13:
                        tmpstr.insert(0, '1')
                    numlst = list(map(float, tmpstr))
                    dma = numlst[1] - ma[jr - 2]
                    dalph = numlst[2] - alph[jr - 2]
                    dbeta = numlst[3] - beta[jr - 2]
                    if (dma > 0.1 or dma < -0.1 or dalph > 0.1 or dalph < -0.1 or
                            dbeta > 0.1 or dbeta < -0.1):
                        print("error input date: %s %d" % (rfile[ir], jr))
                        exit()
                    cl[jr - 2] += numlst[4]
                    cd0[jr - 2] += numlst[5]
                    tt[jr - 2] += numlst[6]
                    tt[jr - 2] += numlst[7]
                    ca[jr - 2] += numlst[8]
                    cy[jr - 2] += numlst[9]
                    cnor[jr - 2] += numlst[10]
                    Crol[jr - 2] += numlst[11] * moment
                    cm[jr - 2] += numlst[12]
                    cn[jr - 2] += numlst[13] * moment

            u = ma[0] * a
            ren = roe * u * self.parameter[self.snlengt] / mu
            q = 0.5 * roe * u * u
            print("ma=%f  re=%e  q=%f \n" % (ma[0], ren, q))

            with open(wfile, 'w') as fwrt:
                fwrt.write(" %6s %6d %6d %6d %6s %6s %6s %6s %6s\n" % (
                    self.parameter[self.sncheci], nw - 2, np, beta[0], dfstr[0],
                    dfstr[1], dfstr[2], dfstr[3], dfstr[4]))
                for jr in range(nw - 2):
                    fwrt.write("%10.5f%10.5f%10.5f%10.5f%10.5f%10.5f%10.5f%10.5f"
                               "%10.5f%10.5f%10.5f%11.3e%11.3e\n"
                               % (alph[jr], ma[jr], cl[jr], cd0[jr], cm[jr], cnor[jr],
                                  ca[jr], cy[jr], cn[jr], Crol[jr], beta[jr], q, ren))

        print("\n GoodLuck ! \n")

    def TDFmt_check(self, infile):
        ma = []
        alph = []
        beta = []
        cl = []
        cd0 = []
        q = []
        ren = []
        ca = []
        cy = []
        cnor = []
        cmx = []
        cm = []
        cn = []

        print(self.parameter[self.sncheci])
        qjfile = self.parameter[self.snoutfo] + self.parameter[self.snprefi] + \
                 self.parameter[self.sncheci] + self.parameter[self.snoutpo]
        if not os.path.isfile(qjfile):
            print("%s is not a file" % qjfile)
            exit()
        with open(qjfile, 'r') as fin0:
            lns = fin0.readlines()
        nw = len(lns)
        print("\nAlpha Cl  Cd   Cm   Cnor   Ca/Cx   Cy   Cn/-Cmz   Crol/-Cmx")
        for iw in range(1, nw):
            tmpstr = lns[iw].split()
            numlst = list(map(float, tmpstr))
            #    if (iw==1):
            #      print (numlst)
            #        %(alph[jr],ma[jr],cl[jr],cd0[jr],cm[jr],cnor[jr],ca[jr],cy[jr],cn[jr],cmx[jr],beta[jr],q,ren))
            alph.append(numlst[0])
            ma.append(numlst[1])
            cl.append(numlst[2])
            cd0.append(numlst[3])
            cm.append(numlst[4])
            cnor.append(numlst[5])
            ca.append(numlst[6])
            cy.append(numlst[7])
            cn.append(numlst[8])
            cmx.append(numlst[9])
            beta.append(numlst[10])
            q.append(numlst[11])
            ren.append(numlst[12])
            print("   %3d   %8.4e   %8.4e   %8.4e   %8.4e   %8.4e   %8.4e   %8.4e   %8.4e"
                  % (alph[-1], cl[-1], cd0[-1], cm[-1], cnor[-1], ca[-1], cy[-1], cn[-1], cmx[-1]))

        for ibj in range(len(self.parameter[self.snoutAs])):
            bjfile = self.parameter[self.snoutfo] + self.parameter[self.snprefi] + \
                     self.parameter[self.sncheci] + self.parameter[self.snoutAs][ibj] + \
                     self.parameter[self.snoutpo]
            if not os.path.isfile(bjfile):
                # print ("%s is not a file"%bjfile)
                continue
            with open(bjfile, 'r') as fin0:
                lns = fin0.readlines()
            if not nw == len(lns):
                print("nw != len(lns) %s !" % bjfile)
                exit()
            for iw in range(1, nw):
                iwd = iw - 1
                tmpstr = lns[iw].split()
                numlst = list(map(float, tmpstr))
                if (alph[iwd] != numlst[0] or ma[iwd] != numlst[1] or beta[iwd] != numlst[10]):
                    print("error: alph or ma or beta, %s %d" % (bjfile, iwd))
                    exit()
                cl[iwd] -= numlst[2]
                cd0[iwd] -= numlst[3]
                cm[iwd] -= numlst[4]
                cnor[iwd] -= numlst[5]
                ca[iwd] -= numlst[6]
                cy[iwd] -= numlst[7]
                cn[iwd] -= numlst[8]
                cmx[iwd] -= numlst[9]
        print("\n\nDelta:  Cl  Cd   Cm   Cnor   Ca/Cx   Cy   Cn/-Cmz   Crol/-Cmx")
        for i in range(nw - 1):
            print("   %8.4e   %8.4e   %8.4e   %8.4e   %8.4e   %8.4e   %8.4e   %8.4e" \
                  % (cl[i], cd0[i], cm[i], cnor[i], ca[i], cy[i], cn[i], cmx[i]))
        examlist = cl + cd0 + cm + cnor + ca + cy + cn + cmx
        print("\n%s examlist: %3d %8.3e %3d %8.3e"
              % (
                  self.parameter[self.sncheci], examlist.index(min(examlist)), min(examlist),
                  examlist.index(max(examlist)),
                  max(examlist)))

        logfile = infile.split('.')[0] + '.log'
        with open(logfile, 'w') as fw:
            fw.write("Delta:  Cl  Cd   Cm   Cnor   Ca/Cx   Cy   Cn/-Cmz   Crol/-Cmx\n")
            for i in range(nw - 1):
                fw.write("   %8.4e   %8.4e   %8.4e   %8.4e   %8.4e   %8.4e   %8.4e   %8.4e\n" \
                         % (cl[i], cd0[i], cm[i], cnor[i], ca[i], cy[i], cn[i], cmx[i]))
            fw.write("---- %s examlist: %3d %8.3e %3d %8.3e\n" % (
                self.parameter[self.sncheci], examlist.index(min(examlist)), min(examlist),
                examlist.index(max(examlist)), max(examlist)))

    def QJ_postdeal(self):
        fname = os.path.join(self.parameter[self.snoutfo], self.parameter[self.snprefi] + \
                             self.parameter[self.sncheci] + self.parameter[self.snoutpo])
        with open(fname, 'r') as fr:
            lns = fr.readlines()
        # shutil.move(fname, self.parameter[self.snoutfo]+'..'+os.sep)

        with open(fname, 'w') as fw:
            fw.write(lns[0])
            for i in range(1, len(lns)):
                numlst = list(map(float, lns[i].split()))
                for j in range(2, 7):
                    numlst[j] *= 2.0
                for j in range(7, 10):
                    numlst[j] = 0.0
                for j in range(len(numlst) - 2):
                    fw.write("%10.5f" % numlst[j])
                for j in range(len(numlst) - 2, len(numlst)):
                    fw.write("%11.3e" % numlst[j])
                fw.write("\n")


def ToTDFmt_f():
    if len(sys.argv) == 1:
        totalfile = 'total.in'
    elif len(sys.argv) == 2:
        totalfile = sys.argv[1]

    totpar = []
    with open(totalfile, 'r') as ftot:
        for line in ftot:
            if re.search("#Fin", line):
                break
            elif line[0] == '#':
                pass
            else:
                print(line)
                totpar.append(line[:-1].replace('\r', ''))

    print(totpar)
    for kk in range(len(totpar)):
        case = TDDataConverter()
        case.run(totpar[kk])


if __name__ == '__main__':
    ToTDFmt_f()
    print("\n Hello World")
    exit()
