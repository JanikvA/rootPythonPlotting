#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test for using seaborn to plot histograms from root files
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import ROOT

def getHistFromRfile(rfileName):
    rfile=ROOT.TFile(rfileName)
    LOH=[]
    for k in rfile.GetListOfKeys():
        name=k.GetName()
        obj=rfile.Get(name)
        if obj.ClassName()=="TCanvas":
            #TODO make this resursive
            LOP=obj.GetListOfPrimitives()
            for p in LOP:
                if p.ClassName()=="TPad":
                    tpadLOP=p.GetListOfPrimitives()
                    for pp in tpadLOP:
                        if "TH1" in pp.ClassName():
                            LOH.append(pp)
                else:
                    LOH.append(p)
        elif "TH1" in obj.ClassName():
            LOH.append(p)
    return LOH

def convertROOThist(hist):
    para={"x":[], "weights":[], "bins":[]}
    for b in range(1,hist.GetNbinsX()+1):
        para["x"].append(hist.GetXaxis().GetBinCenter(b))
        para["weights"].append(hist.GetBinContent(b))
        if b==1:
            para["bins"].append(hist.GetXaxis().GetBinLowEdge(b))
        para["bins"].append(hist.GetXaxis().GetBinUpEdge(b))
    return para


def main(args):
    listOfHists=[]
    for fileName in args.input:
        listOfHists=listOfHists+getHistFromRfile(fileName)

    parameters=convertROOThist(listOfHists[0])
    plt.hist(**parameters)
    plt.gca().set(title='Frequency Histogram', ylabel='Frequency');
    plt.show()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-i", "--input", default=None, help="Input root files",nargs="*")
    # parser.add_argument('infile', help="Input file", type=argparse.FileType('r'))
    # parser.add_argument('-o', '--outfile', help="Output file", default=sys.stdout, type=argparse.FileType('w'))
    # parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true", default=False)
    args = parser.parse_args()
    main(args)
