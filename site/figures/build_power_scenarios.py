#!/usr/bin/env python3
"""Reproduce the constant-power comparison from BJ-STU-001 rev C, section 5.

Requires matplotlib only for figure authoring, never for building the website.
Run from any directory. Outputs are in assets/images and assets/data.
"""
from pathlib import Path
import csv
import os
import re

os.environ.setdefault('MPLCONFIGDIR', '/private/tmp/blackjack-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SITE = Path(__file__).resolve().parents[1]
tokens = (SITE / 'assets/tokens.css').read_text().split('[data-theme="field-light"]')[0]
palette = dict(re.findall(r'--([a-z-]+):\s*(#[0-9a-fA-F]{6})', tokens))
cases = [('Edge AI Assistant / average', 13.5, 'signal', '-'),
         ('Smart Mirror / average', 14.7, 'text', '--'),
         ('Smart Mirror / peak', 33.0, 'accent', '-')]
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                     'text.color': palette['text'], 'axes.labelcolor': palette['text'],
                     'xtick.color': palette['muted'], 'ytick.color': palette['muted'],
                     'axes.edgecolor': palette['line'], 'svg.fonttype': 'path'})
fig, ax = plt.subplots(figsize=(10, 6.4), facecolor=palette['bg'])
ax.set_facecolor(palette['bg'])
volts = [9.0 + i * 3.6 / 180 for i in range(181)]
for label, watts, colour, line in cases:
    ax.plot(volts, [watts / v for v in volts], color=palette[colour],
            linestyle=line, linewidth=2.5, label=f'{label}: {watts:g} W')
    ax.scatter([9, 11.1, 12.6], [watts / v for v in [9, 11.1, 12.6]],
               color=palette[colour], s=24, zorder=4)
ax.axhline(2, color=palette['muted'], linestyle=':', linewidth=1.7)
ax.text(9.1, 2.08, '2 A retail-module output reference*', color=palette['muted'], fontsize=11)
ax.axvspan(9, 12, color=palette['surface-raised'], alpha=.65, zorder=0)
ax.text(9.1, 3.86, 'Below 12 V: board input behaviour requires verification',
        color=palette['muted'], fontsize=10)
ax.set(xlim=(9, 12.6), ylim=(0, 4.1), xlabel='Battery / board input voltage (V)',
       ylabel='Estimated board current (A)', xticks=[9, 10, 11.1, 12, 12.6])
ax.grid(axis='y', color=palette['line'], linewidth=.7)
ax.spines[['top', 'right']].set_visible(False)
ax.legend(loc='lower left', frameon=False, fontsize=10, labelcolor=palette['text'])
fig.text(.105, .94, 'The power case changes as the battery discharges.', fontsize=18,
         color=palette['text'], weight='bold')
fig.text(.105, .895, 'Calculated I = P / V • supplier reference workloads • motor load excluded',
         fontsize=11, color=palette['muted'])
fig.text(.105, .06, '*Installed module revision and its ratings must be confirmed.\n'
         'Constant-power extrapolation, not measured rover demand or proof of operation below 12 V.\n'
         'Source: BJ-STU-001 rev C §5; Arduino ABX00181 reference loads.',
         fontsize=9.5, color=palette['muted'], linespacing=1.5)
fig.subplots_adjust(left=.105, right=.965, top=.84, bottom=.235)
images = SITE / 'assets/images'
fig.savefig(images / 'fig-power-scenarios.png', dpi=180, facecolor=fig.get_facecolor())
fig.savefig(images / 'fig-power-scenarios.svg', facecolor=fig.get_facecolor())
svg_path = images / 'fig-power-scenarios.svg'
svg_path.write_text('\n'.join(line.rstrip() for line in svg_path.read_text().splitlines()) + '\n')
data = SITE / 'assets/data'
data.mkdir(exist_ok=True)
with (data / 'power-scenarios.csv').open('w', newline='') as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerow(['reference_workload', 'power_W', 'voltage_V', 'estimated_board_current_A'])
    for label, watts, _, _ in cases:
        for v in [12.6, 11.1, 9.0]:
            writer.writerow([label, watts, v, f'{watts/v:.6f}'])
print('Wrote PNG, SVG and nine-row calculation table from BJ-STU-001 rev C.')
