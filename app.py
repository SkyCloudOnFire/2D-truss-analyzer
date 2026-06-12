"""
2D Truss Analyzer
Clean, professional structural analysis tool
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Polygon, Circle
import io

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
# STYLING - Clean, modern, no emojis in titles
# ============================================================================

st.markdown("""
<style>
    /* Clean dark inputs and cards - but respect system background */
    .stTextInput input, .stNumberInput input {
        background-color: var(--st-color-secondary-bg) !important;
        border: 1px solid var(--st-color-border) !important;
        border-radius: 8px !important;
        padding: 0.5rem 0.75rem !important;
        font-size: 0.95rem !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #4a90e2 !important;
        box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.15) !important;
        outline: none !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: #1e3c72 !important;
        color: white !important;
        font-weight: 500 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.15s !important;
        letter-spacing: 0.2px !important;
    }
    .stButton > button:hover {
        background: #2a5298 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(30, 60, 114, 0.4) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Primary button */
    .stButton > button[kind="primary"] {
        background: #2a5298 !important;
    }
    
    /* Danger/delete styling */
    .delete-btn > button {
        background: transparent !important;
        color: #e74c3c !important;
        border: 1px solid #e74c3c !important;
    }
    .delete-btn > button:hover {
        background: rgba(231, 76, 60, 0.1) !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border: 1px solid var(--st-color-border) !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    .stDataFrame [data-testid="stTable"] th {
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.3px !important;
        padding: 0.6rem 0.8rem !important;
    }
    .stDataFrame [data-testid="stTable"] td {
        padding: 0.5rem 0.8rem !important;
        font-size: 0.9rem !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px !important;
        background: transparent !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0 !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.2px !important;
    }
    .stTabs [aria-selected="true"] {
        background: #1e3c72 !important;
        color: white !important;
    }
    
    /* Cards */
    .card {
        border: 1px solid var(--st-color-border);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 0.75rem;
    }
    
    /* Title */
    .app-title {
        font-size: 1.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0;
        letter-spacing: -0.3px;
        color: #1e3c72;
    }
    
    /* Section titles */
    .section-label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #8b949e;
        margin-bottom: 0.5rem;
    }
    
    /* Table row hover */
    .stDataFrame tr:hover td {
        cursor: pointer !important;
        background-color: rgba(74, 144, 226, 0.08) !important;
    }
    
    /* Selected row */
    .stDataFrame tr[aria-selected="true"] td {
        background-color: rgba(74, 144, 226, 0.15) !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(128,128,128,0.3); border-radius: 3px; }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #4a90e2 !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .app-title { font-size: 1.4rem; }
        .stTabs [data-baseweb="tab"] { padding: 0.5rem 0.8rem; font-size: 0.8rem; }
    }
</style>

<script>
    document.querySelector('meta[name="viewport"]').setAttribute('content', 
        'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes');
