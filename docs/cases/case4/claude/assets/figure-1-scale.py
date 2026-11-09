#!/usr/bin/env python3
"""Figure 1: DAC output, design capacity and scenario levels on a log axis. Run from the folder holding figure-1-data.csv."""
import csv, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
plt.rcParams.update({"font.family":"Liberation Sans","font.size":8.2,"pdf.fonttype":42})
INK="#0b0b0b"; INK2="#52514e"; GRID="#e4e2dc"
G={"measured":("#eb6834","o","Measured or reported output"),
   "design":("#2a78d6","s","Design capacity"),
   "scenario":("#1baf7a","D","Scenario level")}
rows=list(csv.DictReader(open("figure-1-data.csv")))
fig,ax=plt.subplots(figsize=(6.3,2.95),dpi=300)
n=len(rows)
fmt=lambda v:(f"{v/1e9:.3g} Gt" if v>=1e9 else f"{v/1e6:.3g} Mt" if v>=1e6 else f"{int(v):,} t")
for i,r in enumerate(rows):
    y=n-1-i; v=float(r["value_t_per_year"]); c,m,_=G[r["group"]]
    ax.hlines(y,1e2,v,color=GRID,lw=0.8,zorder=1)
    ax.scatter([v],[y],s=34,marker=m,color=c,edgecolor="white",linewidth=0.7,zorder=3)
    left = "long-term strategies" in r["label"]
    ax.annotate(fmt(v),(v,y),xytext=(-7 if left else 7,0),textcoords="offset points",va="center",ha="right" if left else "left",fontsize=7.6,color=INK2)
ax.axvline(1e9,color=INK2,lw=0.9,ls=(0,(4,3)),zorder=2)
ax.text(1e9,n-0.35,"1 Gt yardstick",ha="center",va="bottom",fontsize=7.6,color=INK2)
ax.set_xscale("log"); ax.set_xlim(1e2,2e10); ax.set_ylim(-0.7,n-0.3)
ax.set_yticks(range(n)); ax.set_yticklabels([r["label"] for r in reversed(rows)],color=INK)
ticks=[1e3,1e4,1e5,1e6,1e7,1e8,1e9,1e10]
ax.set_xticks(ticks); ax.set_xticklabels(["1 kt","10 kt","100 kt","1 Mt","10 Mt","100 Mt","1 Gt","10 Gt"],color=INK2)
ax.minorticks_off(); ax.tick_params(length=0)
ax.set_xlabel("Tonnes of CO2 a year (logarithmic scale: each step is ten times the last)",color=INK2)
for s in ["top","right","left"]: ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID)
h=[Line2D([],[],marker=m,color="none",markerfacecolor=c,markeredgecolor="white",markersize=6.5,label=l) for c,m,l in G.values()]
ax.legend(handles=h,loc="upper left",frameon=False,fontsize=7.8,bbox_to_anchor=(0.34,1.0),handletextpad=0.3,labelspacing=0.35)
fig.tight_layout(pad=0.3)
fig.savefig("figure-1-scale.png",dpi=300)
