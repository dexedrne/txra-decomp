#!/usr/bin/env python3
"""Write a private performance figure and metadata from completed runtime runs."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('output',type=Path)
p.add_argument('--native',type=Path,default=Path('build/runtime-shipping/run.json'))
p.add_argument('--paced',type=Path,default=Path('build/runtime-optimized/paced5.json'))
a=p.parse_args()
native=json.loads(a.native.read_text());paced=json.loads(a.paced.read_text())
rows=[]
for label,data in (('Uncapped race',native),('Paced with audio',paced)):
    rows.append(dict(label=label,frames=data['frames'],elapsed_seconds=data['elapsed_seconds'],
        fps=data['frames']/data['elapsed_seconds'],cpu_percent=data['cpu_seconds']/data['elapsed_seconds']*100,
        audio_queue_ms=data['audio_max_queue_ms'],audio_queue_starvations=data['audio_underruns']))
a.output.mkdir(parents=True,exist_ok=True)
(a.output/'performance.json').write_text(json.dumps(rows,indent=2)+'\n')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
fig,axes=plt.subplots(1,2,figsize=(11,4.8),layout='constrained')
fig.suptitle('TXRA PC runtime · worker measurements',fontsize=17,fontweight='bold')
for ax,key,title,limit in ((axes[0],'fps','Frames per second',max(120,rows[0]['fps']*1.2)),
                         (axes[1],'cpu_percent','CPU use · 100% = one core',120)):
    bars=ax.barh([r['label'] for r in rows],[r[key] for r in rows],color=['#324967','#d38a16'],height=.5)
    ax.set_xlim(0,limit);ax.set_title(title);ax.invert_yaxis();ax.spines[['top','right','left']].set_visible(False)
    ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
    for bar,row in zip(bars,rows):
        ax.text(bar.get_width()+2,bar.get_y()+bar.get_height()/2,f"{row[key]:.1f}",va='center')
    if key=='fps':
        ax.axvline(16777216/280896,color='#667482',linestyle='--',linewidth=1)
        ax.text(61,.95,'59.73 target',transform=ax.get_xaxis_transform(),va='top',fontsize=9,color='#536272',bbox={'facecolor':'white','edgecolor':'none','alpha':.95,'pad':2})
fig.supxlabel(f"Native software output · {native['frames']:,} race frames · stereo dummy device · no real-speaker listening",fontsize=10)
fig.savefig(a.output/'performance.png',dpi=150)
fig.savefig(a.output/'performance.svg')
plt.close(fig)
path=a.output/'captions.json';captions=json.loads(path.read_text()) if path.exists() else {}
caption='After: measured uncapped race speed and paced audio playback; CPU is a percentage of one core.'
captions.update({'performance.png':caption,'performance.svg':caption})
path.write_text(json.dumps(captions,indent=2)+'\n')
print(json.dumps(rows,indent=2))