</script>
""", unsafe_allow_html=True)

# ============================================================================
# LANGUAGE SYSTEM - Clean, no emojis in titles
# ============================================================================

LANG = {
    "English": {
        "title": "2D Truss Analyzer",
        "language": "Language",
        "preview": "Preview",
        "nodes_tab": "Nodes",
        "members_tab": "Members",
        "supports_tab": "Supports",
        "loads_tab": "Loads",
        "analyze": "Analyze",
        "reset": "Reset",
        "node_name": "Name",
        "x_coord": "X (m)",
        "y_coord": "Y (m)",
        "add_node": "Add",
        "update_node": "Update",
        "delete_node": "Delete",
        "start_node": "Start",
        "end_node": "End",
        "add_member": "Add",
        "update_member": "Update",
        "delete_member": "Delete",
        "support_node": "Node",
        "support_type": "Type",
        "support_types": ["Pinned", "Roller X", "Roller Y"],
        "add_support": "Add",
        "delete_support": "Delete",
        "load_type": "Type",
        "load_types": ["On Node", "On Member"],
        "load_name": "Name",
        "load_location": "Location",
        "load_member": "Member",
        "load_position": "Position",
        "load_magnitude": "Force (kN)",
        "load_angle": "Angle",
        "add_load": "Add",
        "delete_load": "Delete",
        "nodes_table": "Nodes",
        "members_table": "Members",
        "supports_table": "Supports",
        "loads_table": "Loads",
        "click_to_edit": "Click row to edit",
        "reactions": "Reactions",
        "member_forces": "Member Forces",
        "displacements": "Displacements",
        "node_col": "Node",
        "fx": "Fx (kN)",
        "fy": "Fy (kN)",
        "resultant": "R (kN)",
        "angle": "Angle",
        "member_col": "Member",
        "length_col": "Length (m)",
        "force_col": "Force (kN)",
        "type": "Type",
        "tension": "Tension",
        "compression": "Compression",
        "ux": "Ux (mm)",
        "uy": "Uy (mm)",
        "no_data": "No data yet",
        "need_min": "Add at least 2 nodes and 1 member to analyze",
        "error_analysis": "Analysis failed. Check supports and geometry.",
        "legend": "Blue = Tension  |  Red = Compression  |  Green = Load  |  Orange = Reaction",
        "export": "Export Results",
        "length": "Length",
    },
    "Persian": {
        "title": "تحلیل‌گر خرپا دوبعدی",
        "language": "زبان",
        "preview": "پیش‌نمایش",
        "nodes_tab": "گره‌ها",
        "members_tab": "اعضا",
        "supports_tab": "تکیه‌گاه‌ها",
        "loads_tab": "بارها",
        "analyze": "تحلیل",
        "reset": "بازنشانی",
        "node_name": "نام",
        "x_coord": "X (متر)",
        "y_coord": "Y (متر)",
        "add_node": "افزودن",
        "update_node": "ویرایش",
        "delete_node": "حذف",
        "start_node": "شروع",
        "end_node": "پایان",
        "add_member": "افزودن",
        "update_member": "ویرایش",
        "delete_member": "حذف",
        "support_node": "گره",
        "support_type": "نوع",
        "support_types": ["گیردار", "غلتک X", "غلتک Y"],
        "add_support": "افزودن",
        "delete_support": "حذف",
        "load_type": "نوع",
        "load_types": ["روی گره", "روی عضو"],
        "load_name": "نام",
        "load_location": "محل",
        "load_member": "عضو",
        "load_position": "موقعیت",
        "load_magnitude": "نیرو (kN)",
        "load_angle": "زاویه",
        "add_load": "افزودن",
        "delete_load": "حذف",
        "nodes_table": "گره‌ها",
        "members_table": "اعضا",
        "supports_table": "تکیه‌گاه‌ها",
        "loads_table": "بارها",
        "click_to_edit": "برای ویرایش کلیک کنید",
        "reactions": "عکس‌العمل‌ها",
        "member_forces": "نیروهای اعضا",
        "displacements": "جابجایی‌ها",
        "node_col": "گره",
        "fx": "Fx (kN)",
        "fy": "Fy (kN)",
        "resultant": "برآیند (kN)",
        "angle": "زاویه",
        "member_col": "عضو",
        "length_col": "طول (متر)",
        "force_col": "نیرو (kN)",
        "type": "نوع",
        "tension": "کشش",
        "compression": "فشار",
        "ux": "Ux (mm)",
        "uy": "Uy (mm)",
        "no_data": "اطلاعاتی نیست",
        "need_min": "حداقل ۲ گره و ۱ عضو اضافه کنید",
        "error_analysis": "تحلیل ناموفق. تکیه‌گاه‌ها و هندسه را بررسی کنید.",
        "legend": "آبی = کشش  |  قرمز = فشار  |  سبز = بار  |  نارنجی = عکس‌العمل",
        "export": "خروجی",
        "length": "طول",
    }
}

# ============================================================================
# ENGINE - Matrix Stiffness Method
# ============================================================================

class Engine:
    def __init__(self, nodes, members, supports, joint_loads, member_loads):
        self.node_names = list(nodes.keys())
        self.node_coords = nodes
        self.idx = {n: i for i, n in enumerate(self.node_names)}
        self.n = len(self.node_names)
        self.ndof = 2 * self.n
        
        self.members = members
        self.supports = supports
        self.joint_loads = joint_loads
        self.member_loads = member_loads
        
        self.E = 200e6
        self.A = 0.01
        
        self.K = np.zeros((self.ndof, self.ndof))
        self.F = np.zeros(self.ndof)
        self.U = None
        self.forces = {}
        self.reactions = {}
        
        self._stiffness()
        self._loads()
        self._boundary()
        self._solve()
    
    def _dof(self, name):
        i = self.idx[name]
        return 2*i, 2*i+1
    
    def _stiffness(self):
        for n1, n2 in self.members:
            x1, y1 = self.node_coords[n1]
            x2, y2 = self.node_coords[n2]
            dx, dy = x2-x1, y2-y1
            L = np.hypot(dx, dy)
            if L < 1e-9: continue
            c, s = dx/L, dy/L
            k = (self.E*self.A/L) * np.array([
                [c*c, c*s, -c*c, -c*s],
                [c*s, s*s, -c*s, -s*s],
                [-c*c, -c*s, c*c, c*s],
                [-c*s, -s*s, c*s, s*s]
            ])
            d = [*self._dof(n1), *self._dof(n2)]
            for i in range(4):
                for j in range(4):
                    self.K[d[i], d[j]] += k[i, j]
    
    def _loads(self):
        for node, (mag, ang) in self.joint_loads.items():
            r = np.radians(ang)
            dx, dy = self._dof(node)
            self.F[dx] += mag * np.cos(r)
            self.F[dy] += mag * np.sin(r)
        
        for node, member, pos, mag, ang in self.member_loads:
            found = None
            for n1, n2 in self.members:
                if (n1, n2) == member or f"{n1}{n2}" == member or n1+n2 == member:
                    found = (n1, n2)
                    break
            if not found: continue
            n1, n2 = found
            x1, y1 = self.node_coords[n1]
            x2, y2 = self.node_coords[n2]
            L = np.hypot(x2-x1, y2-y1)
            if L < 1e-9: continue
            r = np.radians(ang)
            fx = mag * np.cos(r)
            fy = mag * np.sin(r)
            c = (x2-x1)/L
            s = (y2-y1)/L
            axial = fx*c + fy*s
            alpha = pos
            f1 = axial * (1 - alpha)
            f2 = axial * alpha
            d1x, d1y = self._dof(n1)
            d2x, d2y = self._dof(n2)
            self.F[d1x] += f1*c
            self.F[d1y] += f1*s
            self.F[d2x] += f2*c
            self.F[d2y] += f2*s
    
    def _boundary(self):
        big = 1e15
        for node, typ in self.supports.items():
            dx, dy = self._dof(node)
            if typ == 'pinned':
                self.K[dx,dx] += big; self.K[dy,dy] += big
            elif typ == 'roller_x':
                self.K[dy,dy] += big
            elif typ == 'roller_y':
                self.K[dx,dx] += big
    
    def _solve(self):
        try:
            self.U = np.linalg.solve(self.K, self.F)
            for n1, n2 in self.members:
                x1, y1 = self.node_coords[n1]; x2, y2 = self.node_coords[n2]
                L = np.hypot(x2-x1, y2-y1)
                if L < 1e-9: self.forces[(n1,n2)] = 0; continue
                c, s = (x2-x1)/L, (y2-y1)/L
                d1x, d1y = self._dof(n1); d2x, d2y = self._dof(n2)
                f = (self.E*self.A/L)*(c*(self.U[d2x]-self.U[d1x]) + s*(self.U[d2y]-self.U[d1y]))
                self.forces[(n1,n2)] = f
            for node in self.supports:
                dx, dy = self._dof(node)
                rx = self.K[dx]@self.U - self.F[dx]
                ry = self.K[dy]@self.U - self.F[dy]
                self.reactions[node] = (rx, ry)
        except:
            self.U = None

# ============================================================================
# DRAWING
# ============================================================================

def draw(nodes, members, supports, joint_loads, member_loads, 
         results=None, lang=None, highlight_delete=None):
    if lang is None:
        lang = LANG["English"]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_alpha(0)
    
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.12, linestyle='--', color='#888')
    ax.set_xlabel('X (m)', fontsize=10, color='#666')
    ax.set_ylabel('Y (m)', fontsize=10, color='#666')
    ax.tick_params(labelsize=8, colors='#888')
    
    xs = [c[0] for c in nodes.values()]
    ys = [c[1] for c in nodes.values()]
    if not xs: xs, ys = [0,10], [0,10]
    mrg = max(max(xs)-min(xs), max(ys)-min(ys), 2)*0.3 + 1
    ax.set_xlim(min(xs)-mrg, max(xs)+mrg)
    ax.set_ylim(min(ys)-mrg, max(ys)+mrg)
    
    forces_map = results.get('forces', {}) if results else {}
    reacts_map = results.get('reactions', {}) if results else {}
    
    # Members
    for n1, n2 in members:
        x1, y1 = nodes[n1]; x2, y2 = nodes[n2]
        key = (n1, n2)
        if key in forces_map:
            f = forces_map[key]
            color = '#2e86de' if f >= 0 else '#e74c3c'
            lw = 3.5
            ft = 'T' if f >= 0 else 'C'
            label = f'{n1}{n2}  {abs(f):.1f}kN ({ft})'
        else:
            color = '#999'
            lw = 2
            L = np.hypot(x2-x1, y2-y1)
            label = f'{n1}{n2}  {L:.2f}m'
        
        is_hl = highlight_delete and (n1, n2) == highlight_delete
        if is_hl:
            color = '#e74c3c'
            lw = 4
            ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, zorder=2, alpha=0.6)
            ax.plot([x1, x2], [y1, y2], color='#ff6b6b', linewidth=lw+2, zorder=1, alpha=0.3)
        else:
            ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, zorder=2)
        
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.annotate(label, (mx, my), fontsize=7, ha='center', va='center',
                   fontweight='bold', color='#222' if not is_hl else '#e74c3c',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                            edgecolor='#ddd', alpha=0.92))
    
    # Nodes
    for name, (x, y) in nodes.items():
        ax.plot(x, y, 'o', color='white', markersize=12, zorder=5, markeredgecolor='#555', markeredgewidth=2)
        ax.plot(x, y, 'o', color='#2a5298', markersize=8, zorder=6)
        ax.annotate(name, (x, y), fontsize=10, fontweight='bold', color='#222',
                   xytext=(9, 9), textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#ddd', alpha=0.9))
    
    # Supports
    for node, typ in supports.items():
        x, y = nodes[node]
        if typ == 'pinned':
            tri = Polygon([[x-0.45, y-0.45], [x+0.45, y-0.45], [x, y]],
                         facecolor='#888', edgecolor='#444', zorder=3, linewidth=1.5)
            ax.add_patch(tri)
            for i in range(3):
                ax.plot([x-0.4+i*0.4, x-0.35+i*0.4], [y-0.45, y-0.6], color='#444', linewidth=1.2)
        elif typ == 'roller_x':
            c = Circle((x, y-0.28), 0.18, facecolor='white', edgecolor='#444', zorder=3, linewidth=1.5)
            ax.add_patch(c)
            ax.plot([x-0.45, x+0.45], [y-0.6, y-0.6], color='#444', linewidth=1.5)
        elif typ == 'roller_y':
            c = Circle((x-0.28, y), 0.18, facecolor='white', edgecolor='#444', zorder=3, linewidth=1.5)
            ax.add_patch(c)
            ax.plot([x-0.6, x-0.6], [y-0.45, y+0.45], color='#444', linewidth=1.5)
    
    # Scale
    all_f = [mag for mag,_ in joint_loads.values()]
    for _,_,_,mag,_ in member_loads: all_f.append(mag)
    mx_f = max(all_f) if all_f else 1
    scale = (max(xs)-min(xs))/mx_f*0.15 if mx_f > 0 else 0.5
    
    # Joint loads
    for node, (mag, ang) in joint_loads.items():
        x, y = nodes[node]
        r = np.radians(ang)
        dx = -mag*np.cos(r)*scale
        dy = -mag*np.sin(r)*scale
        ax.arrow(x+dx, y+dy, -dx*0.85, -dy*0.85,
                head_width=0.22, head_length=0.3, fc='#27ae60', ec='#27ae60',
                linewidth=2.2, zorder=8)
        ax.annotate(f'{mag:.1f}kN', (x+dx*1.15, y+dy*1.15),
                   fontsize=7.5, color='#1e8449', fontweight='bold')
    
    # Member loads
    for _, member, pos, mag, ang in member_loads:
        found = None
        for n1, n2 in members:
            if (n1,n2)==member or f"{n1}{n2}"==member or n1+n2==member:
                found=(n1,n2); break
        if not found: continue
        n1,n2=found
        x1,y1=nodes[n1]; x2,y2=nodes[n2]
        lx = x1 + (x2-x1)*pos
        ly = y1 + (y2-y1)*pos
        r = np.radians(ang)
        dx = -mag*np.cos(r)*scale
        dy = -mag*np.sin(r)*scale
        ax.arrow(lx+dx, ly+dy, -dx*0.85, -dy*0.85,
                head_width=0.22, head_length=0.3, fc='#f39c12', ec='#f39c12',
                linewidth=2.2, zorder=8)
        ax.annotate(f'{mag:.1f}kN', (lx+dx*1.15, ly+dy*1.15),
                   fontsize=7.5, color='#d68910', fontweight='bold')
    
    # Reactions
    if reacts_map:
        for node, (rx, ry) in reacts_map.items():
            x, y = nodes[node]
            if abs(rx)>0.01 or abs(ry)>0.01:
                dx, dy = rx*scale*0.7, ry*scale*0.7
                ax.arrow(x-dx, y-dy, dx*0.85, dy*0.85,
                        head_width=0.22, head_length=0.3, fc='#e67e22', ec='#e67e22',
                        linewidth=2.5, zorder=8)
                R = np.hypot(rx, ry)
                ax.annotate(f'R={R:.1f}kN', (x-dx*1.15, y-dy*1.15),
                           fontsize=7.5, color='#ca6f1e', fontweight='bold')
    
    ax.text(0.5, 1.02, lang['legend'], transform=ax.transAxes,
           fontsize=7, color='#999', ha='center',
           bbox=dict(boxstyle='round', facecolor='white', edgecolor='#ddd', alpha=0.85))
    
    plt.tight_layout()
    return fig

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Init state
    for k, v in {
        'lang': 'English',
        'nodes': {},
        'members': [],
        'supports': {},
        'joint_loads': {},
        'member_loads': [],
        'results': None,
        'sel_node': None,
        'sel_member': None,
        'sel_support': None,
        'sel_load': None,
        'highlight_del': None,
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v
    
    t = LANG[st.session_state.lang]
    
    # Header
    cL, cT = st.columns([0.7, 5])
    with cL:
        st.session_state.lang = st.selectbox("", ["English","Persian"], 
                                             label_visibility="collapsed", key="langsel")
    
    st.markdown(f'<div class="app-title">{t["title"]}</div>', unsafe_allow_html=True)
    
    # Layout: Left=inputs, Right=drawing
    left, right = st.columns([1, 1.05])
    
    with right:
        # Drawing always visible
        res = st.session_state.results
        fig = draw(
            st.session_state.nodes,
            st.session_state.members,
            st.session_state.supports,
            st.session_state.joint_loads,
            st.session_state.member_loads,
            results=res,
            lang=t,
            highlight_delete=st.session_state.highlight_del
        )
        st.pyplot(fig)
        
        # Results below drawing
        if res:
            st.markdown("---")
            st.markdown(f"### {t['reactions']}")
            if res.get('reactions'):
                rd = []
                for n, (fx, fy) in res['reactions'].items():
                    R = np.hypot(fx, fy)
                    ang = np.degrees(np.arctan2(fy, fx))
                    rd.append({t['node_col']: n, t['fx']: f"{fx:.3f}", 
                              t['fy']: f"{fy:.3f}", t['resultant']: f"{R:.3f}",
                              t['angle']: f"{ang:.1f}"})
                st.dataframe(pd.DataFrame(rd), hide_index=True, use_container_width=True)
            
            col_f, col_d = st.columns(2)
            with col_f:
                st.markdown(f"### {t['member_forces']}")
                if res.get('forces'):
                    fd = []
                    for (n1,n2), f in res['forces'].items():
                        L = np.hypot(
                            st.session_state.nodes[n2][0]-st.session_state.nodes[n1][0],
                            st.session_state.nodes[n2][1]-st.session_state.nodes[n1][1]
                        )
                        fd.append({
                            t['member_col']: f"{n1}{n2}",
                            t['length_col']: f"{L:.2f}",
                            t['force_col']: f"{abs(f):.3f}",
                            t['type']: t['tension'] if f>=0 else t['compression']
                        })
                    st.dataframe(pd.DataFrame(fd), hide_index=True, use_container_width=True)
            with col_d:
                st.markdown(f"### {t['displacements']}")
                if res.get('displacements') is not None:
                    dd = []
                    for i, n in enumerate(res['node_names']):
                        ux = res['displacements'][2*i]*1000
                        uy = res['displacements'][2*i+1]*1000
                        dd.append({t['node_col']: n, t['ux']: f"{ux:.4f}", t['uy']: f"{uy:.4f}"})
                    st.dataframe(pd.DataFrame(dd), hide_index=True, use_container_width=True)
            
            if st.button(t['export']):
                buf = io.StringIO()
                buf.write("2D TRUSS ANALYSIS\n"+"="*40+"\n\n")
                buf.write("REACTIONS:\n")
                for n,(fx,fy) in res['reactions'].items():
                    buf.write(f"  {n}: Fx={fx:.3f}, Fy={fy:.3f}, R={np.hypot(fx,fy):.3f}\n")
                buf.write("\nMEMBER FORCES:\n")
                for (n1,n2),f in res['forces'].items():
                    buf.write(f"  {n1}{n2}: {abs(f):.3f} kN ({'T' if f>=0 else 'C'})\n")
                st.download_button("Download", buf.getvalue(), "results.txt", "text/plain")
    
    with left:
        tabs = st.tabs([t['nodes_tab'], t['members_tab'], t['supports_tab'], t['loads_tab']])
        
        # ===== NODES =====
        with tabs[0]:
            if st.session_state.nodes:
                nd = [{"Name": n, "X": x, "Y": y} for n,(x,y) in st.session_state.nodes.items()]
                df = pd.DataFrame(nd)
                st.caption(t['click_to_edit'])
                sel = st.dataframe(df, hide_index=True, use_container_width=True,
                                  selection_mode="single-row", on_select="rerun", key="ntable")
                if sel and sel.selection.rows:
                    st.session_state.sel_node = list(st.session_state.nodes.keys())[sel.selection.rows[0]]
            
            with st.form("nf", clear_on_submit=False):
                sel_n = st.session_state.sel_node
                dn, dx, dy = "", "", ""
                if sel_n and sel_n in st.session_state.nodes:
                    dn = sel_n
                    dx = str(st.session_state.nodes[sel_n][0])
                    dy = str(st.session_state.nodes[sel_n][1])
                
                c1,c2,c3 = st.columns(3)
                with c1: name = st.text_input(t['node_name'], value=dn, placeholder="A", key="ninp")
                with c2: xv = st.text_input(t['x_coord'], value=dx, placeholder="0", key="xinp")
                with c3: yv = st.text_input(t['y_coord'], value=dy, placeholder="0", key="yinp")
                
                b1,b2,b3 = st.columns(3)
                with b1: add = st.form_submit_button(t['add_node'])
                with b2: upd = st.form_submit_button(t['update_node'])
                with b3: delete = st.form_submit_button(t['delete_node'])
            
            if add and name:
                try:
                    st.session_state.nodes[name] = (float(xv or 0), float(yv or 0))
                    st.session_state.sel_node = None
                    st.rerun()
                except ValueError:
                    st.error("X and Y must be numbers")
            
            if upd and sel_n and name:
                try:
                    old = sel_n
                    coords = (float(xv or 0), float(yv or 0))
                    del st.session_state.nodes[old]
                    st.session_state.nodes[name] = coords
                    st.session_state.members = [
                        (name if m[0]==old else m[0], name if m[1]==old else m[1])
                        for m in st.session_state.members
                    ]
                    st.session_state.supports = {
                        (name if k==old else k): v for k,v in st.session_state.supports.items()
                    }
                    st.session_state.joint_loads = {
                        (name if k==old else k): v for k,v in st.session_state.joint_loads.items()
                    }
                    st.session_state.sel_node = name
                    st.rerun()
                except ValueError:
                    st.error("X and Y must be numbers")
            
            if delete and sel_n:
                del st.session_state.nodes[sel_n]
                st.session_state.members = [m for m in st.session_state.members 
                                           if m[0]!=sel_n and m[1]!=sel_n]
                st.session_state.supports.pop(sel_n, None)
                st.session_state.joint_loads.pop(sel_n, None)
                st.session_state.sel_node = None
                st.session_state.highlight_del = None
                st.rerun()
        
        # ===== MEMBERS =====
        with tabs[1]:
            if st.session_state.members:
                md = []
                for n1,n2 in st.session_state.members:
                    x1,y1 = st.session_state.nodes[n1]
                    x2,y2 = st.session_state.nodes[n2]
                    L = np.hypot(x2-x1, y2-y1)
                    md.append({"Name": f"{n1}{n2}", "Start": n1, "End": n2, t['length']: f"{L:.2f}"})
                df = pd.DataFrame(md)
                st.caption(t['click_to_edit'])
                sel = st.dataframe(df, hide_index=True, use_container_width=True,
                                  selection_mode="single-row", on_select="rerun", key="mtable")
                if sel and sel.selection.rows:
                    st.session_state.sel_member = st.session_state.members[sel.selection.rows[0]]
            
            with st.form("mf", clear_on_submit=False):
                sel_m = st.session_state.sel_member
                ds, de = "", ""
                nnames = list(st.session_state.nodes.keys())
                if sel_m:
                    ds, de = sel_m[0], sel_m[1]
                
                c1,c2 = st.columns(2)
                with c1:
                    si = nnames.index(ds) if ds in nnames else 0
                    sn = st.selectbox(t['start_node'], nnames if nnames else ["-"], 
                                     index=min(si, len(nnames)-1) if nnames else 0, key="sinp")
                with c2:
                    ei = nnames.index(de) if de in nnames else (1 if len(nnames)>1 else 0)
                    en = st.selectbox(t['end_node'], nnames if nnames else ["-"],
                                     index=min(ei, len(nnames)-1) if nnames else 0, key="einp")
                
                b1,b2,b3 = st.columns(3)
                with b1: add_m = st.form_submit_button(t['add_member'])
                with b2: upd_m = st.form_submit_button(t['update_member'])
                with b3: delete_m = st.form_submit_button(t['delete_member'])
            
            if add_m and sn != en and sn in nnames and en in nnames:
                if (sn,en) not in st.session_state.members and (en,sn) not in st.session_state.members:
                    st.session_state.members.append((sn, en))
                    st.session_state.sel_member = None
                    st.rerun()
            
            if upd_m and sel_m and sn != en:
                st.session_state.members = [
                    (sn, en) if m == sel_m else m for m in st.session_state.members
                ]
                st.session_state.sel_member = (sn, en)
                st.rerun()
            
            if delete_m and sel_m:
                st.session_state.members.remove(sel_m)
                st.session_state.member_loads = [
                    l for l in st.session_state.member_loads 
                    if not ((l[1]==(sel_m[0],sel_m[1])) or (l[1]==f"{sel_m[0]}{sel_m[1]}") or (l[1]==sel_m[0]+sel_m[1]))
                ]
                st.session_state.sel_member = None
                st.session_state.highlight_del = None
                st.rerun()
        
        # ===== SUPPORTS =====
        with tabs[2]:
            if st.session_state.supports:
                sd = [{"Node": n, "Type": ty} for n,ty in st.session_state.supports.items()]
                df = pd.DataFrame(sd)
                st.caption(t['click_to_edit'])
                sel = st.dataframe(df, hide_index=True, use_container_width=True,
                                  selection_mode="single-row", on_select="rerun", key="stable")
                if sel and sel.selection.rows:
                    st.session_state.sel_support = list(st.session_state.supports.keys())[sel.selection.rows[0]]
            
            with st.form("sf", clear_on_submit=False):
                sel_sp = st.session_state.sel_support
                nnames = list(st.session_state.nodes.keys())
                ds = sel_sp if sel_sp and sel_sp in nnames else (nnames[0] if nnames else "")
                dt = st.session_state.supports.get(sel_sp, t['support_types'][0]) if sel_sp else t['support_types'][0]
                
                c1,c2 = st.columns(2)
                with c1:
                    si = nnames.index(ds) if ds in nnames else 0
                    spn = st.selectbox(t['support_node'], nnames if nnames else ["-"],
                                      index=min(si, len(nnames)-1) if nnames else 0, key="spinp")
                with c2:
                    ti = t['support_types'].index(dt) if dt in t['support_types'] else 0
                    spt = st.selectbox(t['support_type'], t['support_types'], index=ti, key="stinp")
                
                b1,b2 = st.columns(2)
                with b1: add_s = st.form_submit_button(t['add_support'])
                with b2: delete_s = st.form_submit_button(t['delete_support'])
            
            if add_s and spn in nnames:
                st.session_state.supports[spn] = spt.lower().replace(' ','_')
                st.session_state.sel_support = None
                st.rerun()
            
            if delete_s and sel_sp:
                st.session_state.supports.pop(sel_sp, None)
                st.session_state.sel_support = None
                st.rerun()
        
        # ===== LOADS =====
        with tabs[3]:
            all_loads = []
            for node, (mag, ang) in st.session_state.joint_loads.items():
                all_loads.append({"Type": "Node", "Location": node, "kN": mag, "Angle": ang})
            for _, member, pos, mag, ang in st.session_state.member_loads:
                mname = f"{member[0]}{member[1]}" if isinstance(member, tuple) else member
                all_loads.append({"Type": "Member", "Location": f"{mname} @{pos:.2f}", 
                                 "kN": mag, "Angle": ang})
            
            if all_loads:
                st.dataframe(pd.DataFrame(all_loads), hide_index=True, use_container_width=True)
            
            with st.form("lf", clear_on_submit=False):
                ltype = st.selectbox(t['load_type'], t['load_types'], key="ltinp")
                
                c1,c2,c3,c4,c5 = st.columns(5)
                with c1:
                    lname = st.text_input(t['load_name'], placeholder="F1", key="lninp")
                with c2:
                    if ltype == t['load_types'][0]:
                        nnames = list(st.session_state.nodes.keys())
                        loc = st.selectbox(t['load_location'], nnames if nnames else ["-"], key="llinp")
                    else:
                        mnames = [f"{m[0]}{m[1]}" for m in st.session_state.members]
                        loc = st.selectbox(t['load_member'], mnames if mnames else ["-"], key="llinp")
                with c3:
                    if ltype == t['load_types'][1]:
                        pos = st.slider(t['load_position'], 0.0, 1.0, 0.5, 0.01, key="lpinp")
                    else:
                        pos = 0.0
                        st.text("")
                with c4:
                    mag = st.text_input(t['load_magnitude'], placeholder="10", key="lminp")
                with c5:
                    ang = st.text_input(t['load_angle'], placeholder="270", key="lainp")
                
                b1,b2 = st.columns(2)
                with b1: add_l = st.form_submit_button(t['add_load'])
                with b2: delete_l = st.form_submit_button(t['delete_load'])
            
            if add_l:
                try:
                    mf = float(mag) if mag else 0
                    af = float(ang) if ang else 0
                    if ltype == t['load_types'][0] and loc in st.session_state.nodes:
                        st.session_state.joint_loads[loc] = (mf, af)
                        st.rerun()
                    elif ltype == t['load_types'][1]:
                        found = None
                        for m in st.session_state.members:
                            if f"{m[0]}{m[1]}" == loc or m[0]+m[1] == loc:
                                found = m; break
                        if found:
                            st.session_state.member_loads.append((lname, found, pos, mf, af))
                            st.rerun()
                except ValueError:
                    st.error("Force and angle must be numbers")
            
            if delete_l:
                st.session_state.joint_loads = {}
                st.session_state.member_loads = []
                st.rerun()
    
    # Analyze / Reset
    st.markdown("---")
    ca, cr = st.columns([3, 1])
    with ca:
        if st.button(t['analyze'], use_container_width=True, type="primary"):
            if len(st.session_state.nodes) >= 2 and len(st.session_state.members) >= 1:
                with st.spinner("Analyzing..."):
                    try:
                        eng = Engine(
                            st.session_state.nodes,
                            st.session_state.members,
                            st.session_state.supports,
                            st.session_state.joint_loads,
                            st.session_state.member_loads
                        )
                        if eng.U is not None:
                            st.session_state.results = {
                                'reactions': eng.reactions,
                                'forces': eng.forces,
                                'displacements': eng.U,
                                'node_names': eng.node_names
                            }
                            st.rerun()
                        else:
                            st.error(t['error_analysis'])
                    except Exception as e:
                        st.error(f"{t['error_analysis']}: {e}")
            else:
                st.warning(t['need_min'])
    
    with cr:
        if st.button(t['reset'], use_container_width=True):
            for k in ['nodes','members','supports','joint_loads','member_loads',
                     'results','sel_node','sel_member','sel_support','sel_load','highlight_del']:
                st.session_state[k] = {} if k in ['nodes','supports','joint_loads'] else [] if k in ['members','member_loads'] else None
            st.rerun()

if __name__ == "__main__":
    main()