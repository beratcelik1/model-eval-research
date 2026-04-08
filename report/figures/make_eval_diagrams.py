import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

EDGE = '#4b5563'
TXT = '#1f2937'
MUTED = '#6b7280'
COLORS = {
    'source': '#dbeafe',
    'design': '#dcfce7',
    'run': '#fef3c7',
    'score': '#fee2e2',
    'decision': '#ede9fe',
    'neutral': '#f3f4f6',
}


def box(ax, x, y, w, h, title, body, fc, fs=13, body_fs=None):
    rect = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle='round,pad=0.02,rounding_size=0.03',
        linewidth=1.3,
        edgecolor=EDGE,
        facecolor=fc,
    )
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h * 0.60, title, ha='center', va='center', fontsize=fs, fontweight='bold', color=TXT)
    if body:
        ax.text(
            x + w / 2,
            y + h * 0.33,
            body,
            ha='center',
            va='center',
            fontsize=body_fs if body_fs is not None else fs - 1.1,
            color=TXT,
        )


def diamond(ax, cx, cy, w, h, text):
    pts = [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)]
    ax.add_patch(plt.Polygon(pts, closed=True, facecolor=COLORS['decision'], edgecolor=EDGE, linewidth=1.3))
    ax.text(cx, cy, text, ha='center', va='center', fontsize=12.4, fontweight='bold', color=TXT)


def arrow(ax, a, b, dashed=False):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle='-|>', mutation_scale=16, linewidth=1.45, color=EDGE, linestyle='--' if dashed else '-'))


def poly(ax, pts, dashed=False):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=EDGE, linewidth=1.45, linestyle='--' if dashed else '-')
    arrow(ax, pts[-2], pts[-1], dashed=dashed)

# Build diagram
fig, ax = plt.subplots(figsize=(8.7, 3.6), facecolor='white')
fig.subplots_adjust(left=0.01, right=0.99, bottom=0.02, top=0.98)
ax.set_xlim(0, 8.7)
ax.set_ylim(0, 3.6)
ax.axis('off')

box(ax, 0.25, 2.20, 1.40, 0.92, 'Research Sources', 'papers, reports,\nX discourse', COLORS['source'], fs=11.7)
box(ax, 1.90, 2.20, 1.40, 0.92, 'Knowledge Base', 'source-backed wiki', COLORS['source'], fs=11.8)
box(ax, 3.70, 2.10, 2.25, 1.02, 'Prompt + Rubric Design', 'prompts, answer keys,\nchallenge prompts', COLORS['design'], fs=12.1)
box(ax, 2.00, 0.72, 1.75, 0.96, 'Validation Loop', 'grok-4-1-fast-reasoning', COLORS['design'], fs=11.9, body_fs=10.3)
box(ax, 5.10, 0.72, 1.75, 0.96, 'Frozen Final Set', 'final battery', COLORS['neutral'], fs=11.8)

arrow(ax, (1.65, 2.66), (1.90, 2.66))
arrow(ax, (3.30, 2.66), (3.70, 2.66))
poly(ax, [(4.82, 2.10), (4.82, 1.86), (2.88, 1.86), (2.88, 1.68)])
arrow(ax, (3.75, 1.20), (5.10, 1.20))
poly(ax, [(2.00, 1.20), (0.90, 1.20), (0.90, 1.92), (4.25, 1.92), (4.25, 2.10)], dashed=True)

fig.savefig('report/figures/eval_build_flow.png', dpi=260, bbox_inches='tight', facecolor='white')
plt.close(fig)

# Scoring diagram
fig, ax = plt.subplots(figsize=(8.9, 4.6), facecolor='white')
fig.subplots_adjust(left=0.01, right=0.99, bottom=0.02, top=0.98)
ax.set_xlim(0, 8.9)
ax.set_ylim(0, 4.6)
ax.axis('off')

box(ax, 0.20, 3.15, 1.72, 0.94, 'Final Run', 'grok-4.20-0309-\nreasoning', COLORS['run'], fs=11.4, body_fs=10.0)
box(ax, 1.95, 3.15, 1.80, 0.94, 'Phase 1 Review', 'score cold response', COLORS['score'], fs=11.8)
diamond(ax, 5.00, 3.62, 1.45, 0.98, 'Challenge\nneeded?')
box(ax, 6.10, 3.15, 2.35, 0.94, 'Challenge Prompt', 'evidence-backed,\nanti-sycophancy', COLORS['run'], fs=11.7)

box(ax, 4.00, 1.25, 1.80, 1.00, 'Published Score', '75% phase 1\n+ 25% challenge', COLORS['score'], fs=11.4)
box(ax, 6.15, 1.25, 1.75, 1.00, 'Challenge Review', 'did Grok improve?', COLORS['score'], fs=11.4)
box(ax, 6.35, 0.05, 2.25, 0.90, 'Domain Score', 'area and overall\naggregation', COLORS['neutral'], fs=11.2, body_fs=9.6)

arrow(ax, (1.92, 3.62), (1.95, 3.62))
arrow(ax, (3.75, 3.62), (4.28, 3.62))
arrow(ax, (5.72, 3.62), (6.10, 3.62))
ax.text(5.92, 3.87, 'Yes', ha='center', va='center', fontsize=10.8, color=MUTED)

poly(ax, [(5.00, 3.13), (5.00, 2.72), (4.90, 2.72), (4.90, 2.25)])
ax.text(5.22, 2.88, 'No', ha='center', va='center', fontsize=10.8, color=MUTED)

arrow(ax, (7.28, 3.15), (7.28, 2.25))
arrow(ax, (6.15, 1.75), (5.80, 1.75))
poly(ax, [(5.80, 1.75), (6.00, 1.75), (6.00, 0.50), (6.45, 0.50)])

fig.savefig('report/figures/eval_scoring_flow.png', dpi=260, bbox_inches='tight', facecolor='white')
plt.close(fig)
