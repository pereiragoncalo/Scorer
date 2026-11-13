"""Build-only candidates for a NEW calendar version. Never overwrite frozen v3/v4.

SciPy/NumPy are development dependencies only. Save candidates to a fresh file,
review prefix/alternation invariants and version them before runtime integration.
"""
import sys,json,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
from mirrored_schedule import PATTERNS

def solve(n,prefix=0,limit=10):
 ids=([-1]+list(range(n))) if n%2 else list(range(n));m=len(ids);rounds=[];refs=[[]for _ in range(n)];count=0
 for r in range(m-1):
  rest=ids[1:];rest=rest[-r:]+rest[:-r] if r else rest;order=[ids[0]]+rest;row=[]
  for i in range(m//2):
   a,b=order[i],order[-i-1]
   if a<0 or b<0:continue
   row.append((a,b,count));refs[a].append((count,1,0));refs[b].append((count,-1,1));count+=1
  rounds.append(row)
 constraints=[];objective=[0.]*count;bounds_lo=[0.]*count;bounds_hi=[1.]*count
 def add(co,lo,hi):constraints.append((co,lo,hi))
 fullrefs=[r+[(j,-c,1-k)for j,c,k in r]for r in refs]
 perteam=[]
 for team,r in enumerate(refs):
  full=fullrefs[team]
  for start in range(len(full)-2):
   co={};constant=0
   for j,c,k in full[start:start+3]:co[j]=co.get(j,0)+c;constant+=k
   add(co,1-constant,2-constant)
  co={};constant=0
  for j,c,k in r:co[j]=co.get(j,0)+c;constant+=k
  add(co,(n-1)//2-constant,n//2-constant)
  br=[]
  for first,second in zip(full,full[1:]):
   j=len(objective);objective.append(100.);bounds_lo.append(0.);bounds_hi.append(1.);br.append(j)
   co={j:1.};constant=first[2]+second[2]
   for idx,c,k in (first,second):co[idx]=co.get(idx,0)-c
   add(co,constant-1,np.inf)
   co={j:1.}
   for idx,c,k in (first,second):co[idx]=co.get(idx,0)+c
   add(co,1-constant,np.inf)
  perteam.append(br)
 z=len(objective);objective.append(1.);bounds_lo.append(0.);bounds_hi.append(2*n)
 for br in perteam:add({**{j:1 for j in br},z:-1},-np.inf,0)
 for r,row in enumerate(rounds[:prefix]):
  for slot,(a,b,j)in enumerate(row):
   bit=int(PATTERNS[n][r][slot]);add({j:1},bit,bit)
 if prefix==0:
  j,c,k=refs[0][0];add({j:c},1-k,1-k)
 A=lil_matrix((len(constraints),len(objective)));lo=[];hi=[]
 for i,(co,a,b)in enumerate(constraints):
  for j,c in co.items():A[i,j]=c
  lo.append(a);hi.append(b)
 res=milp(np.array(objective),integrality=np.array([1]*count+[0]*(len(objective)-count)),bounds=Bounds(bounds_lo,bounds_hi),constraints=LinearConstraint(A.tocsr(),lo,hi),options={'time_limit':limit})
 if res.x is None:return None
 bits=np.rint(res.x[:count]).astype(int)
 patterns=[''.join(str(bits[j])for a,b,j in row)for row in rounds]
 sequences=[''.join('H' if c*bits[j]+k else 'A' for j,c,k in r)for r in fullrefs]
 assert all('HHH'not in s and 'AAA'not in s for s in sequences)
 breaks=[sum(a==b for a,b in zip(s,s[1:]))for s in sequences]
 return dict(patterns=patterns,breaks=breaks,total=sum(breaks),max=max(breaks),optimal=res.status==0)


def construction(n):
 if n==2:return ('1',)
 if n<6 or n%2:raise ValueError('Even sizes6+ or2 required')
 base=('01'*(n//2+1))[:n//2]
 return tuple(('1'+base[1:] if r==0 or r>=3 and r%2 else ('00'+base[2:] if r==2 else base))for r in range(n-1))

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--migrations',action='store_true');p.add_argument('--limit',type=float,default=10)
 args=p.parse_args()
 if args.output.exists():p.error('Use a fresh candidate file, never overwrite shipped patterns')
 result={'patterns':{n:construction(n)for n in (2,*range(6,65,2))}}
 if args.migrations:
  result['v3_prefix18']={}
  for prefix in range(1,17):
   row=solve(18,prefix,args.limit)
   if row and row['total']<164:result['v3_prefix18'][prefix]=row
 args.output.write_text(json.dumps(result,indent=2)+'\n')
