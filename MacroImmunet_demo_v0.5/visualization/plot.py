import json
import sys
import os
import matplotlib.pyplot as plt


# =========================
# 🔹 utils
# =========================
def load_json(path):
    with open(path) as f:
        return json.load(f)
# =========================
# 🔹 event_log
# =========================
def generate_event_log(data):

    IMPORTANT_BEHAVIORS = {
        "release_perforin",
        "release_IL2",
        "produce_pMHC"
    }

    ICON_MAP = {
        "produce_pMHC": "🟡",
        "release_IL2": "🔵",
        "release_perforin": "🔴"
    }

    GROUP_MAP = {
        "host_cell": "host_cell",
        "cd4_t": "cd4_t",
        "cd8_t": "cd8_t"
    }

    SEP = "------------------"

    all_logs = []

    for i, frame in enumerate(data):

        tick = frame["tick"]
        lines = []

        # ====== header ======
        lines.append("")
        lines.append(f"{'='*18}  TICK {tick}  {'='*18}")
        lines.append("")

        # ====== 按 cell type 分组 ======
        grouped = {}

        for cid, cell in frame["cells"].items():
            ctype = cell["type"]
            grouped.setdefault(ctype, {})

            for b in cell.get("behaviors", []):
                b_id = b["behavior_id"] if isinstance(b, dict) else b

                if b_id in IMPORTANT_BEHAVIORS:
                    grouped[ctype].setdefault(b_id, []).append(str(cid))

        # ====== 输出每个 group ======
        for ctype, items in grouped.items():
            lines.append(f"{GROUP_MAP.get(ctype, ctype)}：")
 
            if items:
                for b_id, cid_list in items.items():
                    icon = ICON_MAP.get(b_id, "🔶")
                    count = len(cid_list)

                    cid_str = ",".join(cid_list)

                    lines.append(f"  {icon} {b_id} ×{count} ({cid_str})")
            else:
                lines.append("  (none)")

            lines.append("")   # 🔥 关键：group之间留白
            lines.append("------------------")
            lines.append("")

        # ====== events（死亡） ======
        event_lines = []

        for e in extract_events(frame):
            if e.get("type") == "cell_die":
                target = str(e.get("target"))

                if target not in frame["cells"]:
                    continue

                event_lines.append(f"🔶 {target} died")

        if event_lines:
            lines.append("events:")
            for e in event_lines:
                lines.append(f"  {e}")

            lines.append("")
            lines.append("------------------")
            lines.append("")

        all_logs.append({
            "tick": tick,
            "lines": lines
        })

    return all_logs

