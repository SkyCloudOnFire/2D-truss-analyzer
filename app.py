"""
2D Truss Analysis System - Professional Edition v3
Features: Named nodes, editable tables, persistent live preview, clean UI
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrowPatch, Circle, Polygon
import io
import time

# ============================================================================
# PAGE CONFIG - Dark theme, no animations
# ============================================================================

st.set_page_config(
    page_title="2D Truss Analysis Pro",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Force dark theme everywhere
st.markdown("""
<style>
    /* Force dark theme */
    .stApp, .main, body {
        background-color: #0d1117 !important;
        color: #e6edf3 !important;
    }
    
    /* Remove status animations */
    .stStatusWidget, [data-testid="stStatusWidget"] {
        display: none !important;
    }
    
    /* Custom spinner only */
    .stSpinner > div {
        border-color: #4a90e2 !important;
    }
    
    /* Input fields */
    .stTextInput input, .stNumberInput input, .stSelectbox > div > div {
        background-color: #161b22 !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #4a90e2 !important;
        box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1e3c72, #2a5298) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.2s !important;
        letter-spacing: 0.3px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(30, 60, 114, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Dataframe tables */
    .stDataFrame {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
    }
    
    .stDataFrame [data-testid="stTable"] {
        background-color: transparent !important;
    }
    
    .stDataFrame th {
        background-color: #1c2333 !important;
        color: #4a90e2 !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #30363d !important;
    }
    
    .stDataFrame td {
        background-color: #161b22 !important;
        color: #e6edf3 !important;
        border-bottom: 1px solid #21262d !important;
    }
    
    .stDataFrame tr:hover td {
        background-color: #1c2333 !important;
        cursor: pointer !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #161b22 !important;
        border-radius: 10px !important;
        padding: 4px !important;
        gap: 4px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #8b949e !important;
        background: transparent !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
        transition: all 0.2s !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e3c72, #2a5298) !important;
        color: white !important;
    }
    
    /* Cards */
    .input-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .preview-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1rem;
        position: sticky;
        top: 1rem;
    }
    
    /* Headers */
    .section-title {
        color: #4a90e2;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #1e3c72;
    }
    
    .main-title {
        background: linear-gradient(135deg, #4a90e2, #2a5298, #1e3c72);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #4a90e2; }
    
    /* Success/Info messages */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 8px !important;
        border: 1px solid #30363d !important;
    }
    
    /* Remove extra padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
</style>

<script>
    document.querySelector('meta[name="viewport"]').setAttribute('content', 
        'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes');
</script>
""", unsafe_allow_html=True)

# ============================================================================
# LANGUAGE SYSTEM
# ============================================================================

LANGUAGES = {
    "English": {
        "title": "2D Truss Analysis System",
        "subtitle": "Professional Matrix Stiffness Method Solver",
        "language": "Language",
        "live_preview": "Live Preview",
        "node_tab": "Nodes",
        "member_tab": "Members",
        "support_tab": "Supports",
        "load_tab": "Loads",
        "analyze": "Analyze Structure",
        "reset": "Reset All",
        "node_name": "Node Name",
        "x_coord": "X (m)",
        "y_coord": "Y (m)",
        "add_node": "Add Node",
        "update_node": "Update Selected",
        "delete_node": "Delete Selected",
        "member_name": "Member Name",
        "start_node": "Start Node",
        "end_node": "End Node",
        "add_member": "Add Member",
        "update_member": "Update Selected",
        "delete_member": "Delete Selected",
        "support_node": "Node",
        "support_type": "Support Type",
        "support_types": ["Pinned (Fix X, Y)", "Roller X (Free X)", "Roller Y (Free Y)"],
        "add_support": "Add Support",
        "delete_support": "Delete Selected",
        "load_type": "Load Type",
        "load_types": ["Joint Load", "Mid-Member Load"],
        "load_name": "Load Name",
        "load_location": "At Node",
        "load_member": "On Member",
        "load_magnitude": "Magnitude (kN)",
        "load_angle": "Angle (° from +X)",
        "add_load": "Add Load",
        "delete_load": "Delete Selected",
        "nodes_table": "Node Coordinates",
        "members_table": "Member Connectivity",
        "supports_table": "Support Conditions",
        "loads_table": "Applied Loads",
        "select_row": "Click a row to edit/delete",
        "reactions": "Support Reactions",
        "member_forces": "Member Forces",
        "displacements": "Nodal Displacements",
        "node_col": "Node",
        "fx": "Fx (kN)",
        "fy": "Fy (kN)",
        "resultant": "R (kN)",
        "angle": "Angle (°)",
        "member_col": "Member",
        "force": "Force (kN)",
        "type": "Type",
        "tension": "TENSION",
        "compression": "COMPRESSION",
        "ux": "Ux (mm)",
        "uy": "Uy (mm)",
        "no_results": "Build your structure and click 'Analyze' to see results.",
        "warning_min": "Need at least 2 nodes and 1 member to analyze.",
        "error_analysis": "Analysis failed. Check structure geometry and supports.",
        "legend": "Blue = Tension | Red = Compression | Green = Joint Load | Orange = Mid Load",
        "export": "Export Results",
    },
    "Persian": {
        "title": "سیستم تحلیل خرپا دوبعدی",
        "subtitle": "نرم‌افزار حرفه‌ای تحلیل به روش سختی ماتریسی",
        "language": "زبان",
        "live_preview": "پیش‌نمایش زنده",
        "node_tab": "گره‌ها",
        "member_tab": "اعضا",
        "support_tab": "تکیه‌گاه‌ها",
        "load_tab": "بارها",
        "analyze": "تحلیل سازه",
        "reset": "بازنشانی کل",
        "node_name": "نام گره",
        "x_coord": "X (متر)",
        "y_coord": "Y (متر)",
        "add_node": "افزودن گره",
        "update_node": "ویرایش انتخاب",
        "delete_node": "حذف انتخاب",
        "member_name": "نام عضو",
        "start_node": "گره شروع",
        "end_node": "گره پایان",
        "add_member": "افزودن عضو",
        "update_member": "ویرایش انتخاب",
        "delete_member": "حذف انتخاب",
        "support_node": "گره",
        "support_type": "نوع تکیه‌گاه",
        "support_types": ["گیردار (ثابت X, Y)", "غلتک X (آزاد X)", "غلتک Y (آزاد Y)"],
        "add_support": "افزودن تکیه‌گاه",
        "delete_support": "حذف انتخاب",
        "load_type": "نوع بار",
        "load_types": ["بار گرهی", "بار وسط عضو"],
        "load_name": "نام بار",
        "load_location": "در گره",
        "load_member": "روی عضو",
        "load_magnitude": "بزرگی (kN)",
        "load_angle": "زاویه (درجه از +X)",
        "add_load": "افزودن بار",
        "delete_load": "حذف انتخاب",
        "nodes_table": "مختصات گره‌ها",
        "members_table": "اتصالات اعضا",
        "supports_table": "شرایط تکیه‌گاهی",
        "loads_table": "بارهای اعمالی",
        "select_row": "برای ویرایش روی یک ردیف کلیک کنید",
        "reactions": "عکس‌العمل‌های تکیه‌گاهی",
        "member_forces": "نیروهای اعضا",
        "displacements": "جابجایی‌های گرهی",
        "node_col": "گره",
        "fx": "Fx (kN)",
        "fy": "Fy (kN)",
        "resultant": "برآیند (kN)",
        "angle": "زاویه (°)",
        "member_col": "عضو",
        "force": "نیرو (kN)",
        "type": "نوع",
        "tension": "کششی",
        "compression": "فشاری",
        "ux": "Ux (mm)",
        "uy": "Uy (mm)",
        "no_results": "سازه را تعریف کرده و دکمه تحلیل را بزنید.",
        "warning_min": "حداقل به ۲ گره و ۱ عضو نیاز است.",
        "error_analysis": "تحلیل ناموفق. هندسه و تکیه‌گاه‌ها را بررسی کنید.",
        "legend": "آبی = کشش | قرمز = فشار | سبز = بار گرهی | نارنجی = بار وسط",
        "export": "خروجی نتایج",
    }
}

# ============================================================================
# TRUSS ANALYZER
# ============================================================================

class TrussAnalyzer:
    def __init__(self, nodes_dict, members_list, supports_dict, joint_loads_dict, member_loads_list):
        self.node_names = list(nodes_dict.keys())
        self.node_coords = {name: nodes_dict[name] for name in self.node_names}
        self.node_to_idx = {name: i for i, name in enumerate(self.node_names)}
        self.n_nodes = len(self.node_names)
        self.n_dofs = 2 * self.n_nodes
        
        self.members = members_list
        self.supports = supports_dict
        self.joint_loads = joint_loads_dict
        self.member_loads = member_loads_list
        
        self.E = 200e6
        self.A = 0.01
        
        self.K_global = np.zeros((self.n_dofs, self.n_dofs))
        self.F_global = np.zeros(self.n_dofs)
        self.U_global = None
        self.member_forces = {}
        self.reactions = {}
        
        self._assemble()
        self._apply_loads()
        self._apply_BCs()
        self._solve()
    
    def _dof(self, node_name):
        idx = self.node_to_idx[node_name]
        return 2*idx, 2*idx+1
    
    def _assemble(self):
        for member_name, n1, n2 in self.members:
            x1, y1 = self.node_coords[n1]
            x2, y2 = self.node_coords[n2]
            dx, dy = x2-x1, y2-y1
            L = np.sqrt(dx**2 + dy**2)
            if L < 1e-10:
                continue
            c, s = dx/L, dy/L
            
            k = (self.E * self.A / L) * np.array([
                [c*c, c*s, -c*c, -c*s],
                [c*s, s*s, -c*s, -s*s],
                [-c*c, -c*s, c*c, c*s],
                [-c*s, -s*s, c*s, s*s]
            ])
            
            d1x, d1y = self._dof(n1)
            d2x, d2y = self._dof(n2)
            dofs = [d1x, d1y, d2x, d2y]
            
            for i, gi in enumerate(dofs):
                for j, gj in enumerate(dofs):
                    self.K_global[gi, gj] += k[i, j]
    
    def _apply_loads(self):
        # Joint loads
        for node_name, (mag, ang) in self.joint_loads.items():
            rad = np.radians(ang)
            dx, dy = self._dof(node_name)
            self.F_global[dx] += mag * np.cos(rad)
            self.F_global[dy] += mag * np.sin(rad)
        
        # Mid-member loads -> equivalent nodal loads
        for load_name, member_name, mag, ang in self.member_loads:
            for mname, n1, n2 in self.members:
                if mname == member_name:
                    x1, y1 = self.node_coords[n1]
                    x2, y2 = self.node_coords[n2]
                    L = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                    if L < 1e-10:
                        break
                    c, s = (x2-x1)/L, (y2-y1)/L
                    rad = np.radians(ang)
                    axial = mag * np.cos(rad) * c + mag * np.sin(rad) * s
                    d1x, d1y = self._dof(n1)
                    d2x, d2y = self._dof(n2)
                    self.F_global[d1x] += axial * c * 0.5
                    self.F_global[d1y] += axial * s * 0.5
                    self.F_global[d2x] += axial * c * 0.5
                    self.F_global[d2y] += axial * s * 0.5
                    break
    
    def _apply_BCs(self):
        penalty = 1e15
        for node_name, stype in self.supports.items():
            dx, dy = self._dof(node_name)
            if stype == 'pinned':
                self.K_global[dx, dx] += penalty
                self.K_global[dy, dy] += penalty
            elif stype == 'roller_x':
                self.K_global[dy, dy] += penalty
            elif stype == 'roller_y':
                self.K_global[dx, dx] += penalty
    
    def _solve(self):
        try:
            self.U_global = np.linalg.solve(self.K_global, self.F_global)
            
            for member_name, n1, n2 in self.members:
                x1, y1 = self.node_coords[n1]
                x2, y2 = self.node_coords[n2]
                dx, dy = x2-x1, y2-y1
                L = np.sqrt(dx**2 + dy**2)
                if L < 1e-10:
                    self.member_forces[member_name] = 0
                    continue
                c, s = dx/L, dy/L
                d1x, d1y = self._dof(n1)
                d2x, d2y = self._dof(n2)
                u1 = self.U_global[d1x]; v1 = self.U_global[d1y]
                u2 = self.U_global[d2x]; v2 = self.U_global[d2y]
                force = (self.E * self.A / L) * (c*(u2-u1) + s*(v2-v1))
                self.member_forces[member_name] = force
            
            for node_name in self.supports:
                dx, dy = self._dof(node_name)
                rx = np.dot(self.K_global[dx, :], self.U_global) - self.F_global[dx]
                ry = np.dot(self.K_global[dy, :], self.U_global) - self.F_global[dy]
                self.reactions[node_name] = (rx, ry)
        except:
            self.U_global = None

# ============================================================================
# VISUALIZATION
# ============================================================================

def draw_truss(nodes_dict, members_list, supports_dict, joint_loads_dict, member_loads_list,
               member_forces=None, reactions=None, lang=None, for_results=False):
    if lang is None:
        lang = LANGUAGES["English"]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')
    
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.15, linestyle='--', color='#30363d')
    ax.set_xlabel('X (m)', color='#8b949e', fontsize=11)
    ax.set_ylabel('Y (m)', color='#8b949e', fontsize=11)
    ax.tick_params(colors='#8b949e')
    for spine in ax.spines.values():
        spine.set_color('#30363d')
    
    all_x = [c[0] for c in nodes_dict.values()]
    all_y = [c[1] for c in nodes_dict.values()]
    if not all_x:
        all_x, all_y = [0, 10], [0, 10]
    
    margin = max(max(all_x)-min(all_x), max(all_y)-min(all_y), 2) * 0.25 + 1
    ax.set_xlim(min(all_x)-margin, max(all_x)+margin)
    ax.set_ylim(min(all_y)-margin, max(all_y)+margin)
    
    # Members
    for member_name, n1, n2 in members_list:
        x1, y1 = nodes_dict[n1]
        x2, y2 = nodes_dict[n2]
        
        if for_results and member_forces and member_name in member_forces:
            force = member_forces[member_name]
            color = '#4a90e2' if force >= 0 else '#e74c3c'
            lw = 3.5
        else:
            color = '#484f58'
            lw = 2
        
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, zorder=2)
        
        # Member label
        mx, my = (x1+x2)/2, (y1+y2)/2
        if for_results and member_forces and member_name in member_forces:
            fv = abs(member_forces[member_name])
            ft = 'T' if member_forces[member_name] >= 0 else 'C'
            label = f'{member_name}\n{fv:.1f}kN({ft})'
            bcol = '#1a3a2a' if ft == 'T' else '#3a1a1a'
        else:
            label = member_name
            bcol = '#161b22'
        
        ax.annotate(label, (mx, my), fontsize=7, ha='center', va='center',
                   color='#e6edf3', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor=bcol,
                            edgecolor='#30363d', alpha=0.9))
    
    # Nodes
    for node_name, (x, y) in nodes_dict.items():
        ax.plot(x, y, 'o', color='#e6edf3', markersize=14, zorder=5)
        ax.plot(x, y, 'o', color='#2a5298', markersize=10, zorder=6)
        ax.annotate(node_name, (x, y), fontsize=10, fontweight='bold',
                   color='#e6edf3', xytext=(10, 10), textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='#161b22',
                            edgecolor='#30363d', alpha=0.85))
    
    # Supports
    for node_name, stype in supports_dict.items():
        x, y = nodes_dict[node_name]
        if stype == 'pinned':
            tri = Polygon([[x-0.5, y-0.5], [x+0.5, y-0.5], [x, y]],
                         facecolor='#30363d', edgecolor='#8b949e', zorder=3, linewidth=1.5)
            ax.add_patch(tri)
            for i in range(4):
                ax.plot([x-0.45+i*0.3, x-0.4+i*0.3], [y-0.5, y-0.7],
                       color='#8b949e', linewidth=1.2)
        elif stype == 'roller_x':
            circ = Circle((x, y-0.3), 0.2, facecolor='#161b22', edgecolor='#8b949e', zorder=3, linewidth=1.5)
            ax.add_patch(circ)
            ax.plot([x-0.5, x+0.5], [y-0.65, y-0.65], color='#8b949e', linewidth=1.5)
            for i in range(3):
                ax.plot([x-0.45+i*0.45, x-0.45+i*0.45], [y-0.65, y-0.8],
                       color='#8b949e', linewidth=1)
        elif stype == 'roller_y':
            circ = Circle((x-0.3, y), 0.2, facecolor='#161b22', edgecolor='#8b949e', zorder=3, linewidth=1.5)
            ax.add_patch(circ)
            ax.plot([x-0.65, x-0.65], [y-0.5, y+0.5], color='#8b949e', linewidth=1.5)
    
    # Scale for arrows
    all_forces = [mag for mag, _ in joint_loads_dict.values()]
    for _, _, mag, _ in member_loads_list:
        all_forces.append(mag)
    max_f = max(all_forces) if all_forces else 1
    scale = (max(all_x)-min(all_x)) / max_f * 0.15 if max_f > 0 else 0.5
    
    # Joint loads
    for node_name, (mag, ang) in joint_loads_dict.items():
        x, y = nodes_dict[node_name]
        rad = np.radians(ang)
        dx = -mag * np.cos(rad) * scale
        dy = -mag * np.sin(rad) * scale
        ax.arrow(x+dx, y+dy, -dx*0.85, -dy*0.85,
                head_width=0.25, head_length=0.35, fc='#2ecc71', ec='#2ecc71',
                linewidth=2.5, zorder=7)
        ax.annotate(f'{mag:.1f}kN', (x+dx*1.15, y+dy*1.15),
                   fontsize=8, color='#2ecc71', fontweight='bold')
    
    # Mid-member loads
    for load_name, member_name, mag, ang in member_loads_list:
        for mname, n1, n2 in members_list:
            if mname == member_name:
                x1, y1 = nodes_dict[n1]
                x2, y2 = nodes_dict[n2]
                mx, my = (x1+x2)/2, (y1+y2)/2
                rad = np.radians(ang)
                dx = -mag * np.cos(rad) * scale
                dy = -mag * np.sin(rad) * scale
                ax.arrow(mx+dx, my+dy, -dx*0.85, -dy*0.85,
                        head_width=0.25, head_length=0.35, fc='#f39c12', ec='#f39c12',
                        linewidth=2.5, zorder=7)
                ax.annotate(f'{load_name}\n{mag:.1f}kN', (mx+dx*1.15, my+dy*1.15),
                           fontsize=7, color='#f39c12', fontweight='bold')
                break
    
    # Reactions (only in results mode)
    if for_results and reactions:
        for node_name, (rx, ry) in reactions.items():
            x, y = nodes_dict[node_name]
            if abs(rx) > 0.01 or abs(ry) > 0.01:
                dx, dy = rx*scale*0.7, ry*scale*0.7
                ax.arrow(x-dx, y-dy, dx*0.85, dy*0.85,
                        head_width=0.25, head_length=0.35, fc='#e67e22', ec='#e67e22',
                        linewidth=3, zorder=7)
                R = np.sqrt(rx**2+ry**2)
                ax.annotate(f'R={R:.1f}kN', (x-dx*1.15, y-dy*1.15),
                           fontsize=8, color='#e67e22', fontweight='bold')
    
    # Legend
    ax.text(0.5, 1.02, lang['legend'], transform=ax.transAxes,
           fontsize=7, color='#8b949e', ha='center',
           bbox=dict(boxstyle='round', facecolor='#161b22', edgecolor='#30363d', alpha=0.9))
    
    plt.tight_layout()
    return fig

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Initialize session state
    defaults = {
        'language': 'English',
        'nodes': {},           # {name: (x, y)}
        'members': [],         # [(name, node1, node2)]
        'supports': {},        # {node_name: type}
        'joint_loads': {},     # {node_name: (mag, ang)}
        'member_loads': [],    # [(load_name, member_name, mag, ang)]
        'results': None,
        'selected_node': None,
        'selected_member': None,
        'selected_support': None,
        'selected_load': None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val
    
    lang = LANGUAGES[st.session_state.language]
    
    # Header
    col_l, col_t = st.columns([1, 5])
    with col_l:
        st.session_state.language = st.selectbox(
            "", ["English", "Persian"],
            key="lang_sel", label_visibility="collapsed"
        )
    
    st.markdown(f'<div class="main-title">{lang["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center;color:#8b949e;margin-bottom:1.5rem;">{lang["subtitle"]}</p>',
               unsafe_allow_html=True)
    
    # Main layout: Left = inputs, Right = preview
    left_col, right_col = st.columns([1, 1])
    
    with right_col:
        st.markdown(f'<div class="section-title">{lang["live_preview"]}</div>', unsafe_allow_html=True)
        
        # Determine if we should show results or construction view
        if st.session_state.results:
            fig = draw_truss(
                st.session_state.nodes,
                st.session_state.members,
                st.session_state.supports,
                st.session_state.joint_loads,
                st.session_state.member_loads,
                member_forces=st.session_state.results.get('member_forces'),
                reactions=st.session_state.results.get('reactions'),
                lang=lang,
                for_results=True
            )
        else:
            fig = draw_truss(
                st.session_state.nodes,
                st.session_state.members,
                st.session_state.supports,
                st.session_state.joint_loads,
                st.session_state.member_loads,
                lang=lang,
                for_results=False
            )
        st.pyplot(fig)
    
    with left_col:
        # Tabs for input
        tabs = st.tabs([
            f"📌 {lang['node_tab']}",
            f"🔗 {lang['member_tab']}",
            f"🏗️ {lang['support_tab']}",
            f"⬇️ {lang['load_tab']}"
        ])
        
        # ===== NODES TAB =====
        with tabs[0]:
            # Table of nodes
            if st.session_state.nodes:
                node_data = []
                for name, (x, y) in st.session_state.nodes.items():
                    node_data.append({"Name": name, "X (m)": x, "Y (m)": y})
                df = pd.DataFrame(node_data)
                
                st.markdown(f"**{lang['nodes_table']}**")
                st.caption(lang['select_row'])
                
                # Clickable table
                selected_indices = st.dataframe(
                    df, hide_index=True, use_container_width=True,
                    selection_mode="single-row",
                    on_select="rerun",
                    key="node_table"
                )
                
                # Handle row selection
                if selected_indices and len(selected_indices.selection.rows) > 0:
                    row_idx = selected_indices.selection.rows[0]
                    st.session_state.selected_node = list(st.session_state.nodes.keys())[row_idx]
            
            st.markdown("---")
            
            # Add/Edit form
            with st.form("node_form", clear_on_submit=True):
                if st.session_state.selected_node and st.session_state.selected_node in st.session_state.nodes:
                    default_name = st.session_state.selected_node
                    default_x, default_y = st.session_state.nodes[st.session_state.selected_node]
                else:
                    default_name = ""
                    default_x, default_y = 0.0, 0.0
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    new_name = st.text_input(lang['node_name'], value=default_name, 
                                            placeholder="e.g. A, B1", key="n_name")
                with c2:
                    new_x = st.text_input(lang['x_coord'], value=str(default_x), 
                                         placeholder="0.0", key="n_x")
                with c3:
                    new_y = st.text_input(lang['y_coord'], value=str(default_y), 
                                         placeholder="0.0", key="n_y")
                
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                with col_btn1:
                    add_clicked = st.form_submit_button(lang['add_node'])
                with col_btn2:
                    update_clicked = st.form_submit_button(lang['update_node'])
                with col_btn3:
                    delete_clicked = st.form_submit_button(lang['delete_node'])
            
            if add_clicked and new_name:
                try:
                    st.session_state.nodes[new_name] = (float(new_x), float(new_y))
                    st.session_state.selected_node = None
                    st.rerun()
                except ValueError:
                    st.error("X and Y must be numbers!")
            
            if update_clicked and st.session_state.selected_node and new_name:
                try:
                    old_name = st.session_state.selected_node
                    new_coords = (float(new_x), float(new_y))
                    
                    # Remove old, add new
                    del st.session_state.nodes[old_name]
                    st.session_state.nodes[new_name] = new_coords
                    
                    # Update references in members
                    st.session_state.members = [
                        (new_name if n1 == old_name else n1,
                         new_name if n2 == old_name else n2,
                         mname)
                        if isinstance(m, tuple) and len(m) == 3
                        else (m[0], 
                              new_name if m[1] == old_name else m[1],
                              new_name if m[2] == old_name else m[2])
                        for m in st.session_state.members
                    ]
                    
                    st.session_state.selected_node = new_name
                    st.rerun()
                except ValueError:
                    st.error("X and Y must be numbers!")
            
            if delete_clicked and st.session_state.selected_node:
                name = st.session_state.selected_node
                del st.session_state.nodes[name]
                st.session_state.members = [m for m in st.session_state.members 
                                           if m[1] != name and m[2] != name]
                st.session_state.supports.pop(name, None)
                st.session_state.joint_loads.pop(name, None)
                st.session_state.member_loads = [l for l in st.session_state.member_loads 
                                                if not any(m[1] == name or m[2] == name 
                                                          for m in st.session_state.members 
                                                          if m[0] == l[1])]
                st.session_state.selected_node = None
                st.rerun()
        
        # ===== MEMBERS TAB =====
        with tabs[1]:
            # Fix member data structure
            fixed_members = []
            for m in st.session_state.members:
                if isinstance(m, tuple) and len(m) == 3:
                    fixed_members.append(m)
                elif isinstance(m, (list, tuple)) and len(m) == 3:
                    fixed_members.append(tuple(m))
            
            if fixed_members:
                mem_data = []
                for mname, n1, n2 in fixed_members:
                    mem_data.append({"Name": mname, "Start": n1, "End": n2})
                df = pd.DataFrame(mem_data)
                
                st.markdown(f"**{lang['members_table']}**")
                st.caption(lang['select_row'])
                
                selected_indices = st.dataframe(
                    df, hide_index=True, use_container_width=True,
                    selection_mode="single-row",
                    on_select="rerun",
                    key="member_table"
                )
                
                if selected_indices and len(selected_indices.selection.rows) > 0:
                    row_idx = selected_indices.selection.rows[0]
                    st.session_state.selected_member = fixed_members[row_idx][0]
            
            st.markdown("---")
            
            node_names = list(st.session_state.nodes.keys())
            
            with st.form("member_form", clear_on_submit=True):
                if st.session_state.selected_member:
                    # Find the member
                    default_mname = st.session_state.selected_member
                    default_s = ""
                    default_e = ""
                    for m in fixed_members:
                        if m[0] == st.session_state.selected_member:
                            default_s = m[1]
                            default_e = m[2]
                            break
                else:
                    default_mname = ""
                    default_s = node_names[0] if node_names else ""
                    default_e = node_names[-1] if len(node_names) > 1 else ""
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    new_mname = st.text_input(lang['member_name'], value=default_mname,
                                             placeholder="e.g. M1, AB", key="m_name")
                with c2:
                    if node_names:
                        s_idx = node_names.index(default_s) if default_s in node_names else 0
                        start_n = st.selectbox(lang['start_node'], node_names, 
                                              index=s_idx, key="m_start")
                    else:
                        start_n = st.selectbox(lang['start_node'], ["No nodes"], key="m_start")
                with c3:
                    if len(node_names) > 1:
                        e_idx = node_names.index(default_e) if default_e in node_names else 1
                        end_n = st.selectbox(lang['end_node'], node_names,
                                            index=e_idx, key="m_end")
                    else:
                        end_n = st.selectbox(lang['end_node'], ["No nodes"], key="m_end")
                
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                with col_btn1:
                    add_m = st.form_submit_button(lang['add_member'])
                with col_btn2:
                    update_m = st.form_submit_button(lang['update_member'])
                with col_btn3:
                    delete_m = st.form_submit_button(lang['delete_member'])
            
            if add_m and new_mname and start_n != end_n and start_n in node_names and end_n in node_names:
                st.session_state.members.append((new_mname, start_n, end_n))
                st.session_state.selected_member = None
                st.rerun()
            
            if update_m and st.session_state.selected_member and new_mname:
                old_name = st.session_state.selected_member
                st.session_state.members = [
                    (new_mname, start_n, end_n) if m[0] == old_name else m
                    for m in fixed_members
                ]
                st.session_state.selected_member = new_mname
                st.rerun()
            
            if delete_m and st.session_state.selected_member:
                old_name = st.session_state.selected_member
                st.session_state.members = [m for m in fixed_members if m[0] != old_name]
                st.session_state.member_loads = [l for l in st.session_state.member_loads if l[1] != old_name]
                st.session_state.selected_member = None
                st.rerun()
        
        # ===== SUPPORTS TAB =====
        with tabs[2]:
            if st.session_state.supports:
                sup_data = []
                for node_name, stype in st.session_state.supports.items():
                    sup_data.append({"Node": node_name, "Type": stype})
                df = pd.DataFrame(sup_data)
                
                st.markdown(f"**{lang['supports_table']}**")
                st.caption(lang['select_row'])
                
                selected_indices = st.dataframe(
                    df, hide_index=True, use_container_width=True,
                    selection_mode="single-row",
                    on_select="rerun",
                    key="support_table"
                )
                
                if selected_indices and len(selected_indices.selection.rows) > 0:
                    row_idx = selected_indices.selection.rows[0]
                    st.session_state.selected_support = list(st.session_state.supports.keys())[row_idx]
            
            st.markdown("---")
            
            with st.form("support_form", clear_on_submit=True):
                node_names = list(st.session_state.nodes.keys())
                
                if st.session_state.selected_support and st.session_state.selected_support in st.session_state.supports:
                    default_snode = st.session_state.selected_support
                    default_stype = st.session_state.supports[st.session_state.selected_support]
                else:
                    default_snode = node_names[0] if node_names else ""
                    default_stype = lang['support_types'][0]
                
                c1, c2 = st.columns(2)
                with c1:
                    if node_names:
                        s_idx = node_names.index(default_snode) if default_snode in node_names else 0
                        sup_node = st.selectbox(lang['support_node'], node_names,
                                               index=s_idx, key="sup_node")
                    else:
                        sup_node = st.selectbox(lang['support_node'], ["No nodes"], key="sup_node")
                with c2:
                    type_idx = lang['support_types'].index(default_stype) if default_stype in lang['support_types'] else 0
                    sup_type = st.selectbox(lang['support_type'], lang['support_types'],
                                           index=type_idx, key="sup_type")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    add_s = st.form_submit_button(lang['add_support'])
                with col_btn2:
                    delete_s = st.form_submit_button(lang['delete_support'])
            
            if add_s and sup_node in node_names:
                type_map = {
                    lang['support_types'][0]: 'pinned',
                    lang['support_types'][1]: 'roller_x',
                    lang['support_types'][2]: 'roller_y'
                }
                st.session_state.supports[sup_node] = type_map[sup_type]
                st.session_state.selected_support = None
                st.rerun()
            
            if delete_s and st.session_state.selected_support:
                del st.session_state.supports[st.session_state.selected_support]
                st.session_state.selected_support = None
                st.rerun()
        
        # ===== LOADS TAB =====
        with tabs[3]:
            all_loads = []
            for node_name, (mag, ang) in st.session_state.joint_loads.items():
                all_loads.append({"Type": "Joint", "At": f"Node {node_name}", 
                                 "kN": mag, "°": ang})
            for lname, mname, mag, ang in st.session_state.member_loads:
                all_loads.append({"Type": "Mid-Member", "At": f"{mname} ({lname})",
                                 "kN": mag, "°": ang})
            
            if all_loads:
                df = pd.DataFrame(all_loads)
                st.markdown(f"**{lang['loads_table']}**")
                st.caption(lang['select_row'])
                st.dataframe(df, hide_index=True, use_container_width=True)
            
            st.markdown("---")
            
            with st.form("load_form", clear_on_submit=True):
                load_type = st.selectbox(lang['load_type'], lang['load_types'], key="l_type")
                
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    load_name = st.text_input(lang['load_name'], placeholder="e.g. F1, W", key="l_name")
                with c2:
                    if load_type == lang['load_types'][0]:  # Joint
                        node_names = list(st.session_state.nodes.keys())
                        load_at = st.selectbox(lang['load_location'], 
                                              node_names if node_names else ["No nodes"],
                                              key="l_at")
                    else:  # Mid-member
                        mem_names = [m[0] for m in st.session_state.members]
                        load_at = st.selectbox(lang['load_member'],
                                              mem_names if mem_names else ["No members"],
                                              key="l_at")
                with c3:
                    mag = st.text_input(lang['load_magnitude'], placeholder="10", key="l_mag")
                with c4:
                    ang = st.text_input(lang['load_angle'], placeholder="270", key="l_ang")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    add_l = st.form_submit_button(lang['add_load'])
                with col_btn2:
                    delete_l = st.form_submit_button(lang['delete_load'])
            
            if add_l and load_name:
                try:
                    mag_f = float(mag)
                    ang_f = float(ang)
                    if load_type == lang['load_types'][0] and load_at in st.session_state.nodes:
                        st.session_state.joint_loads[load_at] = (mag_f, ang_f)
                        st.rerun()
                    elif load_type == lang['load_types'][1] and any(m[0] == load_at for m in st.session_state.members):
                        st.session_state.member_loads.append((load_name, load_at, mag_f, ang_f))
                        st.rerun()
                except ValueError:
                    st.error("Magnitude and angle must be numbers!")
            
            if delete_l:
                st.session_state.joint_loads = {}
                st.session_state.member_loads = []
                st.session_state.selected_load = None
                st.rerun()
    
    # ===== ANALYZE & RESET BUTTONS =====
    st.markdown("---")
    col_a, col_r = st.columns([3, 1])
    
    with col_a:
        if st.button(f"🚀 {lang['analyze']}", use_container_width=True):
            if len(st.session_state.nodes) >= 2 and len(st.session_state.members) >= 1:
                with st.spinner("Analyzing structure..."):
                    time.sleep(0.3)
                    try:
                        analyzer = TrussAnalyzer(
                            nodes_dict=st.session_state.nodes,
                            members_list=st.session_state.members,
                            supports_dict=st.session_state.supports,
                            joint_loads_dict=st.session_state.joint_loads,
                            member_loads_list=st.session_state.member_loads
                        )
                        
                        if analyzer.U_global is not None:
                            st.session_state.results = {
                                'reactions': analyzer.reactions,
                                'member_forces': analyzer.member_forces,
                                'displacements': analyzer.U_global,
                                'node_names': analyzer.node_names
                            }
                            st.success("✅ Analysis complete!")
                            st.rerun()
                        else:
                            st.error(lang['error_analysis'])
                    except Exception as e:
                        st.error(f"{lang['error_analysis']}: {str(e)}")
            else:
                st.warning(lang['warning_min'])
    
    with col_r:
        if st.button(f"🔄 {lang['reset']}", use_container_width=True):
            for key in ['nodes', 'members', 'supports', 'joint_loads', 'member_loads', 
                       'results', 'selected_node', 'selected_member', 'selected_support', 'selected_load']:
                st.session_state[key] = {} if key in ['nodes', 'supports', 'joint_loads', 'results'] else []
            st.rerun()
    
    # ===== RESULTS SECTION =====
    if st.session_state.results:
        st.markdown("---")
        st.markdown("## 📊 Analysis Results")
        
        res = st.session_state.results
        
        col_r1, col_r2, col_r3 = st.columns(3)
        
        with col_r1:
            st.markdown(f"### {lang['reactions']}")
            if res['reactions']:
                rdata = []
                for nname, (fx, fy) in res['reactions'].items():
                    R = np.sqrt(fx**2 + fy**2)
                    ang = np.degrees(np.arctan2(fy, fx))
                    rdata.append({
                        lang['node_col']: nname,
                        lang['fx']: f"{fx:.3f}",
                        lang['fy']: f"{fy:.3f}",
                        lang['resultant']: f"{R:.3f}",
                        lang['angle']: f"{ang:.1f}"
                    })
                st.dataframe(pd.DataFrame(rdata), hide_index=True, use_container_width=True)
            else:
                st.info("No reactions")
        
        with col_r2:
            st.markdown(f"### {lang['member_forces']}")
            if res['member_forces']:
                fdata = []
                for mname, force in res['member_forces'].items():
                    fdata.append({
                        lang['member_col']: mname,
                        lang['force']: f"{abs(force):.3f}",
                        lang['type']: lang['tension'] if force >= 0 else lang['compression']
                    })
                st.dataframe(pd.DataFrame(fdata), hide_index=True, use_container_width=True)
            else:
                st.info("No member forces")
        
        with col_r3:
            st.markdown(f"### {lang['displacements']}")
            ddata = []
            for i, nname in enumerate(res['node_names']):
                ux = res['displacements'][2*i] * 1000
                uy = res['displacements'][2*i+1] * 1000
                ddata.append({
                    lang['node_col']: nname,
                    lang['ux']: f"{ux:.4f}",
                    lang['uy']: f"{uy:.4f}"
                })
            st.dataframe(pd.DataFrame(ddata), hide_index=True, use_container_width=True)
        
        # Export button
        if st.button(f"📥 {lang['export']}"):
            buf = io.StringIO()
            buf.write("2D TRUSS ANALYSIS RESULTS\n")
            buf.write("="*50 + "\n\n")
            buf.write("SUPPORT REACTIONS:\n")
            for nname, (fx, fy) in res['reactions'].items():
                R = np.sqrt(fx**2+fy**2)
                buf.write(f"  {nname}: Fx={fx:.3f}, Fy={fy:.3f}, R={R:.3f}\n")
            buf.write("\nMEMBER FORCES:\n")
            for mname, f in res['member_forces'].items():
                buf.write(f"  {mname}: {abs(f):.3f} kN ({'T' if f>=0 else 'C'})\n")
            buf.write("\nNODAL DISPLACEMENTS:\n")
            for i, nname in enumerate(res['node_names']):
                ux = res['displacements'][2*i] * 1000
                uy = res['displacements'][2*i+1] * 1000
                buf.write(f"  {nname}: Ux={ux:.4f} mm, Uy={uy:.4f} mm\n")
            
            st.download_button("Download Results (.txt)", buf.getvalue(),
                             "truss_results.txt", "text/plain")
    
    elif not st.session_state.nodes:
        st.info(lang['no_results'])

if __name__ == "__main__":
    main()