"""
2D Truss Analyzer - Clean, Professional, User-Friendly
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrowPatch, Circle, Polygon, Arc
import io
import time

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="2D Truss Analyzer",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# LANGUAGE SYSTEM
# ============================================================================

LANGUAGES = {
    "English": {
        "title": "2D Truss Analyzer",
        "language": "Language",
        "theme": "Theme",
        "theme_system": "System Default",
        "theme_dark": "Dark",
        "theme_light": "Light",
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
        "start_node": "Start Node",
        "end_node": "End Node",
        "add_member": "Add Member",
        "support_node": "Node",
        "support_type": "Support Type",
        "support_types": ["Pinned (Fix X, Y)", "Roller X (Free X)", "Roller Y (Free Y)"],
        "add_support": "Add Support",
        "load_type": "Load Type",
        "load_types": ["On Node", "On Member (any position)"],
        "load_name": "Load Name",
        "load_location": "At Node",
        "load_member": "On Member",
        "load_position": "Position along member (0=start, 1=end)",
        "load_magnitude": "Magnitude (kN)",
        "load_angle": "Angle (° from +X)",
        "add_load": "Add Load",
        "nodes_table": "Nodes",
        "members_table": "Members",
        "supports_table": "Supports",
        "loads_table": "Loads",
        "tap_edit": "Tap row to edit · Hold for delete",
        "delete_confirm": "Delete this item?",
        "yes_delete": "Yes, delete",
        "cancel": "Cancel",
        "reactions": "Support Reactions",
        "member_forces": "Member Forces",
        "displacements": "Nodal Displacements",
        "node_col": "Node",
        "fx": "Fx (kN)",
        "fy": "Fy (kN)",
        "resultant": "R (kN)",
        "angle": "Angle (°)",
        "member_col": "Member",
        "length": "Length (m)",
        "force": "Force (kN)",
        "type": "Type",
        "tension": "TENSION",
        "compression": "COMPRESSION",
        "ux": "Ux (mm)",
        "uy": "Uy (mm)",
        "no_results": "Build your structure and click Analyze.",
        "warning_min": "Need at least 2 nodes and 1 member.",
        "error_analysis": "Analysis failed. Check supports and geometry.",
        "legend": "Blue=Tension  Red=Compression  Green=Joint Load  Orange=Member Load  Brown=Reaction",
        "export": "Export Results",
        "delete": "Delete",
        "editing": "Editing",
    },
    "Persian": {
        "title": "تحلیل‌گر خرپا دوبعدی",
        "language": "زبان",
        "theme": "پوسته",
        "theme_system": "پیش‌فرض سیستم",
        "theme_dark": "تاریک",
        "theme_light": "روشن",
        "live_preview": "پیش‌نمایش زنده",
        "node_tab": "گره‌ها",
        "member_tab": "اعضا",
        "support_tab": "تکیه‌گاه‌ها",
        "load_tab": "بارها",
        "analyze": "تحلیل سازه",
        "reset": "بازنشانی",
        "node_name": "نام گره",
        "x_coord": "X (متر)",
        "y_coord": "Y (متر)",
        "add_node": "افزودن گره",
        "start_node": "گره شروع",
        "end_node": "گره پایان",
        "add_member": "افزودن عضو",
        "support_node": "گره",
        "support_type": "نوع تکیه‌گاه",
        "support_types": ["گیردار", "غلتک X", "غلتک Y"],
        "add_support": "افزودن تکیه‌گاه",
        "load_type": "نوع بار",
        "load_types": ["روی گره", "روی عضو (هر موقعیت)"],
        "load_name": "نام بار",
        "load_location": "در گره",
        "load_member": "روی عضو",
        "load_position": "موقعیت روی عضو (0=شروع, 1=پایان)",
        "load_magnitude": "بزرگی (kN)",
        "load_angle": "زاویه (درجه)",
        "add_load": "افزودن بار",
        "nodes_table": "گره‌ها",
        "members_table": "اعضا",
        "supports_table": "تکیه‌گاه‌ها",
        "loads_table": "بارها",
        "tap_edit": "برای ویرایش کلیک کنید · نگه دارید برای حذف",
        "delete_confirm": "این مورد حذف شود؟",
        "yes_delete": "بله، حذف کن",
        "cancel": "انصراف",
        "reactions": "عکس‌العمل‌های تکیه‌گاهی",
        "member_forces": "نیروهای اعضا",
        "displacements": "جابجایی‌های گرهی",
        "node_col": "گره",
        "fx": "Fx (kN)",
        "fy": "Fy (kN)",
        "resultant": "برآیند (kN)",
        "angle": "زاویه (°)",
        "member_col": "عضو",
        "length": "طول (m)",
        "force": "نیرو (kN)",
        "type": "نوع",
        "tension": "کششی",
        "compression": "فشاری",
        "ux": "Ux (mm)",
        "uy": "Uy (mm)",
        "no_results": "سازه را تعریف کرده و تحلیل را بزنید.",
        "warning_min": "حداقل ۲ گره و ۱ عضو نیاز است.",
        "error_analysis": "خطا در تحلیل. تکیه‌گاه‌ها و هندسه را بررسی کنید.",
        "legend": "آبی=کشش  قرمز=فشار  سبز=بار گرهی  نارنجی=بار عضو  قهوه‌ای=عکس‌العمل",
        "export": "خروجی",
        "delete": "حذف",
        "editing": "در حال ویرایش",
    }
}

# ============================================================================
# THEME SYSTEM
# ============================================================================

def get_theme_css(theme_mode):
    """Return CSS based on theme selection"""
    if theme_mode == "Dark":
        return """
        <style>
            .stApp, body, .main { background-color: #0d1117 !important; color: #e6edf3 !important; }
            .stTextInput input, .stNumberInput input { 
                background-color: #161b22 !important; color: #e6edf3 !important; 
                border: 1px solid #30363d !important; border-radius: 8px !important; 
            }
            .stTextInput input:focus, .stNumberInput input:focus {
                border-color: #4a90e2 !important; box-shadow: 0 0 0 3px rgba(74,144,226,0.2) !important;
            }
            .stSelectbox > div > div { background-color: #161b22 !important; color: #e6edf3 !important; border-color: #30363d !important; }
            .stButton > button { background: linear-gradient(135deg, #1e3c72, #2a5298) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; }
            .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(30,60,114,0.5) !important; }
            .stDataFrame { background: #161b22 !important; border: 1px solid #30363d !important; border-radius: 10px !important; }
            .stDataFrame th { background: #1c2333 !important; color: #4a90e2 !important; }
            .stDataFrame td { background: #161b22 !important; color: #e6edf3 !important; }
            .stDataFrame tr:hover td { background: #1c2333 !important; }
            .stTabs [data-baseweb="tab-list"] { background: #161b22 !important; border-radius: 10px !important; }
            .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #1e3c72, #2a5298) !important; color: white !important; }
            .section-title { color: #4a90e2 !important; border-bottom: 2px solid #1e3c72 !important; }
            .data-card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 1rem; }
            .selected-row { background: #1a2a4a !important; border-left: 3px solid #4a90e2 !important; }
            ::-webkit-scrollbar-track { background: #0d1117; }
            ::-webkit-scrollbar-thumb { background: #30363d; }
            .stSpinner > div { border-color: #4a90e2 !important; }
        </style>
        """
    else:  # Light
        return """
        <style>
            .stApp, body, .main { background-color: #f8fafc !important; color: #1e293b !important; }
            .stTextInput input, .stNumberInput input { 
                background-color: white !important; color: #1e293b !important; 
                border: 1px solid #cbd5e1 !important; border-radius: 8px !important; 
            }
            .stTextInput input:focus, .stNumberInput input:focus {
                border-color: #3b82f6 !important; box-shadow: 0 0 0 3px rgba(59,130,246,0.2) !important;
            }
            .stSelectbox > div > div { background-color: white !important; color: #1e293b !important; border-color: #cbd5e1 !important; }
            .stButton > button { background: linear-gradient(135deg, #2563eb, #1d4ed8) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; }
            .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(37,99,235,0.3) !important; }
            .stDataFrame { background: white !important; border: 1px solid #e2e8f0 !important; border-radius: 10px !important; }
            .stDataFrame th { background: #f1f5f9 !important; color: #2563eb !important; }
            .stDataFrame td { background: white !important; color: #1e293b !important; }
            .stDataFrame tr:hover td { background: #eff6ff !important; }
            .stTabs [data-baseweb="tab-list"] { background: #f1f5f9 !important; border-radius: 10px !important; }
            .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #2563eb, #1d4ed8) !important; color: white !important; }
            .section-title { color: #2563eb !important; border-bottom: 2px solid #bfdbfe !important; }
            .data-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1rem; }
            .selected-row { background: #dbeafe !important; border-left: 3px solid #2563eb !important; }
            ::-webkit-scrollbar-track { background: #f1f5f9; }
            ::-webkit-scrollbar-thumb { background: #cbd5e1; }
            .stSpinner > div { border-color: #2563eb !important; }
        </style>
        """

# ============================================================================
# TRUSS ANALYZER WITH ANY-POSITION MEMBER LOADS
# ============================================================================

class TrussAnalyzer:
    def __init__(self, nodes_dict, members_list, supports_dict, joint_loads_dict, member_loads_list):
        self.node_names = list(nodes_dict.keys())
        self.node_coords = nodes_dict
        self.node_to_idx = {name: i for i, name in enumerate(self.node_names)}
        self.n_nodes = len(self.node_names)
        self.n_dofs = 2 * self.n_nodes
        
        self.members = members_list  # [(name, n1, n2)]
        self.supports = supports_dict
        self.joint_loads = joint_loads_dict
        self.member_loads = member_loads_list  # [(load_name, member_name, position, mag, ang)]
        
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
        
        # Member loads at any position (converted to equivalent nodal loads)
        for load_name, member_name, pos, mag, ang in self.member_loads:
            for mname, n1, n2 in self.members:
                if mname == member_name:
                    x1, y1 = self.node_coords[n1]
                    x2, y2 = self.node_coords[n2]
                    L = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                    if L < 1e-10:
                        break
                    c, s = (x2-x1)/L, (y2-y1)/L
                    rad = np.radians(ang)
                    
                    # Force components
                    fx = mag * np.cos(rad)
                    fy = mag * np.sin(rad)
                    
                    # Axial component (what matters for truss)
                    axial = fx * c + fy * s
                    
                    # Position along member (pos from 0 to 1)
                    a = pos  # distance fraction from n1
                    b = 1 - pos  # distance fraction from n2
                    
                    # Equivalent nodal forces (based on position)
                    d1x, d1y = self._dof(n1)
                    d2x, d2y = self._dof(n2)
                    
                    # Distribute based on distance (closer node gets more)
                    self.F_global[d1x] += axial * c * b
                    self.F_global[d1y] += axial * s * b
                    self.F_global[d2x] += axial * c * a
                    self.F_global[d2y] += axial * s * a
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
            
            # Member forces (including effect of loads on members)
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
                
                # Base force from nodal displacements
                force = (self.E * self.A / L) * (c*(u2-u1) + s*(v2-v1))
                
                # Add effect of loads applied directly on this member
                for lname, mname, pos, mag, ang in self.member_loads:
                    if mname == member_name:
                        rad = np.radians(ang)
                        axial = mag * np.cos(rad) * c + mag * np.sin(rad) * s
                        # Force at the position divides member into two segments
                        # The measured force depends on which side we're measuring from
                        # For member end forces, we add the appropriate share
                        force += axial * (1 - pos)
                
                self.member_forces[member_name] = force
            
            # Reactions
            for node_name in self.supports:
                dx, dy = self._dof(node_name)
                rx = np.dot(self.K_global[dx, :], self.U_global) - self.F_global[dx]
                ry = np.dot(self.K_global[dy, :], self.U_global) - self.F_global[dy]
                self.reactions[node_name] = (rx, ry)
        except:
            self.U_global = None
            self.member_forces = {}
            self.reactions = {}

# ============================================================================
# VISUALIZATION
# ============================================================================

def draw_truss(nodes_dict, members_list, supports_dict, joint_loads_dict, member_loads_list,
               member_forces=None, reactions=None, lang=None, for_results=False):
    if lang is None:
        lang = LANGUAGES["English"]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    # Drawing always dark for engineering clarity
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.15, linestyle='--', color='#404060')
    ax.set_xlabel('X (m)', color='#c0c0d0', fontsize=11)
    ax.set_ylabel('Y (m)', color='#c0c0d0', fontsize=11)
    ax.tick_params(colors='#c0c0d0')
    for spine in ax.spines.values():
        spine.set_color('#404060')
    
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
            color = '#5a5a7a'
            lw = 2
        
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, zorder=2)
        
        mx, my = (x1+x2)/2, (y1+y2)/2
        L = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        
        if for_results and member_forces and member_name in member_forces:
            fv = abs(member_forces[member_name])
            ft = 'T' if member_forces[member_name] >= 0 else 'C'
            label = f'{member_name} ({L:.1f}m)\n{fv:.1f}kN {ft}'
            bcol = '#1a3a2a' if ft == 'T' else '#3a1a1a'
        else:
            label = f'{member_name}\n{L:.1f}m'
            bcol = '#1a1a2e'
        
        ax.annotate(label, (mx, my), fontsize=7, ha='center', va='center',
                   color='#e0e0f0', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor=bcol,
                            edgecolor='#404060', alpha=0.9))
    
    # Nodes
    for node_name, (x, y) in nodes_dict.items():
        ax.plot(x, y, 'o', color='#e0e0f0', markersize=14, zorder=5)
        ax.plot(x, y, 'o', color='#2a5298', markersize=10, zorder=6)
        ax.annotate(node_name, (x, y), fontsize=10, fontweight='bold',
                   color='#e0e0f0', xytext=(10, 10), textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='#1a1a2e',
                            edgecolor='#404060', alpha=0.85))
    
    # Supports
    for node_name, stype in supports_dict.items():
        x, y = nodes_dict[node_name]
        if stype == 'pinned':
            tri = Polygon([[x-0.5, y-0.5], [x+0.5, y-0.5], [x, y]],
                         facecolor='#404060', edgecolor='#c0c0d0', zorder=3, linewidth=1.5)
            ax.add_patch(tri)
            for i in range(4):
                ax.plot([x-0.45+i*0.3, x-0.4+i*0.3], [y-0.5, y-0.7],
                       color='#c0c0d0', linewidth=1.2)
        elif stype == 'roller_x':
            circ = Circle((x, y-0.3), 0.2, facecolor='#1a1a2e', edgecolor='#c0c0d0', zorder=3, linewidth=1.5)
            ax.add_patch(circ)
            ax.plot([x-0.5, x+0.5], [y-0.65, y-0.65], color='#c0c0d0', linewidth=1.5)
            for i in range(3):
                ax.plot([x-0.45+i*0.45, x-0.45+i*0.45], [y-0.65, y-0.8],
                       color='#c0c0d0', linewidth=1)
        elif stype == 'roller_y':
            circ = Circle((x-0.3, y), 0.2, facecolor='#1a1a2e', edgecolor='#c0c0d0', zorder=3, linewidth=1.5)
            ax.add_patch(circ)
            ax.plot([x-0.65, x-0.65], [y-0.5, y+0.5], color='#c0c0d0', linewidth=1.5)
    
    # Scale for arrows
    all_forces = [mag for mag, _ in joint_loads_dict.values()]
    for _, _, _, mag, _ in member_loads_list:
        all_forces.append(mag)
    max_f = max(all_forces) if all_forces else 1
    scale = (max(all_x)-min(all_x)) / max_f * 0.15 if max_f > 0 else 0.5
    
    # Joint loads
    for node_name, (mag, ang) in joint_loads_dict.items():
        if node_name not in nodes_dict:
            continue
        x, y = nodes_dict[node_name]
        rad = np.radians(ang)
        dx = -mag * np.cos(rad) * scale
        dy = -mag * np.sin(rad) * scale
        ax.arrow(x+dx, y+dy, -dx*0.85, -dy*0.85,
                head_width=0.25, head_length=0.35, fc='#2ecc71', ec='#2ecc71',
                linewidth=2.5, zorder=7)
        ax.annotate(f'{mag:.1f}kN', (x+dx*1.15, y+dy*1.15),
                   fontsize=8, color='#2ecc71', fontweight='bold')
    
    # Member loads (at any position)
    for load_name, member_name, pos, mag, ang in member_loads_list:
        for mname, n1, n2 in members_list:
            if mname == member_name:
                x1, y1 = nodes_dict[n1]
                x2, y2 = nodes_dict[n2]
                # Position along member
                px = x1 + pos * (x2 - x1)
                py = y1 + pos * (y2 - y1)
                rad = np.radians(ang)
                dx = -mag * np.cos(rad) * scale
                dy = -mag * np.sin(rad) * scale
                ax.arrow(px+dx, py+dy, -dx*0.85, -dy*0.85,
                        head_width=0.25, head_length=0.35, fc='#f39c12', ec='#f39c12',
                        linewidth=2.5, zorder=7)
                ax.annotate(f'{load_name}\n{mag:.1f}kN', (px+dx*1.15, py+dy*1.15),
                           fontsize=7, color='#f39c12', fontweight='bold')
                break
    
    # Reactions (only in results mode)
    if for_results and reactions:
        for node_name, (rx, ry) in reactions.items():
            if node_name not in nodes_dict:
                continue
            x, y = nodes_dict[node_name]
            if abs(rx) > 0.01 or abs(ry) > 0.01:
                dx, dy = rx*scale*0.7, ry*scale*0.7
                ax.arrow(x-dx, y-dy, dx*0.85, dy*0.85,
                        head_width=0.25, head_length=0.35, fc='#c0843c', ec='#c0843c',
                        linewidth=3, zorder=7)
                R = np.sqrt(rx**2+ry**2)
                ax.annotate(f'R={R:.1f}kN', (x-dx*1.15, y-dy*1.15),
                           fontsize=8, color='#c0843c', fontweight='bold')
    
    # Legend
    ax.text(0.5, 1.02, lang['legend'], transform=ax.transAxes,
           fontsize=6.5, color='#a0a0b0', ha='center',
           bbox=dict(boxstyle='round', facecolor='#1a1a2e', edgecolor='#404060', alpha=0.9))
    
    plt.tight_layout()
    return fig

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Initialize session state
    defaults = {
        'language': 'English',
        'theme': 'System Default',
        'nodes': {},
        'members': [],
        'supports': {},
        'joint_loads': {},
        'member_loads': [],
        'results': None,
        'editing_node': None,
        'editing_member': None,
        'editing_support_node': None,
        'editing_load_key': None,
        'delete_confirm_target': None,
        # Form persistence
        'form_node_name': '',
        'form_node_x': '',
        'form_node_y': '',
        'form_member_start': '',
        'form_member_end': '',
        'form_support_node': '',
        'form_support_type': '',
        'form_load_name': '',
        'form_load_type': '',
        'form_load_target': '',
        'form_load_pos': '',
        'form_load_mag': '',
        'form_load_ang': '',
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val
    
    lang = LANGUAGES[st.session_state.language]
    
    # Determine actual theme
    if st.session_state.theme == "System Default":
        # Streamlit auto-detects, we'll just use a neutral approach
        actual_theme = "Light"  # default fallback
    else:
        actual_theme = st.session_state.theme
    
    # Apply theme
    st.markdown(get_theme_css(actual_theme), unsafe_allow_html=True)
    
    # ===== HEADER =====
    col_lang, col_theme, col_title = st.columns([1, 1, 4])
    with col_lang:
        st.session_state.language = st.selectbox(
            "", ["English", "Persian"],
            key="lang_sel", label_visibility="collapsed"
        )
    with col_theme:
        st.session_state.theme = st.selectbox(
            "", [lang['theme_system'], lang['theme_dark'], lang['theme_light']],
            key="theme_sel", label_visibility="collapsed"
        )
    
    # Title
    st.markdown(f"""
        <h1 style='text-align:center;font-weight:900;margin-bottom:0;'>{lang['title']}</h1>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ===== MAIN LAYOUT: LEFT = INPUTS, RIGHT = PREVIEW =====
    left_col, right_col = st.columns([1, 1])
    
    with right_col:
        # Live preview always visible
        st.markdown(f"**{lang['live_preview']}**")
        
        if st.session_state.results:
            fig = draw_truss(
                st.session_state.nodes, st.session_state.members,
                st.session_state.supports, st.session_state.joint_loads,
                st.session_state.member_loads,
                member_forces=st.session_state.results.get('member_forces'),
                reactions=st.session_state.results.get('reactions'),
                lang=lang, for_results=True
            )
        else:
            fig = draw_truss(
                st.session_state.nodes, st.session_state.members,
                st.session_state.supports, st.session_state.joint_loads,
                st.session_state.member_loads,
                lang=lang, for_results=False
            )
        st.pyplot(fig)
    
    with left_col:
        # ===== TABS =====
        tabs = st.tabs([
            f"📌 {lang['node_tab']}",
            f"🔗 {lang['member_tab']}",
            f"🏗️ {lang['support_tab']}",
            f"⬇️ {lang['load_tab']}"
        ])
        
        # ==================== NODES TAB ====================
        with tabs[0]:
            # Data table
            if st.session_state.nodes:
                node_data = []
                for name, (x, y) in st.session_state.nodes.items():
                    node_data.append({"Node": name, "X (m)": x, "Y (m)": y})
                df = pd.DataFrame(node_data)
                
                st.caption(lang['tap_edit'])
                selected = st.dataframe(
                    df, hide_index=True, use_container_width=True,
                    selection_mode="single-row", on_select="rerun", key="node_tbl"
                )
                
                if selected and len(selected.selection.rows) > 0:
                    idx = selected.selection.rows[0]
                    clicked_name = list(st.session_state.nodes.keys())[idx]
                    
                    if st.session_state.editing_node == clicked_name:
                        # Second click = show delete option
                        st.session_state.delete_confirm_target = ('node', clicked_name)
                    else:
                        # First click = edit
                        st.session_state.editing_node = clicked_name
                        st.session_state.form_node_name = clicked_name
                        st.session_state.form_node_x = str(st.session_state.nodes[clicked_name][0])
                        st.session_state.form_node_y = str(st.session_state.nodes[clicked_name][1])
                        st.session_state.delete_confirm_target = None
                        st.rerun()
            
            # Delete confirmation
            if st.session_state.delete_confirm_target and st.session_state.delete_confirm_target[0] == 'node':
                target = st.session_state.delete_confirm_target[1]
                st.warning(f"{lang['delete_confirm']} **{target}**?")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(lang['yes_delete'], key="del_node_yes"):
                        del st.session_state.nodes[target]
                        st.session_state.members = [m for m in st.session_state.members if m[1] != target and m[2] != target]
                        st.session_state.supports.pop(target, None)
                        st.session_state.joint_loads.pop(target, None)
                        st.session_state.delete_confirm_target = None
                        st.session_state.editing_node = None
                        st.rerun()
                with c2:
                    if st.button(lang['cancel'], key="del_node_no"):
                        st.session_state.delete_confirm_target = None
                        st.rerun()
            
            st.markdown("---")
            
            # Input form
            node_names = list(st.session_state.nodes.keys())
            
            c1, c2, c3 = st.columns(3)
            with c1:
                node_name = st.text_input(
                    lang['node_name'], value=st.session_state.form_node_name,
                    placeholder="e.g. A", key="inp_nname"
                )
            with c2:
                node_x = st.text_input(
                    lang['x_coord'], value=st.session_state.form_node_x,
                    placeholder="0", key="inp_nx"
                )
            with c3:
                node_y = st.text_input(
                    lang['y_coord'], value=st.session_state.form_node_y,
                    placeholder="0", key="inp_ny"
                )
            
            # Update form state
            st.session_state.form_node_name = node_name
            st.session_state.form_node_x = node_x
            st.session_state.form_node_y = node_y
            
            col_b1, col_b2 = st.columns([3, 1])
            with col_b1:
                if st.button(lang['add_node'], key="btn_add_node", use_container_width=True):
                    if node_name:
                        try:
                            xf = float(node_x) if node_x else 0.0
                            yf = float(node_y) if node_y else 0.0
                            st.session_state.nodes[node_name] = (xf, yf)
                            # Clear form
                            st.session_state.form_node_name = ''
                            st.session_state.form_node_x = ''
                            st.session_state.form_node_y = ''
                            st.session_state.editing_node = None
                            st.rerun()
                        except ValueError:
                            st.error("X and Y must be numbers. Please fix and try again.")
                    else:
                        st.error("Please enter a node name.")
            with col_b2:
                if st.button("✕", key="btn_clear_node", help="Clear form"):
                    st.session_state.form_node_name = ''
                    st.session_state.form_node_x = ''
                    st.session_state.form_node_y = ''
                    st.session_state.editing_node = None
                    st.rerun()
        
        # ==================== MEMBERS TAB ====================
        with tabs[1]:
            if st.session_state.members:
                mem_data = []
                for mname, n1, n2 in st.session_state.members:
                    x1, y1 = st.session_state.nodes.get(n1, (0,0))
                    x2, y2 = st.session_state.nodes.get(n2, (0,0))
                    L = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                    mem_data.append({"Member": mname, "Start": n1, "End": n2, "Length (m)": f"{L:.2f}"})
                df = pd.DataFrame(mem_data)
                
                st.caption(lang['tap_edit'])
                selected = st.dataframe(
                    df, hide_index=True, use_container_width=True,
                    selection_mode="single-row", on_select="rerun", key="mem_tbl"
                )
                
                if selected and len(selected.selection.rows) > 0:
                    idx = selected.selection.rows[0]
                    clicked = st.session_state.members[idx]
                    if st.session_state.editing_member == clicked[0]:
                        st.session_state.delete_confirm_target = ('member', clicked[0])
                    else:
                        st.session_state.editing_member = clicked[0]
                        st.session_state.form_member_start = clicked[1]
                        st.session_state.form_member_end = clicked[2]
                        st.session_state.delete_confirm_target = None
                        st.rerun()
            
            if st.session_state.delete_confirm_target and st.session_state.delete_confirm_target[0] == 'member':
                target = st.session_state.delete_confirm_target[1]
                st.warning(f"{lang['delete_confirm']} **{target}**?")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(lang['yes_delete'], key="del_mem_yes"):
                        st.session_state.members = [m for m in st.session_state.members if m[0] != target]
                        st.session_state.member_loads = [l for l in st.session_state.member_loads if l[1] != target]
                        st.session_state.delete_confirm_target = None
                        st.session_state.editing_member = None
                        st.rerun()
                with c2:
                    if st.button(lang['cancel'], key="del_mem_no"):
                        st.session_state.delete_confirm_target = None
                        st.rerun()
            
            st.markdown("---")
            
            node_names = list(st.session_state.nodes.keys())
            
            if len(node_names) >= 2:
                c1, c2 = st.columns(2)
                with c1:
                    start_n = st.selectbox(
                        lang['start_node'], node_names,
                        index=node_names.index(st.session_state.form_member_start) if st.session_state.form_member_start in node_names else 0,
                        key="inp_mstart"
                    )
                with c2:
                    end_n = st.selectbox(
                        lang['end_node'], node_names,
                        index=node_names.index(st.session_state.form_member_end) if st.session_state.form_member_end in node_names else min(1, len(node_names)-1),
                        key="inp_mend"
                    )
                
                st.session_state.form_member_start = start_n
                st.session_state.form_member_end = end_n
                
                if st.button(lang['add_member'], key="btn_add_member", use_container_width=True):
                    if start_n and end_n and start_n != end_n:
                        member_name = f"{start_n}{end_n}"
                        # Check if already exists
                        if not any(m[0] == member_name for m in st.session_state.members):
                            st.session_state.members.append((member_name, start_n, end_n))
                            st.session_state.form_member_start = ''
                            st.session_state.form_member_end = ''
                            st.session_state.editing_member = None
                            st.rerun()
                        else:
                            st.error(f"Member {member_name} already exists.")
                    else:
                        st.error("Start and end nodes must be different.")
            else:
                st.info("Add at least 2 nodes first.")
        
        # ==================== SUPPORTS TAB ====================
        with tabs[2]:
            if st.session_state.supports:
                sup_data = []
                for nname, stype in st.session_state.supports.items():
                    sup_data.append({"Node": nname, "Type": stype})
                df = pd.DataFrame(sup_data)
                
                st.caption(lang['tap_edit'])
                selected = st.dataframe(
                    df, hide_index=True, use_container_width=True,
                    selection_mode="single-row", on_select="rerun", key="sup_tbl"
                )
                
                if selected and len(selected.selection.rows) > 0:
                    idx = selected.selection.rows[0]
                    clicked = list(st.session_state.supports.keys())[idx]
                    if st.session_state.editing_support_node == clicked:
                        st.session_state.delete_confirm_target = ('support', clicked)
                    else:
                        st.session_state.editing_support_node = clicked
                        st.session_state.form_support_node = clicked
                        st.session_state.form_support_type = st.session_state.supports[clicked]
                        st.session_state.delete_confirm_target = None
                        st.rerun()
            
            if st.session_state.delete_confirm_target and st.session_state.delete_confirm_target[0] == 'support':
                target = st.session_state.delete_confirm_target[1]
                st.warning(f"{lang['delete_confirm']} support at **{target}**?")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(lang['yes_delete'], key="del_sup_yes"):
                        del st.session_state.supports[target]
                        st.session_state.delete_confirm_target = None
                        st.session_state.editing_support_node = None
                        st.rerun()
                with c2:
                    if st.button(lang['cancel'], key="del_sup_no"):
                        st.session_state.delete_confirm_target = None
                        st.rerun()
            
            st.markdown("---")
            
            node_names = list(st.session_state.nodes.keys())
            
            if node_names:
                c1, c2 = st.columns(2)
                with c1:
                    sup_node = st.selectbox(
                        lang['support_node'], node_names,
                        index=node_names.index(st.session_state.form_support_node) if st.session_state.form_support_node in node_names else 0,
                        key="inp_snode"
                    )
                with c2:
                    sup_type = st.selectbox(
                        lang['support_type'], lang['support_types'],
                        index=lang['support_types'].index(st.session_state.form_support_type) if st.session_state.form_support_type in lang['support_types'] else 0,
                        key="inp_stype"
                    )
                
                st.session_state.form_support_node = sup_node
                st.session_state.form_support_type = sup_type
                
                if st.button(lang['add_support'], key="btn_add_support", use_container_width=True):
                    type_map = {
                        lang['support_types'][0]: 'pinned',
                        lang['support_types'][1]: 'roller_x',
                        lang['support_types'][2]: 'roller_y'
                    }
                    st.session_state.supports[sup_node] = type_map[sup_type]
                    st.session_state.form_support_node = ''
                    st.session_state.form_support_type = ''
                    st.session_state.editing_support_node = None
                    st.rerun()
            else:
                st.info("Add nodes first.")
        
        # ==================== LOADS TAB ====================
        with tabs[3]:
            all_loads_display = []
            for nname, (mag, ang) in st.session_state.joint_loads.items():
                all_loads_display.append({"Type": "On Node", "Location": nname, "kN": mag, "°": ang})
            for lname, mname, pos, mag, ang in st.session_state.member_loads:
                all_loads_display.append({"Type": "On Member", "Location": f"{mname} @{pos:.2f}", "Name": lname, "kN": mag, "°": ang})
            
            if all_loads_display:
                df = pd.DataFrame(all_loads_display)
                st.caption(lang['tap_edit'])
                st.dataframe(df, hide_index=True, use_container_width=True)
            
            st.markdown("---")
            
            load_type = st.selectbox(lang['load_type'], lang['load_types'], key="inp_ltype")
            st.session_state.form_load_type = load_type
            
            if load_type == lang['load_types'][0]:  # On Node
                c1, c2, c3 = st.columns(3)
                with c1:
                    load_name = st.text_input(lang['load_name'], value=st.session_state.form_load_name, placeholder="e.g. F1", key="inp_lname")
                with c2:
                    node_names = list(st.session_state.nodes.keys())
                    load_target = st.selectbox(lang['load_location'], node_names if node_names else ["-"], key="inp_ltarget")
                with c3:
                    # Placeholder
                    st.write("")
                
                c4, c5 = st.columns(2)
                with c4:
                    load_mag = st.text_input(lang['load_magnitude'], value=st.session_state.form_load_mag, placeholder="10", key="inp_lmag")
                with c5:
                    load_ang = st.text_input(lang['load_angle'], value=st.session_state.form_load_ang, placeholder="270", key="inp_lang")
                
                st.session_state.form_load_name = load_name
                st.session_state.form_load_target = load_target
                st.session_state.form_load_mag = load_mag
                st.session_state.form_load_ang = load_ang
                
                if st.button(lang['add_load'], key="btn_add_load_joint", use_container_width=True):
                    if load_name and load_target in st.session_state.nodes:
                        try:
                            mf = float(load_mag) if load_mag else 0
                            af = float(load_ang) if load_ang else 0
                            st.session_state.joint_loads[load_target] = (mf, af)
                            st.session_state.form_load_name = ''
                            st.session_state.form_load_mag = ''
                            st.session_state.form_load_ang = ''
                            st.rerun()
                        except ValueError:
                            st.error("Magnitude and angle must be numbers.")
                    else:
                        st.error("Enter a load name and select a valid node.")
            
            else:  # On Member (any position)
                member_names = [m[0] for m in st.session_state.members]
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    load_name = st.text_input(lang['load_name'], value=st.session_state.form_load_name, placeholder="e.g. W1", key="inp_lname2")
                with c2:
                    load_target = st.selectbox(lang['load_member'], member_names if member_names else ["-"], key="inp_ltarget2")
                with c3:
                    load_pos = st.text_input(lang['load_position'], value=st.session_state.form_load_pos, placeholder="0.5 = middle", key="inp_lpos")
                
                c4, c5 = st.columns(2)
                with c4:
                    load_mag = st.text_input(lang['load_magnitude'], value=st.session_state.form_load_mag, placeholder="10", key="inp_lmag2")
                with c5:
                    load_ang = st.text_input(lang['load_angle'], value=st.session_state.form_load_ang, placeholder="270", key="inp_lang2")
                
                st.session_state.form_load_name = load_name
                st.session_state.form_load_target = load_target
                st.session_state.form_load_pos = load_pos
                st.session_state.form_load_mag = load_mag
                st.session_state.form_load_ang = load_ang
                
                if st.button(lang['add_load'], key="btn_add_load_member", use_container_width=True):
                    if load_name and load_target in member_names:
                        try:
                            mf = float(load_mag) if load_mag else 0
                            af = float(load_ang) if load_ang else 0
                            pf = float(load_pos) if load_pos else 0.5
                            pf = max(0.0, min(1.0, pf))  # Clamp between 0 and 1
                            st.session_state.member_loads.append((load_name, load_target, pf, mf, af))
                            st.session_state.form_load_name = ''
                            st.session_state.form_load_mag = ''
                            st.session_state.form_load_ang = ''
                            st.session_state.form_load_pos = ''
                            st.rerun()
                        except ValueError:
                            st.error("Magnitude, angle, and position must be numbers.")
                    else:
                        st.error("Enter a load name and select a valid member.")
    
    # ===== ACTION BUTTONS =====
    st.markdown("---")
    col_a, col_r = st.columns([3, 1])
    
    with col_a:
        if st.button(f"🚀 {lang['analyze']}", use_container_width=True, type="primary"):
            if len(st.session_state.nodes) >= 2 and len(st.session_state.members) >= 1:
                with st.spinner("Analyzing..."):
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
            reset_keys = ['nodes', 'members', 'supports', 'joint_loads', 'member_loads',
                         'results', 'editing_node', 'editing_member', 'editing_support_node',
                         'editing_load_key', 'delete_confirm_target',
                         'form_node_name', 'form_node_x', 'form_node_y',
                         'form_member_start', 'form_member_end',
                         'form_support_node', 'form_support_type',
                         'form_load_name', 'form_load_type', 'form_load_target',
                         'form_load_pos', 'form_load_mag', 'form_load_ang']
            for key in reset_keys:
                if key in ['nodes', 'supports', 'joint_loads', 'results']:
                    st.session_state[key] = {}
                else:
                    st.session_state[key] = [] if key == 'members' or key == 'member_loads' else None if 'editing' in key or 'delete' in key or 'form_' in key else None
                if 'form_' in key:
                    st.session_state[key] = ''
            st.rerun()
    
    # ===== RESULTS SECTION (below drawing) =====
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
        
        # Export
        if st.button(f"📥 {lang['export']}"):
            buf = io.StringIO()
            buf.write("2D TRUSS ANALYSIS RESULTS\n" + "="*50 + "\n\n")
            for nname, (fx, fy) in res['reactions'].items():
                R = np.sqrt(fx**2+fy**2)
                buf.write(f"Reaction at {nname}: Fx={fx:.3f}, Fy={fy:.3f}, R={R:.3f} kN\n")
            buf.write("\n")
            for mname, f in res['member_forces'].items():
                buf.write(f"Member {mname}: {abs(f):.3f} kN ({'Tension' if f>=0 else 'Compression'})\n")
            buf.write("\n")
            for i, nname in enumerate(res['node_names']):
                ux = res['displacements'][2*i] * 1000
                uy = res['displacements'][2*i+1] * 1000
                buf.write(f"Node {nname}: Ux={ux:.4f} mm, Uy={uy:.4f} mm\n")
            
            st.download_button("Download Results", buf.getvalue(), "truss_results.txt", "text/plain")
    
    elif not st.session_state.nodes:
        st.info(lang['no_results'])

if __name__ == "__main__":
    main()