# =========================
# 🔹 2D world（2d）
# space 暂停 / 继续
# =========================
def plot_2d_world(data, interval=0.5):
    import matplotlib.pyplot as plt
    global current_cells
    logs_per_frame = generate_event_log(data)

    color_map = {
        "cd8_t": "#1f77b4",
        "cd4_t": "#2ca02c",
        "host_cell": "#d62728"
    }

    # 🔥 双面板
    fig, (ax_world, ax_log) = plt.subplots(
        1, 2,
        figsize=(10, 5),
        gridspec_kw={'width_ratios': [3, 1]}
    )

    plt.ion()

    paused = False
    tick_index = 0
    log_buffer = []
    current_field = "IL2"

    def on_key(event):
        nonlocal paused, tick_index, current_field
 
        if event.key == ' ':
            paused = not paused

        elif event.key == 'right':
            tick_index = min(tick_index + 1, len(data) - 1)

        elif event.key == 'left':
            tick_index = max(tick_index - 1, 0)

    fig.canvas.mpl_connect('key_press_event', on_key)
    cbar = None
    while tick_index < len(data):

        frame = data[tick_index]

        tick = frame["tick"]
        cells = frame["cells"]
        current_cells = cells

        # =========================
        # 🎨 正常绘图（无论是否 paused 都执行）
        # =========================
        ax_world.clear()
        ax_log.clear()

        # =========================
        # 🔥 MULTI FIELD（推荐）
        # =========================
        fields_to_draw = [
            ("IL2", "Greens", 0.25),
            ("pMHC", "Reds", 0.25),
            ("perforin", "Blues", 0.25)
        ]

        for fname, cmap, alpha in fields_to_draw:
            field = build_real_field(frame, substance=fname)
            ax_world.imshow(
                field,
                cmap=cmap,
                origin="lower",
                extent=(0, 10, 0, 10),
                alpha=alpha,
                interpolation="bilinear"
            )
        
        # =========================
        # TuRE/FALSE
        # =========================
        SHOW_COLORBAR = False
        if SHOW_COLORBAR and cbar is None:
            cbar = fig.colorbar(im, ax=ax_world, fraction=0.046)
            cbar.set_label("IL2_signal")
        # =========================
        # 🔵 cells
        # =========================
        xs, ys, colors, sizes = [], [], [], []

        from collections import defaultdict

        grouped = defaultdict(list)

        for cid, cell in cells.items():
            if "pos" not in cell:
                continue

            ctype = cell.get("type", "unknown")
            grouped[ctype].append(cell)

        for ctype, cell_list in grouped.items():
            xs, ys, sizes = [], [], []

            for cell in cell_list:
                x, y = cell["pos"]
                xs.append(x)
                ys.append(y)

                stress = cell.get("node", {}).get("stress", 0)
                sizes.append(80 + stress * 400)

            ax_world.scatter(
                xs,
                ys,
                s=sizes,
                c=color_map.get(ctype, "#cccccc"),
                alpha=0.9,
                edgecolors="black",
                linewidths=0.5
            )

        # =========================
        # 🔥 attack线
        # =========================
        for e in extract_events(frame):
            if e.get("type") == "damage_cell":
                s = str(e["source"])
                t = str(e["target"])

                if s in cells and t in cells:
                    x1, y1 = cells[s]["pos"]
                    x2, y2 = cells[t]["pos"]

                    ax_world.plot([x1, x2], [y1, y2],
                                  color="red", linestyle="--", alpha=0.7)
        from matplotlib.lines import Line2D

        legend_elements = []

        # 🔵 cell legend（每种只出现一次）
        for t, c in color_map.items():
            legend_elements.append(
                Line2D(
                    [0], [0],
                    marker='o',
                    color='w',
                    label=t,
                    markerfacecolor=c,
                    markeredgecolor='black',
                    markersize=8
                )
            )

        ax_world.legend(handles=legend_elements, loc="lower right")
        # =========================
        # 🧠 更新日志（核心升级点）
        # =========================
        new_lines = logs_per_frame[tick]["lines"]

        if new_lines:
            log_buffer.extend(new_lines)

        log_buffer = log_buffer[-12:]  # 滚动窗口

        # =========================
        # 📝 右侧日志面板
        # =========================
        ax_log.set_title("Event Log")
        ax_log.axis("off")

        y = 0.95
        for line in reversed(log_buffer):
            ax_log.text(0.05, y, line, fontsize=9)
            y -= 0.07
        # =========================
        # 🧠 CAUSAL CHAIN（🔥加在这里）
        # =========================
        if tick_index > 0:
            chains = extract_causal_chain(frame, data[tick_index - 1])

            if chains:
                y -= 0.05
                ax_log.text(0.05, y, "[CAUSE]", fontsize=10, weight='bold')

                for c in chains[:5]:   # 最多显示5条
                    y -= 0.05
                    ax_log.text(0.05, y, c, fontsize=8)
        # =========================
        # 🧬 SELECTED CELL
        # =========================
        if selected_cell:
            cid, cell = selected_cell

            y -= 0.05
            ax_log.text(0.05, y, f"[SELECTED] {cid}", fontsize=10, weight='bold')

            for k, v in cell.get("node", {}).items():
                y -= 0.05
                ax_log.text(0.05, y, f"{k}: {v:.2f}", fontsize=8)
        # =========================
        # 🕒 tick
        # =========================
        ax_world.set_title(f"TICK {tick} | FIELD: {current_field}")

        ax_world.set_xlim(0, 10)
        ax_world.set_ylim(0, 10)

        if paused:
            plt.pause(0.1)   # 🔥 慢刷新（允许交互）
        else:
            plt.pause(interval)
            tick_index += 1

    plt.ioff()
    plt.show()
