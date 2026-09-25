"""Draw a compact, source-based explanation of the forestry sampling criteria."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'assets/images/projects/evidence'
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'path'})
fig, ax = plt.subplots(figsize=(6.2,4.1), facecolor='white')
fig.subplots_adjust(left=0,right=1,top=1,bottom=0)
ax.set_xlim(0,620); ax.set_ylim(0,410); ax.axis('off')
ink, green, line = '#28372f', '#365b49', '#d4d8cc'
ax.text(28,370,'Forestry sampling',fontsize=20,color=ink,ha='left')
ax.text(28,335,'Within the chosen study area',fontsize=13,color='#62685f')
rules = [('Forest cover','AVI species percentage > 0'),('Gentle slope','Less than 5°'),('Road access','Within 1,000 metres')]
for y, (label, value) in zip([263,191,119],rules):
    ax.add_patch(Rectangle((28,y-28),355,58,facecolor='#f4f6ef',edgecolor=line,linewidth=1))
    ax.text(43,y+6,label,fontsize=14,color=ink,va='center')
    ax.text(43,y-15,value,fontsize=11.5,color='#62685f',va='center')
ax.plot([395,409,409,395],[291,291,91,91],color=green,linewidth=1.5)
ax.add_patch(FancyArrowPatch((410,191),(452,191),arrowstyle='-|>',mutation_scale=15,color=green,linewidth=1.5))
ax.add_patch(Circle((510,222),13,facecolor=green,edgecolor=green))
ax.text(510,181,'Random',ha='center',fontsize=14,color=ink)
ax.text(510,159,'sample points',ha='center',fontsize=14,color=ink)
ax.text(28,35,'All three conditions must be met.',fontsize=12.5,color=green)
fig.savefig(OUT/'forestry-sampling-criteria.svg',facecolor='white')
fig.savefig(OUT/'forestry-sampling-criteria.png',dpi=180,facecolor='white')
svg = OUT/'forestry-sampling-criteria.svg'
svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines())+'\n', encoding='utf-8')
plt.close(fig)
