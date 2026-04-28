# Internalnet/HIR/hir_core.py

import os
import json

from .hir_engine import run_hir


# =========================
# load config（只加载一次）
# =========================

_HIR_CONFIG = None


def load_hir_config():
    global _HIR_CONFIG

    if _HIR_CONFIG is not None:
        return _HIR_CONFIG

    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, "hir.json")

    with open(path) as f:
        _HIR_CONFIG = json.load(f)

    return _HIR_CONFIG


# =========================
# 主入口（唯一对外接口）
# =========================

def compute_HIR(node_state, cell=None):
    """
    🔥 v0.5 标准入口（唯一合法调用方式）

    输入：
        node_state: 当前节点状态
        cell: 可选（未来用于 cell-specific 参数）

    输出：
        {
            fate,
            scores,
            group_modifiers,
            blocks
        }
    """

    hir_cfg = load_hir_config()

    # 👉 未来扩展点（现在先留空）
    # if cell:
    #     apply cell-specific overrides

    result = run_hir(node_state, hir_cfg)

    return result
