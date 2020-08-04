import os, re, math, sys


def delete_tail(ln):
    return ln.replace('\n', '').replace('\r', '')


def TDFmt_check(infile):
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

    CheCi = infile[:8]
    print(CheCi)
    with open(infile, 'r') as fin0:
        while 1:
            line = fin0.readline()
            lnlst = line.split()
            # print (lnlst)
            if (lnlst[0] == '#'):
                if (len(lnlst) > 1 and lnlst[1] == 'FIN'):
                    break
                if (len(lnlst) > 1 and lnlst[1] == 'prefix_outfile(quanji)'):
                    prefix_out = delete_tail(fin0.readline())
                    print(prefix_out)
                if (len(lnlst) > 1 and lnlst[1] == 'postfix_outfile'):
                    postfix = delete_tail(fin0.readline())
                    print(postfix)
                if (len(lnlst) > 1 and lnlst[1] == 'prefix_inputfile'):
                    prefix_in = delete_tail(fin0.readline())
                    print(prefix_in)
                if (len(lnlst) > 1 and lnlst[1] == 'filename_input'):
                    infilename = delete_tail(fin0.readline())
                    print(infilename)
                if (len(lnlst) > 1 and lnlst[1] == 'n_outfile'):
                    n_outfile = int(delete_tail(fin0.readline()))
                    print(n_outfile)
                if (len(lnlst) > 1 and lnlst[1] == 'name_outfile'):
                    bujian = []
                    for i in range(n_outfile):
                        bujian.append(fin0.readline().split()[0])
                        if (bujian[i][0] == '#'):
                            print("Error n_outfile! too big?")
                            exit()

    print('\n read %s over\n' % infile)
    print(bujian)

    qjfile = prefix_out + CheCi + '.dat'
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
        print("   %3d   %8.4e   %8.4e   %8.4e   %8.4e   %8.4e   %8.4e   %8.4e   %8.4e" \
              % (alph[-1], cl[-1], cd0[-1], cm[-1], cnor[-1], ca[-1], cy[-1], cn[-1], cmx[-1]))

    for ibj in range(len(bujian)):
        bjfile = prefix_out + CheCi + bujian[ibj] + '.dat'
        if not os.path.isfile(bjfile):
            # print ("%s is not a file"%bjfile)
            continue
        # print (bjfile)
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
          % (infile, examlist.index(min(examlist)), min(examlist), examlist.index(max(examlist)), max(examlist)))


def TDFmt_check0(totalfile):
    totpar = []
    with open(totalfile, 'r') as ftot:
        for line in ftot:
            if re.search("#Fin", line):
                break
            print(line)
            totpar.append(line[:-1].replace('\r', ''))

    print(totpar)
    for kk in range(len(totpar)):
        TDFmt_check(totpar[kk])


if __name__ == '__main__':
    if len(sys.argv) == 1:
        TDFmt_check0('total.in')
    elif len(sys.argv) == 2:
        infile = sys.argv[1]
        TDFmt_check(infile)

print("\n Hello World")
exit()
