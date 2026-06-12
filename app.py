"""
2D Truss Analysis System - Professional Edition
Fixed: mid-member loads, live preview, dark theme, proper inputs, zoom
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrowPatch, Circle, Polygon
from matplotlib.lines import Line2D
import io

# ============================================================================
# FORCE DARK THEME AND PROPER ZOOM
# ============================================================================

st.set_page_config(
    page_title="2D Truss Analysis Pro",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Force dark theme
st.markdown("""
<style>
    /* Force dark theme everywhere */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Dark inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: #262730 !important;
        color: #fafafa !important;
        border-color: #4a4a5a !important;
    }
    
    /* Dark dataframes */
    .stDataFrame {
        background-color: #1e2130 !important;
    }
    
    .stDataFrame table {
        color: #fafafa !important;
    }
    
    /* Dark buttons */
    .stButton button {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(30, 60, 114, 0.4) !important;
    }
    
    /* Cards */
    .card {
        background: linear-gradient(135deg, #1e2130 0%, #2a2d3e 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #3a3d4e;
        margin-bottom: 1rem;
    }
    
    /* Main title */
    .main-title {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 50%, #4a90e2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: #8a8fa0;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Remove row numbers from tables */
    .stDataFrame [data-testid="stTable"] th:first-child {
        display: none;
    }
    
    /* Fix number input appearance */
    input[type="number"] {
        -moz-appearance: textfield;
    }
    
    input[type="number"]::-webkit-inner-spin-button,
    input[type="number"]::-webkit-outer-spin-button {
        opacity: 1;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1e2130;
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #8a8fa0 !important;
        background-color: transparent !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2a5298 !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    /* Make scrollbar dark */
    ::-webkit-scrollbar {
        width: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #1e2130;
    }
    ::-webkit-scrollbar-thumb {
        background: #3a3d4e;
        border-radius: 5px;
    }
    
    /* Fix for mobile/desktop consistency */
    @media (prefers-color-scheme: light) {
        .stApp {
            background-color: #0e1117 !important;
            color: #fafafa !important;
        }
    }
</style>

<script>
    // Enable pinch zoom on mobile
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
        "language_label": "Language",
        "node_tab": "📌 Nodes",
        "member_tab": "🔗 Members",
        "support_tab": "🏗️ Supports",
        "load_tab": "⬇️ Loads",
        "analyze_btn": "🚀 Analyze Structure",
        "reset_btn": "🔄 Reset",
        "live_preview": "📐 Live Preview",
        "node_id": "Node ID",
        "x_coord": "X (m)",
        "y_coord": "Y (m)",
        "add_node": "Add Node",
        "member_id": "Member ID",
        "start_node": "Start Node",
        "end_node": "End Node",
        "add_member": "Add Member",
        "support_node": "Node ID",
        "support_type": "Support Type",
        "support_types": ["Pinned (Fix X, Y)", "Roller X (Free X)", "Roller Y (Free Y)"],
        "add_support": "Add Support",
        "load_type": "Load Type",
        "load_types": ["Joint Load", "Member Load (Middle)"],
        "load_node": "Node ID",
        "load_member": "Member ID",
        "load_magnitude": "Magnitude (kN)",
        "load_angle": "Angle (degrees from +X)",
        "add_load": "Add Load",
        "reactions_title": "🔴 Support Reactions",
        "member_forces_title": "🔵 Member Forces",
        "displacements_title": "📐 Nodal Displacements",
        "node_id_col": "Node",
        "fx": "Fx (kN)",
        "fy": "Fy (kN)",
        "resultant": "Resultant (kN)",
        "angle": "Angle (°)",
        "member_id_col": "Member",
        "force": "Force (kN)",
        "type": "Type",
        "tension": "TENSION",
        "compression": "COMPRESSION",
        "ux": "Ux (mm)",
        "uy": "Uy (mm)",
        "no_results": "Add your structure and click 'Analyze Structure' to see results.",
        "warning_min": "Need at least 2 nodes and 1 member.",
        "error_structure": "Structure error. Check geometry and supports.",
        "legend_tension": "Blue = Tension",
        "legend_compression": "Red = Compression",
        "legend_load": "Green = Load",
        "legend_reaction": "Orange = Reaction",
        "export_btn": "📥 Export Results",
        "node_table": "Node Coordinates",
        "member_table": "Member Connectivity",
        "support_table": "Support Conditions",
        "load_table": "Applied Loads",
        "delete_node": "Delete Selected Node",
        "delete_member": "Delete Selected Member",
        "delete_support": "Delete Selected Support",
        "delete_load": "Delete Selected Load",
        "select_delete_node": "Select node to delete",
        "select_delete_member": "Select member to delete",
        "select_delete_support": "Select node support to delete",
        "select_delete_load": "Select load to delete",
    },
    "Persian": {
        "title": "سیستم تحلیل خرپا دو بعدی",
        "subtitle": "نرم‌افزار حرفه‌ای تحلیل به روش سختی ماتریسی",
        "language_label": "زبان",
        "node_tab": "📌 گره‌ها",
        "member_tab": "🔗 اعضا",
        "support_tab": "🏗️ تکیه‌گاه‌ها",
        "load_tab": "⬇️ بارها",
        "analyze_btn": "🚀 تحلیل سازه",
        "reset_btn": "🔄 بازنشانی",
        "live_preview": "📐 پیش‌نمایش زنده",
        "node_id": "شماره گره",
        "x_coord": "X (متر)",
        "y_coord": "Y (متر)",
        "add_node": "افزودن گره",
        "member_id": "شماره عضو",
        "start_node": "گره شروع",
        "end_node": "گره پایان",
        "add_member": "افزودن عضو",
        "support_node": "شماره گره",
        "support_type": "نوع تکیه‌گاه",
        "support_types": ["گیردار (ثابت X, Y)", "غلتک X (آزاد X)", "غلتک Y (آزاد Y)"],
        "add_support": "افزودن تکیه‌گاه",
        "load_type": "نوع بار",
        "load_types": ["بار گرهی", "بار وسط عضو"],
        "load_node": "شماره گره",
        "load_member": "شماره عضو",
        "load_magnitude": "بزرگی (کیلونیوتن)",
        "load_angle": "زاویه (درجه از +X)",
        "add_load": "افزودن بار",
        "reactions_title": "🔴 عکس‌العمل‌های تکیه‌گاهی",
        "member_forces_title": "🔵 نیروهای اعضا",
        "displacements_title": "📐 جابجایی‌های گرهی",
        "node_id_col": "گره",
        "fx": "Fx (kN)",
        "fy": "Fy (kN)",
        "resultant": "برآیند (kN)",
        "angle": "زاویه (°)",
        "member_id_col": "عضو",
        "force": "نیرو (kN)",
        "type": "نوع",
        "tension": "کششی",
        "compression": "فشاری",
        "ux": "Ux (mm)",
        "uy": "Uy (mm)",
        "no_results": "سازه خود را تعریف کرده و دکمه تحلیل را بزنید.",
        "warning_min": "حداقل به ۲ گره و ۱ عضو نیاز است.",
        "error_structure": "خطای سازه. هندسه و تکیه‌گاه‌ها را بررسی کنید.",
        "legend_tension": "آبی = کشش",
        "legend_compression": "قرمز = فشار",
        "legend_load": "سبز = بار",
        "legend_reaction": "نارنجی = عکس‌العمل",
        "export_btn": "📥 خروجی نتایج",
        "node_table": "مختصات گره‌ها",
        "member_table": "اتصالات اعضا",
        "support_table": "شرایط تکیه‌گاهی",
        "load_table": "بارهای اعمالی",
        "delete_node": "حذف گره انتخاب شده",
        "delete_member": "حذف عضو انتخاب شده",
        "delete_support": "حذف تکیه‌گاه انتخاب شده",
        "delete_load": "حذف بار انتخاب شده",
        "select_delete_node": "گره مورد نظر را انتخاب کنید",
        "select_delete_member": "عضو مورد نظر را انتخاب کنید",
        "select_delete_support": "تکیه‌گاه مورد نظر را انتخاب کنید",
        "select_delete_load": "بار مورد نظر را انتخاب کنید",
    }
}

# ============================================================================
# CORE ENGINEERING SOLVER WITH MID-MEMBER LOADS
# ============================================================================

class TrussAnalyzer:
    """2D Truss Analysis with mid-member load support"""
    
    def __init__(self, nodes, members, supports, joint_loads, member_loads, E=200e6):
        self.nodes = nodes
        self.members = members
        self.supports = supports
        self.joint_loads = joint_loads
        self.member_loads = member_loads
        self.E = E
        self.A = 0.01
        self.n_nodes = len(nodes)
        self.n_dofs = 2 * self.n_nodes
        
        # Convert member loads to equivalent nodal loads
        self.equivalent_loads = self._convert_member_loads()
        
        # Combine all loads
        self.all_loads = {}
        for node_id, (mag, ang) in self.joint_loads.items():
            self.all_loads[node_id] = self.all_loads.get(node_id, [0, 0])
            ang_rad = np.radians(ang)
            self.all_loads[node_id][0] += mag * np.cos(ang_rad)
            self.all_loads[node_id][1] += mag * np.sin(ang_rad)
        
        for node_id, (fx, fy) in self.equivalent_loads.items():
            self.all_loads[node_id] = self.all_loads.get(node_id, [0, 0])
            self.all_loads[node_id][0] += fx
            self.all_loads[node_id][1] += fy
        
        self.K_global = np.zeros((self.n_dofs, self.n_dofs))
        self.F_global = np.zeros(self.n_dofs)
        self.U_global = None
        self.member_forces = {}
        self.reactions = {}
        
        self._assemble_stiffness()
        self._apply_loads()
        self._apply_boundary_conditions()
        self._solve()
    
    def _convert_member_loads(self):
        """Convert mid-member loads to equivalent nodal loads"""
        equiv = {}
        
        for member_id, magnitude, angle_deg in self.member_loads:
            # Find the member
            member_found = False
            for mid, ni, nj in self.members:
                if mid == member_id:
                    member_found = True
                    break
            
            if not member_found:
                continue
            
            # Get member length and orientation
            xi, yi = self.nodes[ni]
            xj, yj = self.nodes[nj]
            L = np.sqrt((xj - xi)**2 + (yj - yi)**2)
            
            if L == 0:
                continue
            
            # For a load at mid-span of a beam, equivalent nodal forces:
            # Simply divide the load equally to both ends
            # This is a simplification - for pure truss action, we project onto member axis
            ang_rad = np.radians(angle_deg)
            fx = magnitude * np.cos(ang_rad)
            fy = magnitude * np.sin(ang_rad)
            
            # Member direction cosines
            c = (xj - xi) / L
            s = (yj - yi) / L
            
            # Project load onto member direction (axial component)
            axial_component = fx * c + fy * s
            
            # Distribute to both nodes
            equiv[ni] = equiv.get(ni, [0, 0])
            equiv[ni][0] += axial_component * c * 0.5
            equiv[ni][1] += axial_component * s * 0.5
            
            equiv[nj] = equiv.get(nj, [0, 0])
            equiv[nj][0] += axial_component * c * 0.5
            equiv[nj][1] += axial_component * s * 0.5
        
        return equiv
    
    def _get_dof_indices(self, node_id):
        base = 2 * (node_id - 1)
        return base, base + 1
    
    def _assemble_stiffness(self):
        for member_id, node_i, node_j in self.members:
            xi, yi = self.nodes[node_i]
            xj, yj = self.nodes[node_j]
            dx, dy = xj - xi, yj - yi
            L = np.sqrt(dx**2 + dy**2)
            if L == 0:
                continue
            c, s = dx / L, dy / L
            
            k = (self.E * self.A / L) * np.array([
                [c*c, c*s, -c*c, -c*s],
                [c*s, s*s, -c*s, -s*s],
                [-c*c, -c*s, c*c, c*s],
                [-c*s, -s*s, c*s, s*s]
            ])
            
            dof_i = self._get_dof_indices(node_i)
            dof_j = self._get_dof_indices(node_j)
            dofs = [dof_i[0], dof_i[1], dof_j[0], dof_j[1]]
            
            for ii, gi in enumerate(dofs):
                for jj, gj in enumerate(dofs):
                    self.K_global[gi, gj] += k[ii, jj]
    
    def _apply_loads(self):
        for node_id, (fx, fy) in self.all_loads.items():
            dof_x, dof_y = self._get_dof_indices(node_id)
            self.F_global[dof_x] += fx
            self.F_global[dof_y] += fy
    
    def _apply_boundary_conditions(self):
        penalty = 1e15
        for node_id, support_type in self.supports.items():
            dof_x, dof_y = self._get_dof_indices(node_id)
            if support_type == 'pinned':
                self.K_global[dof_x, dof_x] += penalty
                self.K_global[dof_y, dof_y] += penalty
            elif support_type == 'roller_x':
                self.K_global[dof_y, dof_y] += penalty
            elif support_type == 'roller_y':
                self.K_global[dof_x, dof_x] += penalty
    
    def _solve(self):
        try:
            self.U_global = np.linalg.solve(self.K_global, self.F_global)
            
            # Member forces
            for member_id, node_i, node_j in self.members:
                xi, yi = self.nodes[node_i]
                xj, yj = self.nodes[node_j]
                dx, dy = xj - xi, yj - yi
                L = np.sqrt(dx**2 + dy**2)
                if L == 0:
                    self.member_forces[member_id] = 0
                    continue
                c, s = dx / L, dy / L
                
                dof_i = self._get_dof_indices(node_i)
                dof_j = self._get_dof_indices(node_j)
                u_i = self.U_global[dof_i[0]]
                v_i = self.U_global[dof_i[1]]
                u_j = self.U_global[dof_j[0]]
                v_j = self.U_global[dof_j[1]]
                
                force = (self.E * self.A / L) * (c*(u_j - u_i) + s*(v_j - v_i))
                
                # Add mid-member load effect if applicable
                for mload_id, mag, ang in self.member_loads:
                    if mload_id == member_id:
                        ang_rad = np.radians(ang)
                        axial_component = mag * np.cos(ang_rad) * c + mag * np.sin(ang_rad) * s
                        force += axial_component * 0.5
                        break
                
                self.member_forces[member_id] = force
            
            # Reactions
            for node_id in self.supports:
                dof_x, dof_y = self._get_dof_indices(node_id)
                rx = np.dot(self.K_global[dof_x, :], self.U_global) - self.F_global[dof_x]
                ry = np.dot(self.K_global[dof_y, :], self.U_global) - self.F_global[dof_y]
                self.reactions[node_id] = (rx, ry)
                
        except np.linalg.LinAlgError:
            self.U_global = None
            self.member_forces = {}
            self.reactions = {}

# ============================================================================
# VISUALIZATION MODULE
# ============================================================================

def plot_truss(nodes, members, supports, joint_loads, member_loads, 
               member_forces=None, reactions=None, lang_dict=None):
    if lang_dict is None:
        lang_dict = LANGUAGES["English"]
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')
    
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2, linestyle='--', color='#4a4a5a')
    ax.set_xlabel('X (m)', fontsize=12, color='#fafafa')
    ax.set_ylabel('Y (m)', fontsize=12, color='#fafafa')
    ax.set_title('2D Truss Structure', fontsize=14, fontweight='bold', color='#fafafa')
    ax.tick_params(colors='#8a8fa0')
    
    for spine in ax.spines.values():
        spine.set_color('#4a4a5a')
    
    all_x = [coord[0] for coord in nodes.values()]
    all_y = [coord[1] for coord in nodes.values()]
    if not all_x:
        all_x, all_y = [0, 1], [0, 1]
    
    x_min, x_max = min(all_x), max(all_x)
    y_min, y_max = min(all_y), max(all_y)
    margin = max(x_max - x_min, y_max - y_min, 1) * 0.3 + 1
    ax.set_xlim(x_min - margin, x_max + margin)
    ax.set_ylim(y_min - margin, y_max + margin)
    
    # Draw members
    for member_id, node_i, node_j in members:
        xi, yi = nodes[node_i]
        xj, yj = nodes[node_j]
        
        if member_forces and member_id in member_forces:
            force = member_forces[member_id]
            color = '#4a90e2' if force >= 0 else '#e74c3c'
            lw = 3
        else:
            color = '#5a5a6a'
            lw = 2
        
        ax.plot([xi, xj], [yi, yj], color=color, linewidth=lw, zorder=2)
        
        mid_x, mid_y = (xi + xj) / 2, (yi + yj) / 2
        if member_forces and member_id in member_forces:
            force_val = abs(member_forces[member_id])
            force_type = 'T' if member_forces[member_id] >= 0 else 'C'
            ax.annotate(f'M{member_id}\n{force_val:.1f} kN ({force_type})',
                       (mid_x, mid_y), fontsize=7, ha='center', va='center',
                       color='#fafafa',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='#1e2130', 
                                edgecolor='#4a4a5a', alpha=0.9))
        else:
            ax.annotate(f'M{member_id}', (mid_x, mid_y), fontsize=7, ha='center',
                       color='#8a8fa0')
    
    # Draw nodes
    for node_id, (x, y) in nodes.items():
        ax.plot(x, y, 'o', color='#fafafa', markersize=12, zorder=4)
        ax.plot(x, y, 'o', color='#2a5298', markersize=8, zorder=5)
        ax.annotate(f'{node_id}', (x, y), fontsize=10, fontweight='bold',
                   color='#fafafa', xytext=(8, 8), textcoords='offset points')
    
    # Draw supports
    for node_id, support_type in supports.items():
        x, y = nodes[node_id]
        if support_type == 'pinned':
            triangle = Polygon([[x-0.4, y-0.4], [x+0.4, y-0.4], [x, y-0.05]],
                              facecolor='#5a5a6a', edgecolor='#fafafa', zorder=3)
            ax.add_patch(triangle)
            for i in range(4):
                ax.plot([x-0.35+i*0.23, x-0.3+i*0.23], [y-0.4, y-0.55],
                       color='#fafafa', linewidth=1.5)
        elif support_type == 'roller_x':
            circle = Circle((x, y-0.25), 0.18, facecolor='#1e2130', 
                           edgecolor='#fafafa', zorder=3)
            ax.add_patch(circle)
            ax.plot([x-0.4, x+0.4], [y-0.55, y-0.55], color='#fafafa', linewidth=1.5)
            for i in range(3):
                ax.plot([x-0.35+i*0.35, x-0.35+i*0.35], [y-0.55, y-0.65],
                       color='#fafafa', linewidth=1)
        elif support_type == 'roller_y':
            circle = Circle((x-0.25, y), 0.18, facecolor='#1e2130',
                           edgecolor='#fafafa', zorder=3)
            ax.add_patch(circle)
            ax.plot([x-0.55, x-0.55], [y-0.4, y+0.4], color='#fafafa', linewidth=1.5)
    
    # Scale for arrows
    all_forces = []
    for mag, _ in joint_loads.values():
        all_forces.append(mag)
    for _, mag, _ in member_loads:
        all_forces.append(mag)
    
    max_force = max(all_forces) if all_forces else 1
    scale = (x_max - x_min) / max_force * 0.2 if max_force > 0 else 1
    
    # Draw joint loads
    for node_id, (magnitude, angle_deg) in joint_loads.items():
        x, y = nodes[node_id]
        angle_rad = np.radians(angle_deg)
        dx = -magnitude * np.cos(angle_rad) * scale
        dy = -magnitude * np.sin(angle_rad) * scale
        
        ax.arrow(x + dx, y + dy, -dx*0.9, -dy*0.9,
                head_width=0.2, head_length=0.3, fc='#2ecc71', ec='#2ecc71',
                linewidth=2, zorder=6)
        ax.annotate(f'{magnitude:.1f} kN', (x + dx*1.1, y + dy*1.1),
                   fontsize=8, color='#2ecc71', fontweight='bold')
    
    # Draw mid-member loads
    for member_id, magnitude, angle_deg in member_loads:
        for mid, ni, nj in members:
            if mid == member_id:
                xi, yi = nodes[ni]
                xj, yj = nodes[nj]
                mx, my = (xi + xj) / 2, (yi + yj) / 2
                
                angle_rad = np.radians(angle_deg)
                dx = -magnitude * np.cos(angle_rad) * scale
                dy = -magnitude * np.sin(angle_rad) * scale
                
                ax.arrow(mx + dx, my + dy, -dx*0.9, -dy*0.9,
                        head_width=0.2, head_length=0.3, fc='#f39c12', ec='#f39c12',
                        linewidth=2, zorder=6)
                ax.annotate(f'{magnitude:.1f} kN', (mx + dx*1.1, my + dy*1.1),
                           fontsize=8, color='#f39c12', fontweight='bold')
                break
    
    # Draw reactions
    if reactions:
        for node_id, (rx, ry) in reactions.items():
            x, y = nodes[node_id]
            if abs(rx) > 0.001 or abs(ry) > 0.001:
                dx, dy = rx * scale * 0.8, ry * scale * 0.8
                ax.arrow(x - dx, y - dy, dx*0.9, dy*0.9,
                        head_width=0.2, head_length=0.3, fc='#e67e22', ec='#e67e22',
                        linewidth=2.5, zorder=6)
                R = np.sqrt(rx**2 + ry**2)
                ax.annotate(f'R={R:.1f}', (x - dx*1.1, y - dy*1.1),
                           fontsize=8, color='#e67e22', fontweight='bold')
    
    # Legend
    legend_text = f"🔵 {lang_dict['legend_tension']}  🔴 {lang_dict['legend_compression']}  🟢 {lang_dict['legend_load']}  🟠 {lang_dict['legend_reaction']}"
    ax.text(0.02, 0.98, legend_text, transform=ax.transAxes,
           fontsize=8, color='#fafafa', verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='#1e2130', edgecolor='#4a4a5a', alpha=0.9))
    
    plt.tight_layout()
    return fig

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    
    # Initialize session state
    if 'language' not in st.session_state:
        st.session_state.language = "English"
    if 'nodes' not in st.session_state:
        st.session_state.nodes = {}
    if 'members' not in st.session_state:
        st.session_state.members = []
    if 'supports' not in st.session_state:
        st.session_state.supports = {}
    if 'joint_loads' not in st.session_state:
        st.session_state.joint_loads = {}
    if 'member_loads' not in st.session_state:
        st.session_state.member_loads = []
    if 'results' not in st.session_state:
        st.session_state.results = None
    
    # Language selector
    col_lang, col_title = st.columns([1, 5])
    with col_lang:
        st.session_state.language = st.selectbox(
            "🌐",
            ["English", "Persian"],
            key="lang_sel",
            label_visibility="collapsed"
        )
    
    lang = LANGUAGES[st.session_state.language]
    
    # Title
    st.markdown(f'<div class="main-title">{lang["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{lang["subtitle"]}</div>', unsafe_allow_html=True)
    
    # Input tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        lang['node_tab'], lang['member_tab'], 
        lang['support_tab'], lang['load_tab']
    ])
    
    # ===== NODES TAB =====
    with tab1:
        col_input, col_preview = st.columns([1, 1.2])
        
        with col_input:
            st.markdown(f"### {lang['node_table']}")
            
            if st.session_state.nodes:
                node_list = []
                for nid, (x, y) in st.session_state.nodes.items():
                    node_list.append({"Node": nid, "X (m)": x, "Y (m)": y})
                df = pd.DataFrame(node_list)
                st.dataframe(df, hide_index=True, use_container_width=True)
            
            with st.form("add_node", clear_on_submit=True):
                c1, c2, c3 = st.columns(3)
                with c1:
                    nid = st.text_input(lang['node_id'], key="nid_inp", placeholder="e.g. 1")
                with c2:
                    xc = st.text_input(lang['x_coord'], key="xc_inp", placeholder="e.g. 0")
                with c3:
                    yc = st.text_input(lang['y_coord'], key="yc_inp", placeholder="e.g. 0")
                
                if st.form_submit_button(lang['add_node']):
                    try:
                        nid_int = int(nid)
                        xf = float(xc)
                        yf = float(yc)
                        st.session_state.nodes[nid_int] = (xf, yf)
                        st.rerun()
                    except:
                        st.error("Invalid input. Use numbers only.")
            
            # Delete node
            if st.session_state.nodes:
                del_node = st.selectbox(lang['select_delete_node'], 
                                       list(st.session_state.nodes.keys()))
                if st.button(lang['delete_node'], key="del_node_btn"):
                    del st.session_state.nodes[del_node]
                    # Also remove connected members, supports, loads
                    st.session_state.members = [m for m in st.session_state.members 
                                               if m[1] != del_node and m[2] != del_node]
                    if del_node in st.session_state.supports:
                        del st.session_state.supports[del_node]
                    if del_node in st.session_state.joint_loads:
                        del st.session_state.joint_loads[del_node]
                    st.rerun()
        
        with col_preview:
            st.markdown(f"### {lang['live_preview']}")
            fig = plot_truss(
                st.session_state.nodes,
                st.session_state.members,
                st.session_state.supports,
                st.session_state.joint_loads,
                st.session_state.member_loads,
                lang_dict=lang
            )
            st.pyplot(fig)
    
    # ===== MEMBERS TAB =====
    with tab2:
        col_input, col_preview = st.columns([1, 1.2])
        
        with col_input:
            st.markdown(f"### {lang['member_table']}")
            
            if st.session_state.members:
                mem_list = []
                for mid, ni, nj in st.session_state.members:
                    mem_list.append({"Member": mid, "Start Node": ni, "End Node": nj})
                df = pd.DataFrame(mem_list)
                st.dataframe(df, hide_index=True, use_container_width=True)
            
            if len(st.session_state.nodes) >= 2:
                with st.form("add_member", clear