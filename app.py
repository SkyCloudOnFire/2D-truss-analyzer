"""
2D Truss Analyzer
Clean, professional structural analysis tool
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrowPatch, Circle, Polygon
import io
import time

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="2D Truss Analyzer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clean modern styling - no forced theme
st.markdown("""
<style>
    /* Clean inputs */
    .stTextInput input, .stNumberInput input {
        border-radius: 8px !important;
        border: 1px solid #d0d5dd !important;
        padding: 0.5rem 0.75rem !important;
        font-size: 0.95rem !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
        outline: none !important;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        padding: 0.5rem 1.25rem !important;
        transition: all 0.15s !important;
        border: 1px solid #d0d5dd !important;
        background: #ffffff !important;
        color: #1a1a1a !important;
    }
    
    .stButton > button:hover {
        border-color: #2563eb !important;
        background: #f8faff !important;
    }
    
    .stButton > button:active {
        background: #eef2ff !important;
    }
    
    /* Primary button */
    .stButton > button[kind="primary"] {
        background: #2563eb !important;
        color: white !important;
        border-color: #2563eb !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #1d4ed8 !important;
    }
    
    /* Danger button */
    .danger-button > button {
        color: #dc2626 !important;
        border-color: #fca5a5 !important;
    }
    
    .danger-button > button:hover {
        background: #fef2f2 !important;
        border-color: #dc2626 !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        border: 1px solid #e5e7eb !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    
    .stDataFrame th {
        background: #f9fafb !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        color: #6b7280 !important;
        border-bottom: 2px solid #e5e7eb !important;
        padding: 0.6rem 0.75rem !important;
    }
    
    .stDataFrame td {
        padding: 0.5rem 0.75rem !important;
        font-size: 0.9rem !important;
        border-bottom: 1px solid #f3f4f6 !important;
    }
    
    .stDataFrame tr:hover td {
        background: #f9fafb !important;
        cursor: pointer !important;
    }
    
    /* Selected row */
    .stDataFrame tr[aria-selected="true"] td {
        background: #eff6ff !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px !important;
        background: #f3f4f6 !important;
        border-radius: 10px !important;
        padding: 3px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: #6b7280 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #2563eb !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
    }
    
    /* Cards */
    .card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.25rem;
    }
    
    /* Title */
    .app-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1a1a1a;
        letter-spacing: -0.3px;
    }
    
    /* Section label */
    .section-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #9ca3af;
        margin-bottom: 0.5rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Smooth scroll */
    html {scroll-behavior: smooth;}
    
    /* Number input - remove spinners */
    input[type="number"]::-webkit-inner-spin-button,
    input[type="number"]::-webkit-outer-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    input[type="number"] {
        -moz-appearance: textfield;
    }
    
    /* Placeholder styling */
    input::placeholder {
        color: #d1d5db !important;
        font-style: italic;
    }
</style>

<script>
    document.querySelector('meta[name="viewport"]').setAttribute('content', 
        'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes');
