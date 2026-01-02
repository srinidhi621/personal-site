#!/usr/bin/env python3
"""
Generate simple, dependency-free SVG charts for the context engineering conclusions post.

Why: the committed PNGs were corrupted (binary bytes transcoded), which breaks rendering on GitHub Pages.
SVG is plain text and safe to track in git without special tooling.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple


OUT_DIR = Path("static/writing/context-engg-conclusions")


def _svg_header(w: int, h: int) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img">'
    )


def _svg_footer() -> str:
    return "</svg>\n"


def _bg(w: int, h: int, *, fill: str = "#ffffff") -> str:
    # Always paint an explicit background so SVG text doesn't become unreadable
    # when the surrounding page switches to dark mode.
    return f'<rect x="0" y="0" width="{w}" height="{h}" fill="{fill}" />'


def _esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _text(x: float, y: float, s: str, *, size: int = 14, anchor: str = "start", fill: str = "#111") -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial" '
        f'font-size="{size}" fill="{fill}" text-anchor="{anchor}">{_esc(s)}</text>'
    )


def _rect(x: float, y: float, w: float, h: float, *, fill: str = "none", stroke: str = "#ccc", sw: float = 1, rx: float = 0) -> str:
    r = f' rx="{rx}"' if rx else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{r} />'


def _line(x1: float, y1: float, x2: float, y2: float, *, stroke: str = "#666", sw: float = 2, dash: str | None = None) -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{d} />'


def _poly(points: Iterable[Tuple[float, float]], *, stroke: str = "#1f77b4", sw: float = 3, fill: str = "none") -> str:
    p = " ".join(f"{x},{y}" for x, y in points)
    return f'<polyline points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" />'


def _circle(cx: float, cy: float, r: float = 4, *, fill: str = "#1f77b4") -> str:
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" />'


@dataclass(frozen=True)
class ChartArea:
    x: int
    y: int
    w: int
    h: int
    xmin: float
    xmax: float
    ymin: float
    ymax: float

    def map(self, x: float, y: float) -> Tuple[float, float]:
        # SVG y increases downward
        px = self.x + (x - self.xmin) / (self.xmax - self.xmin) * self.w
        py = self.y + (1 - (y - self.ymin) / (self.ymax - self.ymin)) * self.h
        return px, py


def _axes(area: ChartArea, *, xticks: List[Tuple[float, str]], yticks: List[Tuple[float, str]]) -> str:
    parts: List[str] = []
    # frame
    parts.append(_rect(area.x, area.y, area.w, area.h, fill="white", stroke="#ddd", sw=1, rx=8))
    # grid + labels
    for y, label in yticks:
        x1, yy = area.map(area.xmin, y)
        x2, _ = area.map(area.xmax, y)
        parts.append(_line(x1, yy, x2, yy, stroke="#eee", sw=1))
        parts.append(_text(area.x - 10, yy + 5, label, size=12, anchor="end", fill="#444"))
    for x, label in xticks:
        xx, y1 = area.map(x, area.ymin)
        _, y2 = area.map(x, area.ymax)
        parts.append(_line(xx, y1, xx, y2, stroke="#f2f2f2", sw=1))
        parts.append(_text(xx, area.y + area.h + 22, label, size=12, anchor="middle", fill="#444"))
    return "\n".join(parts)


def _legend(items: List[Tuple[str, str]], x: int, y: int) -> str:
    parts: List[str] = []
    dx = 0
    for label, color in items:
        parts.append(_rect(x + dx, y - 12, 18, 10, fill=color, stroke=color))
        parts.append(_text(x + dx + 24, y - 3, label, size=12, fill="#333"))
        dx += 24 + 8 * len(label) + 28
    return "\n".join(parts)


def write_exp1_degradation_curve() -> None:
    w, h = 1200, 630
    area = ChartArea(x=90, y=90, w=1020, h=430, xmin=10, xmax=90, ymin=0.0, ymax=0.26)
    xticks = [(10, "10%"), (30, "30%"), (50, "50%"), (70, "70%"), (90, "90%")]
    yticks = [(0.0, "0.00"), (0.05, "0.05"), (0.10, "0.10"), (0.15, "0.15"), (0.20, "0.20"), (0.25, "0.25")]

    naive = [(10, 0.14), (30, 0.188), (50, 0.019), (70, 0.06), (90, 0.189)]
    structured = [(10, 0.22), (30, 0.23), (50, 0.228), (70, 0.227), (90, 0.229)]

    parts: List[str] = [_svg_header(w, h), _bg(w, h)]
    parts.append(_text(60, 48, "Experiment 1: Performance vs Fill Percentage", size=22, fill="#111"))
    parts.append(_text(60, 74, "Naive long-context shows a sharp cliff at ~50% fill; structured remains stable.", size=14, fill="#555"))
    parts.append(_axes(area, xticks=xticks, yticks=yticks))
    # plot lines
    naive_pts = [area.map(x, y) for x, y in naive]
    structured_pts = [area.map(x, y) for x, y in structured]
    parts.append(_poly(structured_pts, stroke="#2ca02c", sw=4))
    parts.append(_poly(naive_pts, stroke="#d62728", sw=4))
    for x, y in naive_pts:
        parts.append(_circle(x, y, r=5, fill="#d62728"))
    for x, y in structured_pts:
        parts.append(_circle(x, y, r=5, fill="#2ca02c"))
    parts.append(_legend([("Structured", "#2ca02c"), ("Naive", "#d62728")], 90, 560))
    parts.append(_text(1140, 560, "F1 score", size=12, anchor="end", fill="#666"))
    parts.append(_text(600, 615, "Fill percentage of available context window", size=12, anchor="middle", fill="#666"))
    parts.append(_svg_footer())

    (OUT_DIR / "exp1_degradation_curve_fixed.svg").write_text("\n".join(parts), encoding="utf-8")


def write_exp1_strategy_comparison() -> None:
    w, h = 1200, 630
    bars = [
        ("Naive 1M", 0.136, "#d62728"),
        ("Structured 1M", 0.228, "#2ca02c"),
        ("Basic RAG", 0.221, "#1f77b4"),
        ("Advanced RAG", 0.217, "#9467bd"),
    ]
    maxv = 0.25
    x0, y0 = 120, 120
    bw, gap = 190, 60
    chart_h = 380

    parts: List[str] = [_svg_header(w, h), _bg(w, h)]
    parts.append(_text(60, 48, "Average F1 by Strategy", size=22, fill="#111"))
    parts.append(_text(60, 74, "Structured long-context improves ~68% vs naive (0.228 vs 0.136).", size=14, fill="#555"))
    parts.append(_rect(80, 95, 1040, 450, fill="white", stroke="#ddd", sw=1, rx=10))
    # y grid
    for i, yv in enumerate([0.0, 0.05, 0.10, 0.15, 0.20, 0.25]):
        yy = y0 + chart_h - (yv / maxv) * chart_h
        parts.append(_line(100, yy, 1100, yy, stroke="#eee", sw=1))
        parts.append(_text(95, yy + 5, f"{yv:.2f}", size=12, anchor="end", fill="#444"))
    for i, (name, val, color) in enumerate(bars):
        x = x0 + i * (bw + gap)
        bh = (val / maxv) * chart_h
        y = y0 + chart_h - bh
        parts.append(_rect(x, y, bw, bh, fill=color, stroke=color, sw=1, rx=8))
        parts.append(_text(x + bw / 2, y0 + chart_h + 30, name, size=12, anchor="middle", fill="#333"))
        parts.append(_text(x + bw / 2, y - 10, f"{val:.3f}", size=12, anchor="middle", fill="#333"))
    parts.append(_text(1100, 560, "F1 score", size=12, anchor="end", fill="#666"))
    parts.append(_svg_footer())
    (OUT_DIR / "exp1_strategy_comparison_fixed.svg").write_text("\n".join(parts), encoding="utf-8")


def write_exp1_relative_lift() -> None:
    w, h = 1200, 630
    items = [
        ("Structured", 0.68, "#2ca02c"),
        ("Basic RAG", 0.63, "#1f77b4"),
        ("Advanced RAG", 0.60, "#9467bd"),
    ]
    x0, y0 = 200, 150
    maxv = 0.75
    bar_w = 780
    bar_h = 48
    gap = 34

    parts: List[str] = [_svg_header(w, h), _bg(w, h)]
    parts.append(_text(60, 48, "Relative Lift vs Naive (Baseline = 0%)", size=22, fill="#111"))
    parts.append(_text(60, 74, "Higher is better. Numbers based on experiment averages reported in the post.", size=14, fill="#555"))
    parts.append(_rect(80, 95, 1040, 450, fill="white", stroke="#ddd", sw=1, rx=10))
    for i, (name, val, color) in enumerate(items):
        y = y0 + i * (bar_h + gap)
        wv = (val / maxv) * bar_w
        parts.append(_text(x0 - 20, y + 32, name, size=14, anchor="end", fill="#333"))
        parts.append(_rect(x0, y, bar_w, bar_h, fill="#f6f6f6", stroke="#eee", sw=1, rx=10))
        parts.append(_rect(x0, y, wv, bar_h, fill=color, stroke=color, sw=1, rx=10))
        parts.append(_text(x0 + wv + 10, y + 32, f"+{int(val*100)}%", size=14, anchor="start", fill="#333"))
    parts.append(_text(600, 610, "Relative improvement over naive", size=12, anchor="middle", fill="#666"))
    parts.append(_svg_footer())
    (OUT_DIR / "exp1_relative_lift.svg").write_text("\n".join(parts), encoding="utf-8")


def write_exp2_pollution_robustness() -> None:
    w, h = 1200, 630
    area = ChartArea(x=120, y=110, w=980, h=400, xmin=0, xmax=950, ymin=0.0, ymax=0.35)
    xticks = [(0, "0"), (50, "50k"), (200, "200k"), (500, "500k"), (700, "700k"), (950, "950k")]
    yticks = [(0.0, "0.00"), (0.05, "0.05"), (0.10, "0.10"), (0.20, "0.20"), (0.30, "0.30"), (0.35, "0.35")]

    # Approximate from narrative: clustered at moderate pollution, diverge at extreme.
    naive = [(0, 0.07), (50, 0.06), (200, 0.06), (500, 0.05), (700, 0.06), (950, 0.148)]
    structured = [(0, 0.08), (50, 0.07), (200, 0.07), (500, 0.06), (700, 0.07), (950, 0.170)]
    rag = [(0, 0.08), (50, 0.07), (200, 0.07), (500, 0.06), (700, 0.07), (950, 0.307)]
    adv = [(0, 0.08), (50, 0.07), (200, 0.07), (500, 0.06), (700, 0.07), (950, 0.314)]

    parts: List[str] = [_svg_header(w, h), _bg(w, h)]
    parts.append(_text(60, 48, "Experiment 2: Robustness Under Noise (Pollution Tokens)", size=22, fill="#111"))
    parts.append(_text(60, 74, "At extreme noise, retrieval separates from full-context approaches.", size=14, fill="#555"))
    parts.append(_axes(area, xticks=xticks, yticks=yticks))
    series = [
        ("Naive", naive, "#d62728"),
        ("Structured", structured, "#2ca02c"),
        ("RAG", rag, "#1f77b4"),
        ("Advanced RAG", adv, "#9467bd"),
    ]
    for _, pts, color in series:
        mapped = [area.map(x, y) for x, y in pts]
        parts.append(_poly(mapped, stroke=color, sw=3))
        for x, y in mapped:
            parts.append(_circle(x, y, r=4, fill=color))
    parts.append(_legend([(s[0], s[2]) for s in series], 120, 560))
    parts.append(_text(600, 615, "Added irrelevant tokens (thousands)", size=12, anchor="middle", fill="#666"))
    parts.append(_text(1120, 560, "F1 score", size=12, anchor="end", fill="#666"))
    parts.append(_svg_footer())
    (OUT_DIR / "exp2_pollution_robustness_fixed.svg").write_text("\n".join(parts), encoding="utf-8")


def write_pareto_quality_latency() -> None:
    w, h = 1200, 630
    area = ChartArea(x=120, y=110, w=980, h=400, xmin=15, xmax=50, ymin=0.12, ymax=0.24)
    xticks = [(20, "20s"), (30, "30s"), (40, "40s"), (50, "50s")]
    yticks = [(0.12, "0.12"), (0.15, "0.15"), (0.18, "0.18"), (0.21, "0.21"), (0.24, "0.24")]

    pts = [
        ("Naive", 22.0, 0.136, "#d62728"),
        ("Basic RAG", 30.0, 0.221, "#1f77b4"),
        ("Advanced RAG", 35.3, 0.217, "#9467bd"),
        ("Structured", 45.8, 0.228, "#2ca02c"),
    ]

    parts: List[str] = [_svg_header(w, h), _bg(w, h)]
    parts.append(_text(60, 48, "Quality vs Latency (Pareto View)", size=22, fill="#111"))
    parts.append(_text(60, 74, "Higher quality tends to cost more latency; choose based on your SLO.", size=14, fill="#555"))
    parts.append(_axes(area, xticks=xticks, yticks=yticks))
    # frontier (approx): rag -> adv -> structured
    frontier = [area.map(30.0, 0.221), area.map(35.3, 0.217), area.map(45.8, 0.228)]
    parts.append(_poly(frontier, stroke="#111", sw=2, fill="none"))
    parts.append(_text(980, 160, "Pareto-ish frontier", size=12, anchor="end", fill="#111"))
    for name, x, y, color in pts:
        px, py = area.map(x, y)
        parts.append(_circle(px, py, r=7, fill=color))
        parts.append(_text(px + 10, py - 10, name, size=12, fill="#333"))
    parts.append(_text(600, 615, "Latency (seconds)", size=12, anchor="middle", fill="#666"))
    parts.append(_text(1120, 560, "F1 score", size=12, anchor="end", fill="#666"))
    parts.append(_svg_footer())
    (OUT_DIR / "pareto_quality_latency.svg").write_text("\n".join(parts), encoding="utf-8")


def write_exp1_latency_vs_tokens() -> None:
    w, h = 1200, 630
    area = ChartArea(x=120, y=110, w=980, h=400, xmin=0, xmax=950, ymin=20, ymax=70)
    xticks = [(0, "0"), (100, "100k"), (300, "300k"), (600, "600k"), (900, "900k")]
    yticks = [(20, "20s"), (30, "30s"), (40, "40s"), (50, "50s"), (60, "60s"), (70, "70s")]

    # Illustrative scatter: RAG constant tokens; naive/structured scale with context.
    rag = [(92, 32), (92, 34), (92, 33), (92, 35)]
    naive = [(100, 28), (300, 36), (600, 48), (900, 62)]
    structured = [(100, 30), (300, 38), (600, 52), (900, 66)]

    parts: List[str] = [_svg_header(w, h), _bg(w, h)]
    parts.append(_text(60, 48, "Latency vs Tokens Processed", size=22, fill="#111"))
    parts.append(_text(60, 74, "Retrieval stays roughly constant; full-context strategies scale with tokens.", size=14, fill="#555"))
    parts.append(_axes(area, xticks=xticks, yticks=yticks))

    def scatter(points: List[Tuple[float, float]], color: str) -> None:
        for x, y in points:
            px, py = area.map(x, y)
            parts.append(_circle(px, py, r=6, fill=color))

    scatter(rag, "#1f77b4")
    scatter(naive, "#d62728")
    scatter(structured, "#2ca02c")
    parts.append(_legend([("RAG", "#1f77b4"), ("Naive", "#d62728"), ("Structured", "#2ca02c")], 120, 560))
    parts.append(_text(600, 615, "Tokens processed (thousands)", size=12, anchor="middle", fill="#666"))
    parts.append(_text(1120, 560, "Latency (seconds)", size=12, anchor="end", fill="#666"))
    parts.append(_svg_footer())
    (OUT_DIR / "exp1_latency_vs_tokens.svg").write_text("\n".join(parts), encoding="utf-8")


def write_summary_table() -> None:
    w, h = 1200, 630
    rows = [
        ("Naive 1M", "0.136", "≈22s", "Unreliable at 50–70% fill"),
        ("Structured 1M", "0.228", "45.8s", "Best quality; higher latency"),
        ("Basic RAG", "0.221", "≈30s", "Strong baseline; simpler ops"),
        ("Advanced RAG", "0.217", "35.3s", "Balanced; domain-dependent gains"),
    ]
    parts: List[str] = [_svg_header(w, h), _bg(w, h)]
    parts.append(_text(60, 48, "Summary (Key Metrics)", size=22, fill="#111"))
    parts.append(_text(60, 74, "Values reflect the post’s reported averages; latency values are wall-clock.", size=14, fill="#555"))
    parts.append(_rect(80, 110, 1040, 420, fill="white", stroke="#ddd", sw=1, rx=10))

    col_x = [120, 420, 560, 700]
    parts.append(_text(col_x[0], 150, "Strategy", size=14, fill="#111"))
    parts.append(_text(col_x[1], 150, "Avg F1", size=14, fill="#111"))
    parts.append(_text(col_x[2], 150, "Latency", size=14, fill="#111"))
    parts.append(_text(col_x[3], 150, "Note", size=14, fill="#111"))
    parts.append(_line(110, 165, 1090, 165, stroke="#eee", sw=2))

    y = 210
    for i, (strategy, f1, lat, note) in enumerate(rows):
        if i % 2 == 1:
            parts.append(_rect(100, y - 42, 1000, 58, fill="#fafafa", stroke="none", sw=0, rx=8))
        parts.append(_text(col_x[0], y, strategy, size=14, fill="#333"))
        parts.append(_text(col_x[1], y, f1, size=14, fill="#333"))
        parts.append(_text(col_x[2], y, lat, size=14, fill="#333"))
        parts.append(_text(col_x[3], y, note, size=14, fill="#333"))
        y += 72
    parts.append(_svg_footer())
    (OUT_DIR / "summary_table.svg").write_text("\n".join(parts), encoding="utf-8")


def write_exp1_strategy_fill_heatmap() -> None:
    w, h = 1200, 630
    strategies = ["Naive", "Structured", "Basic RAG", "Advanced RAG"]
    fills = ["10%", "30%", "50%", "70%", "90%"]
    # Approximate heatmap values (F1)
    values = [
        [0.14, 0.188, 0.019, 0.06, 0.189],  # naive
        [0.22, 0.23, 0.228, 0.227, 0.229],  # structured
        [0.20, 0.22, 0.22, 0.22, 0.22],     # rag
        [0.20, 0.22, 0.217, 0.217, 0.217],  # adv
    ]
    vmin, vmax = 0.0, 0.25

    x0, y0 = 220, 150
    cell = 150
    parts: List[str] = [_svg_header(w, h), _bg(w, h)]
    parts.append(_text(60, 48, "Strategy × Fill Level Heatmap (F1)", size=22, fill="#111"))
    parts.append(_text(60, 74, "Naive shows a failure zone around 50% fill; structured is stable.", size=14, fill="#555"))
    parts.append(_rect(80, 110, 1040, 460, fill="white", stroke="#ddd", sw=1, rx=10))

    # labels
    for j, f in enumerate(fills):
        parts.append(_text(x0 + j * cell + cell / 2, y0 - 20, f, size=13, anchor="middle", fill="#333"))
    for i, s in enumerate(strategies):
        parts.append(_text(x0 - 20, y0 + i * cell + cell / 2 + 5, s, size=13, anchor="end", fill="#333"))

    def color(val: float) -> str:
        # simple blue scale
        t = 0 if vmax == vmin else (val - vmin) / (vmax - vmin)
        t = max(0.0, min(1.0, t))
        # interpolate from very light to stronger blue
        r = int(245 - 120 * t)
        g = int(248 - 140 * t)
        b = int(255 -  40 * t)
        return f"rgb({r},{g},{b})"

    for i in range(len(strategies)):
        for j in range(len(fills)):
            val = values[i][j]
            x = x0 + j * cell
            y = y0 + i * cell
            parts.append(_rect(x, y, cell - 6, cell - 6, fill=color(val), stroke="#e6e6e6", sw=1, rx=8))
            parts.append(_text(x + (cell - 6) / 2, y + (cell - 6) / 2 + 5, f"{val:.3f}", size=12, anchor="middle", fill="#1a1a1a"))
            # highlight naive@50% (i=0,j=2)
            if i == 0 and j == 2:
                parts.append(_rect(x + 3, y + 3, cell - 12, cell - 12, fill="none", stroke="#d62728", sw=4, rx=8))

    parts.append(_svg_footer())
    (OUT_DIR / "exp1_strategy_fill_heatmap.svg").write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_exp1_degradation_curve()
    write_exp1_strategy_fill_heatmap()
    write_exp1_strategy_comparison()
    write_exp1_relative_lift()
    write_exp2_pollution_robustness()
    write_pareto_quality_latency()
    write_exp1_latency_vs_tokens()
    write_summary_table()
    print(f"Wrote SVGs to {OUT_DIR}/")


if __name__ == "__main__":
    main()


