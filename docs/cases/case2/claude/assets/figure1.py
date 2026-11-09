import csv, collections
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
rows = list(csv.DictReader(open("assets/figure1-data.csv")))
s = collections.OrderedDict()
for r in rows:
    s.setdefault(r["series"], []).append(r)
style = [("#0072B2","o","-"),("#D55E00","s","--"),("#009E73","^",":")]
plt.rcParams["font.family"] = "Liberation Serif"
fig, ax = plt.subplots(figsize=(6.4, 3.5), dpi=200)
for (name, pts), (c, m, ls) in zip(s.items(), style):
    x = [float(p["median_steps_per_day"]) for p in pts]
    y = [float(p["hazard_ratio_all_cause_mortality"]) for p in pts]
    ax.plot(x, y, color=c, marker=m, linestyle=ls, linewidth=1.8, markersize=6, label=name)
ax.axvline(10000, color="#666666", linewidth=0.8)
ax.text(10100, 1.04, "10,000", fontsize=8, color="#444444")
ax.set_xlabel("Average steps per day (group median)", fontsize=9)
ax.set_ylabel("Mortality risk relative to reference group\n(hazard ratio; 1.0 = reference)", fontsize=9)
ax.set_ylim(0.25, 1.1); ax.set_xlim(2000, 13000)
ax.grid(alpha=0.25); ax.tick_params(labelsize=8)
ax.legend(fontsize=7.5, loc="lower left", frameon=False)
for sp in ("top","right"): ax.spines[sp].set_visible(False)
fig.tight_layout()
fig.savefig("assets/figure1.png")
