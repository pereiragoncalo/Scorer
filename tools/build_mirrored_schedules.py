"""Build-only candidate mirrored orientations (SciPy); never replace shipped v3 tables.

Review generated candidates under a NEW schedule version/migration. The runtime
module contains the frozen data, uses no solver and consumes no gameplay RNG.
"""
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
import sys,json,time

def solve(n,limit=10,prefix=2,anchor=False):
 ids=list(range(n));ids=([-1]+ids) if n%2 else ids;m=len(ids);rounds=[];ref=[[] for _ in range(n)];old=[]
 for r in range(m-1):
  rest=ids[1:];rest=rest[-r:]+rest[:-r] if r else rest;order=[ids[0]]+rest;row=[]
  for i in range(m//2):
   a,b=order[i],order[-1-i]
   if a<0 or b<0:continue
   j=len(old);flip=(r%2 if i==0 else i%2);old.append(1-flip);row.append((a,b,j));ref[a].append((j,1,0));ref[b].append((j,-1,1))
  rounds.append(row)
 constraints=[]
 for refs in ref:
  full=refs+[(j,-c,1-k) for j,c,k in refs]
  for z in range(len(full)-2):
   triples=full[z:z+3];co={};constant=0
   for j,c,k in triples:co[j]=co.get(j,0)+c;constant+=k
   constraints.append((co,1-constant,2-constant))
  co={};constant=0
  for j,c,k in refs:co[j]=co.get(j,0)+c;constant+=k
  games=n-1;constraints.append((co,games//2-constant,(games+1)//2-constant))
 for row in rounds[:prefix]:
  for a,b,j in row:constraints.append(({j:1},old[j],old[j]))
 if anchor:
  for i,(j,c,k) in enumerate(ref[0]):constraints.append(({j:c},(1-i%2)-k,(1-i%2)-k))
 A=lil_matrix((len(constraints),len(old)));lo=[];hi=[]
 for i,(co,a,b) in enumerate(constraints):
  for j,c in co.items():A[i,j]=c
  lo.append(a);hi.append(b)
 res=milp(np.zeros(len(old)),integrality=np.ones(len(old)),bounds=Bounds(0,1),constraints=LinearConstraint(A.tocsr(),lo,hi),options={'time_limit':limit})
 if res.x is None:return {'n':n,'status':res.message}
 x=np.rint(res.x).astype(int);patterns=[]
 for refs in ref:
  a=''.join('H' if c*x[j]+k else 'A' for j,c,k in refs);patterns.append(a+a.translate(str.maketrans('HA','AH')))
 assert all('HHH' not in a and 'AAA' not in a for a in patterns)
 return dict(n=n,status='ok',orientations=[''.join(str(x[j]) for a,b,j in row) for row in rounds],patterns=patterns)
if __name__=='__main__':
 import argparse
 from pathlib import Path
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--maximum',type=int,default=48);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 if not 2<=args.maximum<=64:parser.error('maximum must be2–64')
 result={}
 for n in range(2,args.maximum+1):
  if n==4:continue
  r=solve(n,8,prefix=2)
  if r['status']!='ok':r=solve(n,30,prefix=0,anchor=True)
  if r['status']!='ok':raise RuntimeError(str(r))
  result[n]=r['orientations'];print(n,flush=True)
 args.output.write_text(json.dumps(result,indent=2)+'\n')