</script>
""", unsafe_allow_html=True)

# ============================================================================
# LANGUAGE
# ============================================================================

LANG = {
    "English": {
        "title": "2D Truss Analyzer",
        "language": "Language",
        "live_preview": "Preview",
        "nodes": "Nodes",
        "members": "Members",
        "supports": "Supports",
        "loads": "Loads",
        "analyze": "Analyze",
        "reset": "Reset",
        "node_name": "Node name",
        "x_coord": "X coordinate",
        "y_coord": "Y coordinate",
        "add_node": "Add node",
        "start_node": "Start node",
        "end_node": "End node",
        "add_member": "Add member",
        "support_node": "Node",
        "support_type": "Support type",
        "support_types": ["Pinned", "Roller (free X)", "Roller (free Y)"],
        "add_support": "Add support",
        "remove_support": "Remove support",
        "load_type": "Load type",
        "load_types": ["On node", "On member"],
        "load_node": "Node",
        "load_member": "Member",
        "load_position": "Position along member",
        "load_position_hint": "0 = start, 0.5 = middle, 1 = end",
        "load_magnitude": "Magnitude",
        "load_angle": "Angle from +X",
        "add_load": "Add load",
        "remove_load": "Remove selected",
        "nodes_table": "Nodes",
        "members_table": "Members",
        "supports_table": "Supports",
        "loads_table": "Loads",
        "tap_to_edit": "Tap a row to edit",
        "hold_to_delete": "Tap a row, then press Delete below",
        "delete_selected": "Delete selected",
        "reactions": "Support reactions",
        "member_forces": "Member forces",
        "displacements": "Displacements",
        "node": "Node",
        "fx": "Fx",
        "fy": "Fy",
        "resultant": "R",
        "angle": "Angle",
        "member": "Member",
        "length": "Length",
        "force": "Force",
        "type": "Type",
        "tension": "Tension",
        "compression": "Compression",
        "ux": "Ux",
        "uy": "Uy",
        "units_reaction": "kN",
        "units_force": "kN",
        "units_disp": "mm",
        "units_length": "m",
        "no_data": "Add nodes and members, then press Analyze.",
        "need_minimum": "At least 2 nodes and 1 member required.",
        "analysis_error": "Analysis failed. Check supports and geometry.",
        "legend_tension": "Tension",
        "legend_compression": "Compression",
        "legend_load": "Applied load",
        "legend_reaction": "Reaction",
        "export": "Export results",
    },
    "Persian": {
        "title": "تحلیل‌گر خرپا دوبعدی",
        "language": "زبان",
        "live_preview": "پیش‌نمایش",
        "nodes": "گره‌ها",
        "members": "اعضا",
        "supports": "تکیه‌گاه‌ها",
        "loads": "بارها",
        "analyze": "تحلیل",
        "reset": "بازنشانی",
        "node_name": "نام گره",
        "x_coord": "مختصات X",
        "y_coord": "مختصات Y",
        "add_node": "افزودن گره",
        "start_node": "گره آغاز",
        "end_node": "گره پایان",
        "add_member": "افزودن عضو",
        "support_node": "گره",
        "support_type": "نوع تکیه‌گاه",
        "support_types": ["گیردار", "غلتک (آزاد X)", "غلتک (آزاد Y)"],
        "add_support": "افزودن تکیه‌گاه",
        "remove_support": "حذف تکیه‌گاه",
        "load_type": "نوع بار",
        "load_types": ["روی گره", "روی عضو"],
        "load_node": "گره",
        "load_member": "عضو",
        "load_position": "موقعیت روی عضو",
        "load_position_hint": "0 = آغاز, 0.5 = وسط, 1 = پایان",
        "load_magnitude": "بزرگی",
        "load_angle": "زاویه از +X",
        "add_load": "افزودن بار",
        "remove_load": "حذف انتخاب",
        "nodes_table": "گره‌ها",
        "members_table": "اعضا",
        "supports_table": "تکیه‌گاه‌ها",
        "loads_table": "بارها",
        "tap_to_edit": "برای ویرایش روی یک ردیف بزنید",
        "hold_to_delete": "روی ردیف بزنید، سپس دکمه حذف را بفشارید",
        "delete_selected": "حذف انتخاب",
        "reactions": "عکس‌العمل‌های تکیه‌گاهی",
        "member_forces": "نیروهای اعضا",
        "displacements": "جابجایی‌ها",
        "node": "گره",
        "fx": "Fx",
        "fy": "Fy",
        "resultant": "برآیند",
        "angle": "زاویه",
        "member": "عضو",
        "length": "طول",
        "force": "نیرو",
        "type": "نوع",
        "tension": "کشش",
        "compression": "فشار",
        "ux": "Ux",
        "uy": "Uy",
        "units_reaction": "kN",
        "units_force": "kN",
        "units_disp": "mm",
        "units_length": "m",
        "no_data": "گره‌ها و اعضا را تعریف کرده، سپس تحلیل را بزنید.",
        "need_minimum": "حداقل ۲ گره و ۱ عضو الزامی است.",
        "analysis_error": "تحلیل ناموفق. تکیه‌گاه‌ها و هندسه را بررسی کنید.",
        "legend_tension": "کشش",
        "legend_compression": "فشار",
        "legend_load": "بار اعمالی",
        "legend_reaction": "عکس‌العمل",
        "export": "خروجی نتایج",
    }
}

# ============================================================================
# TRUSS SOLVER - Supports loads anywhere on member
# ============================================================================

class TrussAnalyzer:
    def __init__(self, nodes_dict, members_list, supports_dict, joint_loads_dict, member_loads_list):
        self.node_names = list(nodes_dict.keys())
        self.node_coords = {n: nodes_dict[n] for n in self.node_names}
        self.node_idx = {n: i for i, n in enumerate(self.node_names)}
        self.n_nodes = len(self.node_names)
        self.n_dofs = 2 * self.n_nodes
        
        self.members = members_list  # [(name, n1, n2)]
        self.supports = supports_dict  # {node: type}
        self.joint_loads = joint_loads_dict  # {node: (mag, ang)}
        self.member_loads = member_loads_list  # [(load_name, member, position, mag, ang)]
        
        self.E = 200e6
        self.A = 0.01
        
        self.K = np.zeros((self.n_dofs, self.n_dofs))
        self.F = np.zeros(self.n_dofs)
        self.U = None
        self.member_forces = {}
        self.reactions = {}
        
        self._assemble_stiffness()
        self._apply_loads()
        self._apply_supports()
        self._solve()
    
    def _dof(self, name):
        i = self.node_idx[name]
        return 2*i, 2*i+1
    
    def _assemble_stiffness(self):
        for mname, n1, n2 in self.members:
            x1, y1 = self.node_coords[n1]
            x2, y2 = self.node_coords[n2]
            dx, dy = x2-x1, y2-y1
            L = np.sqrt(dx**2 + dy**2)
            if L < 1e-10: continue
            c, s = dx/L, dy/L
            
            k = (self.E * self.A / L) * np.array([
                [c*c, c*s, -c*c, -c*s],
                [c*s, s*s, -c*s, -s*s],
                [-c*c, -c*s, c*c, c*s],
                [-c*s, -s*s, c*s, s*s]
            ])
            
            d1x, d1y = self._dof(n1)
            d2x, d2y = self._dof(n2)
            for ii, gi in enumerate([d1x, d1y, d2x, d2y]):
                for jj, gj in enumerate([d1x, d1y, d2x, d2y]):
                    self.K[gi, gj] += k[ii, jj]
    
    def _apply_loads(self):
        # Joint loads
        for node, (mag, ang) in self.joint_loads.items():
            r = np.radians(ang)
            dx, dy = self._dof(node)
            self.F[dx] += mag * np.cos(r)
            self.F[dy] += mag * np.sin(r)
        
        # Member loads at any position
        for lname, mname, pos, mag, ang in self.member_loads:
            for mn, n1, n2 in self.members:
                if mn == mname:
                    x1, y1 = self.node_coords[n1]
                    x2, y2 = self.node_coords[n2]
                    L = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                    if L < 1e-10: break
                    c, s = (x2-x1)/L, (y2-y1)/L
                    r = np.radians(ang)
                    
                    # Force components in global
                    fx = mag * np.cos(r)
                    fy = mag * np.sin(r)
                    
                    # Axial component along member
                    axial = fx * c + fy * s
                    
                    # Position ratios for equivalent nodal loads
                    a = pos      # distance ratio from start
                    b = 1 - pos  # distance ratio from end
                    
                    d1x, d1y = self._dof(n1)
                    d2x, d2y = self._dof(n2)
                    
                    self.F[d1x] += axial * c * b
                    self.F[d1y] += axial * s * b
                    self.F[d2x] += axial * c * a
                    self.F[d2y] += axial * s * a
                    break
    
    def _apply_supports(self):
        penalty = 1e15
        for node, stype in self.supports.items():
            dx, dy = self._dof(node)
            if stype == 'pinned':
                self.K[dx, dx] += penalty
                self.K[dy, dy] += penalty
            elif stype == 'roller_x':
                self.K[dy, dy] += penalty
            elif stype == 'roller_y':
                self.K[dx, dx] += penalty
    
    def _solve(self):
        try:
            self.U = np.linalg.solve(self.K, self.F)
            
            for mname, n1, n2 in self.members:
                x1, y1 = self.node_coords[n1]
                x2, y2 = self.node_coords[n2]
                dx, dy = x2-x1, y2-y1
                L = np.sqrt(dx**2+dy**2)
                if L < 1e-10: 
                    self.member_forces[mname] = 0
                    continue
                c, s = dx/L, dy/L
                d1x, d1y = self._dof(n1)
                d2x, d2y = self._dof(n2)
                u1, v1 = self.U[d1x], self.U[d1y]
                u2, v2 = self.U[d2x], self.U[d2y]
                force = (self.E * self.A / L) * (c*(u2-u1) + s*(v2-v1))
                self.member_forces[mname] = force
            
            for node in self.supports:
                dx, dy = self._dof(node)
                rx = np.dot(self.K[dx, :], self.U) - self.F[dx]
                ry = np.dot(self.K[dy, :], self.U) - self.F[dy]
                self.reactions[node] = (rx, ry)
        except:
            self.U = None

# ============================================================================
# VISUALIZATION
# ============================================================================

def draw_truss(nodes_dict, members_list, supports_dict, joint_loads, member_loads,
               member_forces=None, reactions=None, lang=None, show_results=False):
    if lang is None:
        lang = LANG["English"]
    
    fig, ax = plt.subplots(figsize=(11, 9))
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2, linestyle='-', color='#d0d5dd')
    ax.set_xlabel('X (m)', fontsize=10, color='#6b7280')
    ax.set_ylabel('Y (m)', fontsize=10, color='#6b7280')
    ax.tick_params(labelsize=8, colors='#9ca3af')
    for spine in ax.spines.values():
        spine.set_color('#e5e7eb')
    
    xs = [c[0] for c in nodes_dict.values()]
    ys = [c[1] for c in nodes_dict.values()]
    if not xs:
        xs, ys = [0, 10], [0, 10]
    
    margin = max(max(xs)-min(xs), max(ys)-min(ys), 2) * 0.25 + 1.5
    ax.set_xlim(min(xs)-margin, max(xs)+margin)
    ax.set_ylim(min(ys)-margin, max(ys)+margin)
    
    # Members
    for mname, n1, n2 in members_list:
        x1, y1 = nodes_dict[n1]
        x2, y2 = nodes_dict[n2]
        
        if show_results and member_forces and mname in member_forces:
            f = member_forces[mname]
            color = '#2563eb' if f >= 0 else '#dc2626'
            lw = 3.5
        else:
            color = '#9ca3af'
            lw = 2
        
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, zorder=2, solid_capstyle='round')
        
        mx, my = (x1+x2)/2, (y1+y2)/2
        L = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        
        if show_results and member_forces and mname in member_forces:
            fv = abs(member_forces[mname])
            ft = 'T' if member_forces[mname] >= 0 else 'C'
            label = f'{mname}\n{fv:.1f} kN ({ft})'
        else:
            label = f'{mname}\n{L:.2f} m'
        
        ax.annotate(label, (mx, my), fontsize=7, ha='center', va='center',
                   color='#374151', fontweight='600',
                   bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                            edgecolor='#e5e7eb', alpha=0.92))
    
    # Nodes
    for name, (x, y) in nodes_dict.items():
        ax.plot(x, y, 'o', color='#2563eb', markersize=9, zorder=5, markeredgecolor='white', markeredgewidth=2)
        ax.annotate(name, (x, y), fontsize=9, fontweight='700', color='#1a1a1a',
                   xytext=(8, 8), textcoords='offset points')
    
    # Supports
    for node, stype in supports_dict.items():
        x, y = nodes_dict[node]
        if stype == 'pinned':
            tri = Polygon([[x-0.5, y-0.5], [x+0.5, y-0.5], [x, y-0.02]],
                         facecolor='#6b7280', edgecolor='#374151', zorder=3, linewidth=1.2)
            ax.add_patch(tri)
            for i in range(4):
                ax.plot([x-0.45+i*0.3, x-0.4+i*0.3], [y-0.5, y-0.65],
                       color='#374151', linewidth=1)
        elif stype == 'roller_x':
            circ = Circle((x, y-0.3), 0.2, facecolor='white', edgecolor='#374151', zorder=3, linewidth=1.2)
            ax.add_patch(circ)
            ax.plot([x-0.5, x+0.5], [y-0.6, y-0.6], color='#374151', linewidth=1.2)
        elif stype == 'roller_y':
            circ = Circle((x-0.3, y), 0.2, facecolor='white', edgecolor='#374151', zorder=3, linewidth=1.2)
            ax.add_patch(circ)
            ax.plot([x-0.6, x-0.6], [y-0.5, y+0.5], color='#374151', linewidth=1.2)
    
    # Scale
    all_f = [mag for mag, _ in joint_loads.values()]
    for _, _, _, mag, _ in member_loads:
        all_f.append(mag)
    max_f = max(all_f) if all_f else 1
    scale = (max(xs)-min(xs)) / max_f * 0.18 if max_f > 0 else 0.5
    
    # Joint loads
    for node, (mag, ang) in joint_loads.items():
        x, y = nodes_dict[node]
        r = np.radians(ang)
        dx = -mag * np.cos(r) * scale
        dy = -mag * np.sin(r) * scale
        ax.arrow(x+dx, y+dy, -dx*0.85, -dy*0.85,
                head_width=0.2, head_length=0.3, fc='#059669', ec='#059669',
                linewidth=2.2, zorder=7)
        ax.annotate(f'{mag:.1f} kN', (x+dx*1.15, y+dy*1.15),
                   fontsize=7, color='#059669', fontweight='600')
    
    # Member loads at any position
    for lname, mname, pos, mag, ang in member_loads:
        for mn, n1, n2 in members_list:
            if mn == mname:
                x1, y1 = nodes_dict[n1]
                x2, y2 = nodes_dict[n2]
                px = x1 + pos*(x2-x1)
                py = y1 + pos*(y2-y1)
                r = np.radians(ang)
                dx = -mag * np.cos(r) * scale
                dy = -mag * np.sin(r) * scale
                ax.arrow(px+dx, py+dy, -dx*0.85, -dy*0.85,
                        head_width=0.2, head_length=0.3, fc='#d97706', ec='#d97706',
                        linewidth=2.2, zorder=7)
                ax.annotate(f'{lname}\n{mag:.1f} kN', (px+dx*1.15, py+dy*1.15),
                           fontsize=6.5, color='#d97706', fontweight='600')
                break
    
    # Reactions
    if show_results and reactions:
        for node, (rx, ry) in reactions.items():
            x, y = nodes_dict[node]
            if abs(rx) > 0.01 or abs(ry) > 0.01:
                dx, dy = rx*scale*0.7, ry*scale*0.7
                ax.arrow(x-dx, y-dy, dx*0.85, dy*0.85,
                        head_width=0.2, head_length=0.3, fc='#7c3aed', ec='#7c3aed',
                        linewidth=2.8, zorder=7)
                R = np.sqrt(rx**2+ry**2)
                ax.annotate(f'{R:.1f} kN', (x-dx*1.15, y-dy*1.15),
                           fontsize=7, color='#7c3aed', fontweight='600')
    
    # Legend
    if show_results:
        legend = f'{lang["legend_tension"]} | {lang["legend_compression"]} | {lang["legend_load"]} | {lang["legend_reaction"]}'
        ax.text(0.5, 1.02, legend, transform=ax.transAxes, fontsize=7,
               color='#6b7280', ha='center',
               bbox=dict(boxstyle='round', facecolor='white', edgecolor='#e5e7eb', alpha=0.9))
    
    plt.tight_layout()
    return fig

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Init session state
    defaults = {
        'language': 'English',
        'nodes': {},
        'members': [],
        'supports': {},
        'joint_loads': {},
        'member_loads': [],
        'results': None,
        'selected_node': None,
        'selected_member': None,
        'selected_support_node': None,
        'form_node_name': '',
        'form_node_x': '',
        'form_node_y': '',
        'form_member_start': '',
        'form_member_end': '',
        'form_support_node': '',
        'form_support_type': '',
        'form_load_type': '',
        'form_load_name': '',
        'form_load_location': '',
        'form_load_position': '',
        'form_load_mag': '',
        'form_load_ang': '',
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    
    lang = LANG[st.session_state.language]
    
    # Header - clean
    col_lang, col_title = st.columns([1, 6])
    with col_lang:
        st.session_state.language = st.selectbox(
            "", ["English", "Persian"], label_visibility="collapsed", key="lang_sel"
        )
    
    st.markdown(f'<div class="app-title">{lang["title"]}</div>', unsafe_allow_html=True)
    
    # Main layout
    left, right = st.columns([1, 1.1])
    
    # ===== RIGHT: Live Preview =====
    with right:
        st.markdown(f'<div class="section-label">{lang["live_preview"]}</div>', unsafe_allow_html=True)
        
        show_results = st.session_state.results is not None
        fig = draw_truss(
            st.session_state.nodes,
            st.session_state.members,
            st.session_state.supports,
            st.session_state.joint_loads,
            st.session_state.member_loads,
            member_forces=st.session_state.results.get('member_forces') if show_results else None,
            reactions=st.session_state.results.get('reactions') if show_results else None,
            lang=lang,
            show_results=show_results
        )
        st.pyplot(fig)
    
    # ===== LEFT: Input =====
    with left:
        tabs = st.tabs([lang["nodes"], lang["members"], lang["supports"], lang["loads"]])
        
        # ---- NODES ----
        with tabs[0]:
            # Table
            if st.session_state.nodes:
                data = [{"Name": n, "X": x, "Y": y} for n, (x, y) in st.session_state.nodes.items()]
                df = pd.DataFrame(data)
                st.caption(lang["tap_to_edit"])
                sel = st.dataframe(df, hide_index=True, use_container_width=True,
                                  selection_mode="single-row", on_select="rerun", key="tbl_nodes")
                if sel and len(sel.selection.rows) > 0:
                    idx = sel.selection.rows[0]
                    name = list(st.session_state.nodes.keys())[idx]
                    st.session_state.selected_node = name
                    st.session_state.form_node_name = name
                    st.session_state.form_node_x = str(st.session_state.nodes[name][0])
                    st.session_state.form_node_y = str(st.session_state.nodes[name][1])
            
            # Delete button - right below table
            if st.session_state.selected_node and st.session_state.selected_node in st.session_state.nodes:
                if st.button(lang["delete_selected"], key="del_node", 
                           type="secondary"):
                    name = st.session_state.selected_node
                    del st.session_state.nodes[name]
                    st.session_state.members = [m for m in st.session_state.members if m[1] != name and m[2] != name]
                    st.session_state.supports.pop(name, None)
                    st.session_state.joint_loads.pop(name, None)
                    st.session_state.selected_node = None
                    st.session_state.form_node_name = ''
                    st.session_state.form_node_x = ''
                    st.session_state.form_node_y = ''
                    st.rerun()
            
            # Form - keeps values
            c1, c2, c3 = st.columns(3)
            with c1:
                node_name = st.text_input(lang["node_name"], 
                                         value=st.session_state.form_node_name,
                                         placeholder="A", key="inp_nname",
                                         label_visibility="collapsed")
            with c2:
                node_x = st.text_input(lang["x_coord"],
                                      value=st.session_state.form_node_x,
                                      placeholder="0", key="inp_nx",
                                      label_visibility="collapsed")
            with c3:
                node_y = st.text_input(lang["y_coord"],
                                      value=st.session_state.form_node_y,
                                      placeholder="0", key="inp_ny",
                                      label_visibility="collapsed")
            
            # Save form values so they persist
            st.session_state.form_node_name = node_name
            st.session_state.form_node_x = node_x
            st.session_state.form_node_y = node_y
            
            if st.button(lang["add_node"], key="btn_add_node", use_container_width=True):
                if node_name:
                    try:
                        xf = float(node_x) if node_x else 0.0
                        yf = float(node_y) if node_y else 0.0
                        st.session_state.nodes[node_name] = (xf, yf)
                        st.session_state.selected_node = node_name
                        st.session_state.form_node_name = ''
                        st.session_state.form_node_x = ''
                        st.session_state.form_node_y = ''
                        st.rerun()
                    except ValueError:
                        st.error("Coordinates must be numbers. Please fix and try again.")
        
        # ---- MEMBERS ----
        with tabs[1]:
            if st.session_state.members:
                data = []
                for mname, n1, n2 in st.session_state.members:
                    x1, y1 = st.session_state.nodes.get(n1, (0,0))
                    x2, y2 = st.session_state.nodes.get(n2, (0,0))
                    L = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                    data.append({"Member": mname, "Start": n1, "End": n2, "Length": f"{L:.2f} m"})
                df = pd.DataFrame(data)
                st.caption(lang["tap_to_edit"])
                sel = st.dataframe(df, hide_index=True, use_container_width=True,
                                  selection_mode="single-row", on_select="rerun", key="tbl_members")
                if sel and len(sel.selection.rows) > 0:
                    idx = sel.selection.rows[0]
                    mname = st.session_state.members[idx][0]
                    st.session_state.selected_member = mname
                    st.session_state.form_member_start = st.session_state.members[idx][1]
                    st.session_state.form_member_end = st.session_state.members[idx][2]
            
            if st.session_state.selected_member:
                if st.button(lang["delete_selected"], key="del_member", type="secondary"):
                    st.session_state.members = [m for m in st.session_state.members if m[0] != st.session_state.selected_member]
                    st.session_state.member_loads = [l for l in st.session_state.member_loads if l[1] != st.session_state.selected_member]
                    st.session_state.selected_member = None
                    st.rerun()
            
            node_names = list(st.session_state.nodes.keys())
            c1, c2 = st.columns(2)
            with c1:
                s_idx = node_names.index(st.session_state.form_member_start) if st.session_state.form_member_start in node_names else 0
                start_n = st.selectbox(lang["start_node"], node_names if node_names else ["-"],
                                      index=s_idx, key="sel_mstart")
            with c2:
                e_idx = node_names.index(st.session_state.form_member_end) if st.session_state.form_member_end in node_names else (1 if len(node_names)>1 else 0)
                end_n = st.selectbox(lang["end_node"], node_names if node_names else ["-"],
                                    index=e_idx, key="sel_mend")
            
            st.session_state.form_member_start = start_n
            st.session_state.form_member_end = end_n
            
            if st.button(lang["add_member"], key="btn_add_member", use_container_width=True):
                if start_n and end_n and start_n != end_n and start_n != "-" and end_n != "-":
                    mname = f"{start_n}{end_n}"
                    # Check if already exists
                    if not any(m[0] == mname for m in st.session_state.members):
                        st.session_state.members.append((mname, start_n, end_n))
                        st.session_state.selected_member = mname
                        st.rerun()
                    else:
                        st.error("This member already exists.")
        
        # ---- SUPPORTS ----
        with tabs[2]:
            if st.session_state.supports:
                data = [{"Node": n, "Type": t} for n, t in st.session_state.supports.items()]
                df = pd.DataFrame(data)
                st.caption(lang["tap_to_edit"])
                sel = st.dataframe(df, hide_index=True, use_container_width=True,
                                  selection_mode="single-row", on_select="rerun", key="tbl_supports")
                if sel and len(sel.selection.rows) > 0:
                    idx = sel.selection.rows[0]
                    sname = list(st.session_state.supports.keys())[idx]
                    st.session_state.selected_support_node = sname
                    st.session_state.form_support_node = sname
                    st.session_state.form_support_type = st.session_state.supports[sname]
            
            if st.session_state.selected_support_node:
                if st.button(lang["remove_support"], key="del_support", type="secondary"):
                    del st.session_state.supports[st.session_state.selected_support_node]
                    st.session_state.selected_support_node = None
                    st.rerun()
            
            node_names = list(st.session_state.nodes.keys())
            c1, c2 = st.columns(2)
            with c1:
                s_idx = node_names.index(st.session_state.form_support_node) if st.session_state.form_support_node in node_names else 0
                sup_node = st.selectbox(lang["support_node"], node_names if node_names else ["-"],
                                       index=s_idx, key="sel_snode")
            with c2:
                type_map_rev = {'pinned': lang["support_types"][0], 'roller_x': lang["support_types"][1], 'roller_y': lang["support_types"][2]}
                current_type = st.session_state.form_support_type
                t_idx = lang["support_types"].index(type_map_rev.get(current_type, lang["support_types"][0])) if current_type else 0
                sup_type = st.selectbox(lang["support_type"], lang["support_types"],
                                       index=t_idx, key="sel_stype")
            
            st.session_state.form_support_node = sup_node
            st.session_state.form_support_type = sup_type
            
            if st.button(lang["add_support"], key="btn_add_support", use_container_width=True):
                if sup_node and sup_node != "-":
                    type_map = {
                        lang["support_types"][0]: 'pinned',
                        lang["support_types"][1]: 'roller_x',
                        lang["support_types"][2]: 'roller_y'
                    }
                    st.session_state.supports[sup_node] = type_map[sup_type]
                    st.rerun()
        
        # ---- LOADS ----
        with tabs[3]:
            all_loads = []
            for node, (mag, ang) in st.session_state.joint_loads.items():
                all_loads.append({"Type": "Node", "Location": node, "kN": mag, "deg": ang})
            for lname, mname, pos, mag, ang in st.session_state.member_loads:
                all_loads.append({"Type": "Member", "Location": f"{mname} @ {pos:.2f}", "kN": mag, "deg": ang, "Name": lname})
            
            if all_loads:
                df = pd.DataFrame(all_loads)
                st.caption(lang["tap_to_edit"])
                st.dataframe(df, hide_index=True, use_container_width=True)
            
            load_type = st.selectbox(lang["load_type"], lang["load_types"], key="sel_ltype")
            st.session_state.form_load_type = load_type
            
            if load_type == lang["load_types"][0]:  # On node
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    load_name = st.text_input(lang["load_type"].replace("Type","Name"), 
                                             value=st.session_state.form_load_name,
                                             placeholder="F1", key="inp_lname_n")
                with c2:
                    node_names = list(st.session_state.nodes.keys())
                    l_idx = node_names.index(st.session_state.form_load_location) if st.session_state.form_load_location in node_names else 0
                    load_at = st.selectbox(lang["load_node"], node_names if node_names else ["-"],
                                          index=l_idx, key="sel_lnode")
                with c3:
                    load_mag = st.text_input(lang["load_magnitude"],
                                            value=st.session_state.form_load_mag,
                                            placeholder="10", key="inp_lmag_n")
                with c4:
                    load_ang = st.text_input(lang["load_angle"],
                                            value=st.session_state.form_load_ang,
                                            placeholder="270", key="inp_lang_n")
                
                st.session_state.form_load_name = load_name
                st.session_state.form_load_location = load_at
                st.session_state.form_load_mag = load_mag
                st.session_state.form_load_ang = load_ang
                
                if st.button(lang["add_load"], key="btn_add_load_node", use_container_width=True):
                    if load_at and load_at != "-":
                        try:
                            mag_f = float(load_mag) if load_mag else 0
                            ang_f = float(load_ang) if load_ang else 0
                            st.session_state.joint_loads[load_at] = (mag_f, ang_f)
                            st.session_state.form_load_mag = ''
                            st.session_state.form_load_ang = ''
                            st.rerun()
                        except ValueError:
                            st.error("Magnitude and angle must be numbers.")
            
            else:  # On member
                c1, c2, c3, c4, c5 = st.columns(5)
                with c1:
                    load_name = st.text_input("Name", value=st.session_state.form_load_name,
                                             placeholder="W1", key="inp_lname_m")
                with c2:
                    mem_names = [m[0] for m in st.session_state.members]
                    l_idx = mem_names.index(st.session_state.form_load_location) if st.session_state.form_load_location in mem_names else 0
                    load_mem = st.selectbox(lang["load_member"], mem_names if mem_names else ["-"],
                                           index=l_idx, key="sel_lmem")
                with c3:
                    load_pos = st.text_input(lang["load_position"],
                                            value=st.session_state.form_load_position,
                                            placeholder="0.5", key="inp_lpos")
                    st.caption(lang["load_position_hint"])
                with c4:
                    load_mag = st.text_input(lang["load_magnitude"],
                                            value=st.session_state.form_load_mag,
                                            placeholder="10", key="inp_lmag_m")
                with c5:
                    load_ang = st.text_input(lang["load_angle"],
                                            value=st.session_state.form_load_ang,
                                            placeholder="270", key="inp_lang_m")
                
                st.session_state.form_load_name = load_name
                st.session_state.form_load_location = load_mem
                st.session_state.form_load_position = load_pos
                st.session_state.form_load_mag = load_mag
                st.session_state.form_load_ang = load_ang
                
                if st.button(lang["add_load"], key="btn_add_load_mem", use_container_width=True):
                    if load_mem and load_mem != "-":
                        try:
                            pos_f = float(load_pos) if load_pos else 0.5
                            mag_f = float(load_mag) if load_mag else 0
                            ang_f = float(load_ang) if load_ang else 0
                            pos_f = max(0, min(1, pos_f))
                            st.session_state.member_loads.append((load_name, load_mem, pos_f, mag_f, ang_f))
                            st.session_state.form_load_name = ''
                            st.session_state.form_load_position = ''
                            st.session_state.form_load_mag = ''
                            st.session_state.form_load_ang = ''
                            st.rerun()
                        except ValueError:
                            st.error("Position, magnitude, and angle must be numbers.")
            
            # Remove all loads button
            if all_loads:
                if st.button(lang["remove_load"], key="btn_clear_loads", type="secondary"):
                    st.session_state.joint_loads = {}
                    st.session_state.member_loads = []
                    st.rerun()
    
    # ===== ACTION BUTTONS =====
    st.markdown("---")
    c1, c2 = st.columns([3, 1])
    with c1:
        if st.button(lang["analyze"], type="primary", use_container_width=True, key="btn_analyze"):
            if len(st.session_state.nodes) >= 2 and len(st.session_state.members) >= 1:
                with st.spinner(""):
                    try:
                        analyzer = TrussAnalyzer(
                            st.session_state.nodes,
                            st.session_state.members,
                            st.session_state.supports,
                            st.session_state.joint_loads,
                            st.session_state.member_loads
                        )
                        if analyzer.U is not None:
                            st.session_state.results = {
                                'reactions': analyzer.reactions,
                                'member_forces': analyzer.member_forces,
                                'displacements': analyzer.U,
                                'node_names': analyzer.node_names
                            }
                            st.rerun()
                        else:
                            st.error(lang["analysis_error"])
                    except Exception as e:
                        st.error(f"{lang['analysis_error']}: {e}")
            else:
                st.warning(lang["need_minimum"])
    
    with c2:
        if st.button(lang["reset"], use_container_width=True, key="btn_reset"):
            for k in ['nodes', 'members', 'supports', 'joint_loads', 'member_loads', 'results',
                     'selected_node', 'selected_member', 'selected_support_node',
                     'form_node_name', 'form_node_x', 'form_node_y',
                     'form_member_start', 'form_member_end',
                     'form_support_node', 'form_support_type',
                     'form_load_name', 'form_load_location', 'form_load_position', 'form_load_mag', 'form_load_ang']:
                st.session_state[k] = {} if k in ['nodes', 'supports', 'joint_loads', 'results'] else ('' if 'form_' in k else [])
            st.rerun()
    
    # ===== RESULTS (below drawing) =====
    if st.session_state.results:
        st.markdown("---")
        res = st.session_state.results
        
        r1, r2, r3 = st.columns(3)
        
        with r1:
            st.markdown(f"**{lang['reactions']}**")
            if res['reactions']:
                rd = []
                for n, (fx, fy) in res['reactions'].items():
                    R = np.sqrt(fx**2+fy**2)
                    a = np.degrees(np.arctan2(fy, fx))
                    rd.append({lang['node']: n, lang['fx']: f"{fx:.2f}", lang['fy']: f"{fy:.2f}",
                              lang['resultant']: f"{R:.2f}", lang['angle']: f"{a:.1f}"})
                st.dataframe(pd.DataFrame(rd), hide_index=True, use_container_width=True)
        
        with r2:
            st.markdown(f"**{lang['member_forces']}**")
            if res['member_forces']:
                fd = []
                for m, f in res['member_forces'].items():
                    fd.append({lang['member']: m, lang['force']: f"{abs(f):.2f}",
                              lang['type']: lang['tension'] if f>=0 else lang['compression']})
                st.dataframe(pd.DataFrame(fd), hide_index=True, use_container_width=True)
        
        with r3:
            st.markdown(f"**{lang['displacements']}**")
            dd = []
            for i, n in enumerate(res['node_names']):
                ux = res['displacements'][2*i] * 1000
                uy = res['displacements'][2*i+1] * 1000
                dd.append({lang['node']: n, lang['ux']: f"{ux:.3f}", lang['uy']: f"{uy:.3f}"})
            st.dataframe(pd.DataFrame(dd), hide_index=True, use_container_width=True)
        
        if st.button(lang["export"]):
            buf = io.StringIO()
            buf.write("2D TRUSS ANALYSIS\n" + "="*40 + "\n\n")
            buf.write("REACTIONS:\n")
            for n, (fx, fy) in res['reactions'].items():
                buf.write(f"  {n}: Fx={fx:.2f}, Fy={fy:.2f}, R={np.sqrt(fx**2+fy**2):.2f}\n")
            buf.write("\nMEMBER FORCES:\n")
            for m, f in res['member_forces'].items():
                buf.write(f"  {m}: {abs(f):.2f} kN ({'T' if f>=0 else 'C'})\n")
            buf.write("\nDISPLACEMENTS:\n")
            for i, n in enumerate(res['node_names']):
                buf.write(f"  {n}: Ux={res['displacements'][2*i]*1000:.3f} mm, Uy={res['displacements'][2*i+1]*1000:.3f} mm\n")
            st.download_button("Download", buf.getvalue(), "truss_results.txt", "text/plain")

if __name__ == "__main__":
    main()