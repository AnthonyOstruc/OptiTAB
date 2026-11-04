from commun_redaction import ROOT
import runpy
B=chr(92)
for code in [33,35]:
 p=next(ROOT.glob(f'{code:02}_*'))/'figures/figures.py';ns=runpy.run_path(str(p));figs=ns['FIGURES']
 if code==33:
  old=B+'node[anchor=west,text=otInk] at (2.92,0) {$M$};'
  new=B+'node[anchor=north,text=otInk] at (2.8,-0.2) {$M$};'
  assert old in figs['milieu'];figs['milieu']=figs['milieu'].replace(old,new)
 else:
  old=B+'node[geoLabel,anchor=south east,xshift=-3pt,yshift=3pt] at (3.0,2.4) {$D$};'
  new=B+'node[geoLabel,anchor=north west,xshift=3pt,yshift=-3pt] at (3.0,2.4) {$D$};'
  for name in ['sym_h','sym_h_corrige']:
   assert old in figs[name];figs[name]=figs[name].replace(old,new)
 p.write_text('# -*- coding: utf-8 -*-\n"""Figures TikZ, légendes dégagées des traits."""\n'+'\n'.join(k+' = '+repr(ns[k]) for k in ['FIGURES','GEOMETRIE','TOLERE'])+'\n',encoding='utf-8')
