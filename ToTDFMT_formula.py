import os, re, math, sys


def delete_tail(ln):
    return ln.replace('\n', '').replace('\r', '')


def haiba2TRPMA(haiba):
    T0 = 288.15
    roe0 = 1.226
    p0 = 1.013e5
    mu0 = 1.7894e-5
    if (haiba < 11000.):
        T = T0 - haiba / 1000. * 6.5
    elif (haiba < 20000.):
        T = 216.65
    else:
        T = 216.65 + (haiba - 20000.) / 1000.
    g_mu = (T / T0) ** 1.5 * (T0 + 110.4) / (T + 110.4)
    if (haiba < 11000.):
        g_roe = (1. - haiba / 1000. / 44.3) ** 4.253
        g_p = g_roe ** 1.235
    else:
        g_roe = 0.297 * math.e ** (-(haiba - 11000.) / 6.336)
        g_p = 0.752 * g_roe
    roe = g_roe * roe0
    p = g_p * p0
    mu = g_mu * mu0
    a = (1.4 * 287.14 * T) ** 0.5
    print("%8f %8f %8f %8f %8f %8f %8f\n" % (haiba, roe, a, mu, 0, p, T))
    return T, roe, p, mu, a


def ToTDFmt(infile):
    np = 13

    # CheCi = infile[:8]
    CheCi = infile.split('\\')[-1][4:8]
    print(CheCi)
    with open(infile, 'r') as fin0:
        while 1:
            line = fin0.readline()
            lnlst = line.split()
            print(lnlst)
            if (lnlst[0] == '#'):
                print(line)
                if (len(lnlst) > 1 and lnlst[1] == 'FIN'):
                    break
                if (len(lnlst) > 1 and lnlst[1] == 'High'):
                    highline = fin0.readline()[:-1]
                    highlist = highline.split()
                    haiba = float(highlist[0])
                    lref = float(highlist[-1])

                if (len(lnlst) > 1 and lnlst[1] == 'df'):
                    dfline = delete_tail(fin0.readline())
                    print(dfline)
                    dfstr = dfline.split()
                if (len(lnlst) > 1 and lnlst[1] == 'prefix_outfile(quanji)'):
                    prefix_out = delete_tail(fin0.readline())
                    print(prefix_out)
                    newdir = prefix_out[:prefix_out.rindex('/')]
                    os.popen("mkdir %s" % newdir)
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
                    namelines = []
                    for i in range(n_outfile):
                        namelines.append(delete_tail(fin0.readline()))
                        if (namelines[i][0] == '#'):
                            print("Error n_outfile! too big?")
                            exit()
            else:
                print("Error Format: %s " % infile)
                exit()

    print('\n read %s over\n' % infile)

    T, roe, p, mu, a = haiba2TRPMA(haiba)
    print("%8f %8f %8f %8f %8f %8f %8f\n" % (haiba, roe, a, mu, lref, p, T))

    for i in range(n_outfile):
        print(namelines[i])
        namestr = namelines[i].split()
        if i == 0:
            wfile = prefix_out + CheCi + '.' + postfix
        else:
            wfile = prefix_out + CheCi + namestr[0] + '.' + postfix
        print(wfile)

        nrfile = len(namestr) - 1
        if (nrfile < 1):
            print('error !!! nrfile isnot right')
            exit()
        rfile = []
        for j in range(1, len(namestr)):
            rfile.append(prefix_in + namestr[j] + '/' + infilename)
            print(rfile[j - 1])

        ma = []
        alph = []
        beta = []
        cl = []
        cd0 = []
        tt = []
        tt = []
        ca = []
        cy = []
        cnor = []
        Crol = []
        cm = []
        cn = []
        with open(rfile[0], 'r') as fr0:
            lns = fr0.readlines()
        nw = len(lns)
        if lns[0].split()[-1].replace('"', '') == 'C<sub>n</sub>':
            moment = 1
        else:
            moment = -1
        for jr in range(2, nw):
            tmpstr = lns[jr].split()
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

        for ir in range(1, nrfile):
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
                numlst = list(map(float, tmpstr))
                dma = numlst[1] - ma[jr - 2]
                dalph = numlst[2] - alph[jr - 2]
                dbeta = numlst[3] - beta[jr - 2]
                if (dma > 0.1 or dma < -0.1 or dalph > 0.1 or dalph < -0.1 or dbeta > 0.1 or dbeta < -0.1):
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
        ren = roe * u * lref / mu
        q = 0.5 * roe * u * u
        print("ma=%f  re=%e  q=%f \n" % (ma[0], ren, q))

        with open(wfile, 'w') as fwrt:
            fwrt.write(" %6s %6d %6d %6d %6s %6s %6s %6s %6s\n" % (
                CheCi[4:], nw - 2, np, beta[0], dfstr[0], dfstr[1], dfstr[2], dfstr[3], dfstr[4]))
            for jr in range(nw - 2):
                fwrt.write("%10.5f%10.5f%10.5f%10.5f%10.5f%10.5f%10.5f%10.5f%10.5f%10.5f%10.5f%11.3e%11.3e\n"
                           % (alph[jr], ma[jr], cl[jr], cd0[jr], cm[jr], cnor[jr], ca[jr], cy[jr], cn[jr], Crol[jr],
                              beta[jr], q, ren))

    print("\n GoodLuck ! \n")


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
            print(line)
            totpar.append(line[:-1].replace('\r', ''))

    print(totpar)
    for kk in range(len(totpar)):
        ToTDFmt(totpar[kk])


if __name__ == '__main__':
    ToTDFmt_f()
    print("\n Hello World")
    exit()