selected_cell = None

# =========================
# 🔹 field heatmap（简易版）
# =========================
import numpy as np

def build_fake_field(cells, key="IL2_signal", size=10):
    grid = np.zeros((size, size))

    for c in cells.values():
        if "pos" not in c:
            continue

        x, y = c["pos"]
        val = c.get("node", {}).get(key, 0)

        xi = int(x)
        yi = int(y)

        if 0 <= xi < size and 0 <= yi < size:
            grid[yi][xi] += val  # 注意 y,x 顺序

    return grid
def extract_causal_chain(frame, prev_frame):
    chains = []

    for cid, cell in frame["cells"].items():
        prev = prev_frame["cells"].get(cid)
        if not prev:
            continue

        node = cell.get("node", {})
        prev_node = prev.get("node", {})

        chain = []

        # 🔶 行为触发
        for b in cell.get("behaviors", []):
            b_id = b["behavior_id"] if isinstance(b, dict) else b
            if b_id == "release_perforin":
                chain.append("perforin")

        # 🔥 delta 推导
        ca = node.get("Ca", node.get("Ca_signal", 0))
        prev_ca = prev_node.get("Ca", prev_node.get("Ca_signal", 0))

        if ca - prev_ca > 0.2:
            chain.append("Ca↑")

        if node.get("stress", 0) - prev_node.get("stress", 0) > 0.3:
            chain.append("stress↑")

        # ☠ fate
        for e in extract_events(frame):
            if e.get("type") == "cell_die" and str(e["target"]) == str(cid):
                chain.append("dying")

        if len(chain) >= 2:
            chains.append(f"{cid}: " + " → ".join(chain))

    return chains
def build_real_field(frame, substance="IL2", size=10):
    import numpy as np

    grid = np.zeros((size, size))

    fields = frame.get("fields", {})
    sub_field = fields.get(substance, {})

    for pos_str, val in sub_field.items():
        x, y = eval(pos_str)

        if 0 <= x < size and 0 <= y < size:
            grid[y][x] += val

    return grid
def draw_field(ax, grid, alpha=0.3):
    im = ax.imshow(
        grid,
        cmap="Reds",
        origin="lower",
        extent=(0, 10, 0, 10),
        alpha=alpha,
        interpolation="bilinear"
    )
    return im   # 🔥 加这一行
def extract_events(frame):
    events = []

    raw = frame.get("events", [])

    for item in raw:
        if isinstance(item, dict) and "events" in item:
            events.extend(item["events"])
        elif isinstance(item, dict):
            events.append(item)

    return events
def draw_event_overlay(ax, lines, max_lines=6):

    # 只显示最后几条（滚动效果）
    lines = lines[-max_lines:]

    y = 0.85  # 避开 tick

    for line in lines:

        if "☠" in line:
            color = "red"
        elif "🔥" in line:
            color = "orange"
        elif "⚠" in line:
            color = "yellow"
        elif "🔶" in line:
            color = "cyan"
        else:
            color = "white"

        ax.text(
            0.02, y,
            line,
            transform=ax.transAxes,
            fontsize=10,
            color=color,
            verticalalignment='top',
            bbox=dict(
                facecolor='black',
                alpha=0.4,
                edgecolor='none'
            )
        )

        y -= 0.05
current_cells = {}
selected_cell = None
# =========================
# 🔹 main
# =========================
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python plot_line.py <config.json>")
        sys.exit(1)

    config = load_json(sys.argv[1])
    data = load_json(config["input"])

    plot_type = config["type"]

    if plot_type == "event_log":
        logs = generate_event_log(data)

        for log in logs:
            print("\n".join(log["lines"]))
    elif plot_type == "2d":
        plot_2d_world(data)
    else:
        raise ValueError(f"Unknown plot type: {plot_type}")
        
