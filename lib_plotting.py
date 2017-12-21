#!/usr/bin/env python
import ROOT
from ROOT import TCanvas
from ROOT import TLegend

def comp_two_w_ratio(h1, h2):
    c = TCanvas()
    c.Draw()
    c.Divide(1,2)
    h1.SetLineColor(ROOT.kBlue)
    h1.SetMarkerColor(ROOT.kBlue)
    h2.SetLineColor(ROOT.kRed)
    h2.SetMarkerColor(ROOT.kRed)
    c.cd(1)
    h1.Draw("ehist")
    h2.Draw("ehistsame")
    lg = TLegend(0.4, 0.5, 0.9, 0.9)
    lg.AddEntry(h1, h1.GetName(), "lp")
    lg.AddEntry(h2, h2.GetName(), "lp")
    lg.Draw()
    #gPad.SetLogy()
    c.cd(2)
    h_ratio = h1.Clone("h_ratio")
    h_ratio.Divide(h2)
    h_ratio.Draw()
    h_ratio.GetYaxis().SetRangeUser(0.5, 1.5)
    c.Print("tmp.pdf")
    return

def overlay(pdfname, show_ratio, *arg):
    lg = TLegend(0.3, 0.45, 0.9, 0.9)
    #c = TCanvas()
    c.SetWindowSize(600, 600)
    if show_ratio:
        c.Divide(1, 2)
    icolor = 1
    hh = [] # holder for ratio
    hd = [] # holder for diff
    for h in arg:
        if icolor==5:
            icolor += 1
        if show_ratio:
            c.cd(1)
        h.Sumw2()
        #h.Scale(1./h.Integral())
        h.SetLineColor(icolor)
        h.SetMarkerColor(icolor)
        if icolor==1:
            h.SetMarkerStyle(24)
            h.SetMarkerSize(0.8)
            h.Draw("ehist")
            #h.GetYaxis().SetRangeUser(0, 1.2)
            h.GetYaxis().SetRangeUser(0, 0.4)
        else:
            h.Draw("ehistsame")
        lg.AddEntry(h, h.GetName(), "lp")
        h.SetTitle("")
        if show_ratio:
            c.cd(2)
            h_ratio = h.Clone(h.GetName()+'_ratio')
            hh.append(h.Clone(h.GetName()+'_ratio'))
            h_ratio = hh[-1]
            h_ratio.GetYaxis().SetTitle("MC/data")
            h_ratio.Divide(arg[0])
            if icolor==1:
                h_ratio.Draw("e")
                #h_ratio.GetYaxis().SetRangeUser(0.5, 1.5)
                h_ratio.GetYaxis().SetRangeUser(0., 2.0)
            else:
                h_ratio.Draw("esame")
            #c.cd(3)
            #h_diff = h.Clone(h.GetName()+'_diff')
            #hd.append(h.Clone(h.GetName()+'_diff'))
            #h_diff = hd[-1]
            #h_diff.GetYaxis().SetTitle("MC/data")
            #h_diff.Add(arg[0], -1)
            #if icolor==1:
            #    h_diff.Draw("e")
            #    h_diff.GetYaxis().SetRangeUser(-0.5, 0.5)
            #else:
            #    h_diff.Draw("esame")
        icolor += 1
    if show_ratio:
        c.cd(1)
        #gPad.SetLogy()
    lg.Draw()
    c.Print(pdfname)
    return
