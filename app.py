"""
2D Truss Analysis System - Matrix Stiffness Method
Professional Engineering Tool with Streamlit Interface
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyArrowPatch
import io

# ============================================================================
# LANGUAGE SYSTEM
# ============================================================================

LANGUAGES = {
    "English": {
        "title": "🔧 2D Truss Analysis System",
        "subtitle": "Matrix Stiffness Method Solver",
        "node_tab": "📌 Nodes",
        "member_tab": "🔗 Members",
        "support_tab": "🏗️ Supports",
        "load_tab": "⬇️ Loads",
        "results_tab": "📊 Results",
        "visualization_tab": "📈 Visualization",
        "language_label": "🌐 Language",
        "analyze_btn": "🚀 Analyze Structure",
        "reset_btn": "🔄 Reset All",
        "node_id": "Node ID",
        "x_coord": "X Coordinate (m)",
        "y_coord": "Y Coordinate (m)",
        "add_node": "Add Node",
        "member_id": "Member ID",
        "start_node": "Start Node",
        "end_node": "End Node",
        "add_member": "Add Member",
        "support_node": "Node ID",
        "support_type": "Support Type",
        "support_types": ["Pinned (Fixed X, Y)", "Roller X (Free X)", "Roller Y (Free Y)"],
        "add_support": "Add Support",
        "load_node": "Node ID",
        "load_magnitude": "Magnitude (kN)",
        "load_angle": "Angle (degrees)",
        "add_load": "Add Load",
        "reactions_title": "🔴 Support Reactions",
        "member_forces_title": "🔵 Member Forces",
        "displacements_title": "📐 Nodal Displacements",
        "fx": "Fx (kN)",
        "fy": "Fy (kN)",
        "resultant": "Resultant (kN)",
        "angle": "Angle (deg)",
        "force": "Force (kN)",
        "type": "Type",
        "tension": "TENSION",
        "compression": "COMPRESSION",
        "ux": "Ux (mm)",
        "uy": "Uy (mm)",
        "no_results": "No results yet. Click 'Analyze Structure' to compute.",
        "warning_title": "⚠️ Warning",
        "warning_message": "Please add at least 2 nodes, 1 member, and appropriate supports before analysis.",
        "error_geometry": "Error: Check node coordinates and member connectivity.",
        "error_singular": "Error: Structure is unstable or has insufficient supports.",
        "export_btn": "📥 Export Results",
        "legend_title": "📌 Color Legend",
        "legend_tension": "🔵 Blue = Tension",
        "legend_compression": "🔴 Red = Compression",
        "node_table_title": "Node Coordinates",
        "member_table_title": "Member Connectivity",
        "support_table_title": "Support Conditions",
        "load_table_title": "Applied Loads",
    },
    "Persian": {
        "title": "🔧 سیستم تحلیل خرپا دو بعدی",
        "subtitle": "حل‌کننده به روش سختی ماتریسی",
        "node_tab": "📌 گره‌ها",
        "member_tab": "🔗 اعضا",
        "support_tab": "🏗️ تکیه‌گاه‌ها",
        "load_tab": "⬇️ بارها",
        "results_tab": "📊 نتایج",
        "visualization_tab": "📈 نمودار",
        "language_label": "🌐 زبان",
        "analyze_btn": "🚀 تحلیل سازه",
        "reset_btn": "🔄 بازنشانی",
        "node_id": "شماره گره",
        "x_coord": "مختصات X (متر)",
        "y_coord": "مختصات Y (متر)",
        "add_node": "افزودن گره",
        "member_id": "شماره عضو",
        "start_node": "گره شروع",
        "end_node": "گره پایان",
        "add_member": "افزودن عضو",
        "support_node": "شماره گره",
        "support_type": "نوع تکیه‌گاه",
        "support_types": ["گیردار (ثابت X, Y)", "غلتک X (آزاد X)", "غلتک Y (آزاد Y)"],
        "add_support": "افزودن تکیه‌گاه",
        "load_node": "شماره گره",
        "load_magnitude": "بزرگی (کیلونیوتن)",
        "load_angle": "زاویه (درجه)",
        "add_load": "افزودن بار",
        "reactions_title": "🔴 عکس‌العمل‌های تکیه‌گاهی",
        "member_forces_title": "🔵 نیروهای اعضا",
        "displacements_title": "📐 جابجایی‌های گرهی",
        "fx": "Fx (kN)",
        "fy": "Fy (kN)",
        "resultant": "برآیند (kN)",
        "angle": "زاویه (درجه)",
        "force": "نیرو (kN)",
        "type": "نوع",
        "tension": "کششی",
        "compression": "فشاری",
        "ux": "Ux (mm)",
        "uy": "Uy (mm)",
        "no_results": "هنوز نتیجه‌ای موجود نیست. دکمه 'تحلیل سازه' را بزنید.",
        "warning_title": "⚠️ هشدار",
        "warning_message": "لطفاً حداقل ۲ گره، ۱ عضو و تکیه‌گاه مناسب قبل از تحلیل اضافه کنید.",
        "error_geometry": "خطا: مختصات گره‌ها و اتصالات اعضا را بررسی کنید.",
        "error_singular": "خطا: سازه ناپایدار است یا تکیه‌گاه کافی ندارد.",
        "export_btn": "📥 خروجی نتایج",
        "legend_title": "📌 راهنمای رنگ‌ها",
        "legend_tension": "🔵 آبی = کشش",
        "legend_compression": "🔴 قرمز = فشار",
        "node_table_title": "مختصات گره‌ها",
        "member_table_title": "اتصالات اعضا",
        "support_table_title": "شرایط تکیه‌گاهی",
        "load_table_title": "بارهای اعمالی",
    }
}

# ============================================================================
# CORE ENGINEERING SOLVER
# ============================================================================

class TrussAnalyzer:
    """2D Truss Analysis using Matrix Stiffness Method"""
    
    def __init__(self, nodes, members, supports, loads, E=200e6):
        """
        Initialize truss analyzer
        
        Parameters:
        - nodes: dict {id: (x, y)}
        - members: list of tuples (id, node_i, node_j)
        - supports: dict {node_id: ('pinned'|'roller_x'|'roller_y')}
        - loads: dict {node_id: (magnitude, angle_deg)}
        - E: Elastic modulus (kN/m²), default steel = 200e6 kN/m²
        """
        self.nodes = nodes
        self.members = members
        self.supports = supports
        self.loads = loads
        self.E = E
        self.n_nodes = len(nodes)
        self.n_members = len(members)
        self.n_dofs = 2 * self.n_nodes  # 2 DOFs per node (x, y)
        
        # Initialize arrays
        self.K_global = np.zeros((self.n_dofs, self.n_dofs))
        self.F_global = np.zeros(self.n_dofs)
        self.U_global = np.zeros(self.n_dofs)
        self.member_forces = {}
        self.reactions = {}
        
        # Assemble and solve
        self._assemble_stiffness()
        self._apply_loads()
        self._apply_boundary_conditions()
        self._solve()
        
    def _get_dof_indices(self, node_id):
        """Get global DOF indices for a node"""
        base = 2 * (node_id - 1)
        return base, base + 1  # (x_dof, y_dof)
    
    def _calculate_member_length_angle(self, node_i, node_j):
        """Calculate length and angle of a member"""
        xi, yi = self.nodes[node_i]
        xj, yj = self.nodes[node_j]
        dx = xj - xi
        dy = yj - yi
        L = np.sqrt(dx**2 + dy**2)
        cos = dx / L if L > 0 else 0
        sin = dy / L if L > 0 else 0
        return L, cos, sin
    
    def _assemble_stiffness(self):
        """Assemble global stiffness matrix"""
        A = 0.01  # Cross-sectional area (m²) - simplified for truss analysis
        
        for member_id, node_i, node_j in self.members:
            L, c, s = self._calculate_member_length_angle(node_i, node_j)
            
            if L == 0:
                continue
                
            # Local stiffness matrix in global coordinates
            k = (self.E * A / L) * np.array([
                [c*c, c*s, -c*c, -c*s],
                [c*s, s*s, -c*s, -s*s],
                [-c*c, -c*s, c*c, c*s],
                [-c*s, -s*s, c*s, s*s]
            ])
            
            # Get DOF indices
            dof_i = self._get_dof_indices(node_i)
            dof_j = self._get_dof_indices(node_j)
            dof_indices = [dof_i[0], dof_i[1], dof_j[0], dof_j[1]]
            
            # Assemble into global stiffness matrix
            for ii, global_i in enumerate(dof_indices):
                for jj, global_j in enumerate(dof_indices):
                    self.K_global[global_i, global_j] += k[ii, jj]
    
    def _apply_loads(self):
        """Apply external loads to force vector"""
        for node_id, (magnitude, angle_deg) in self.loads.items():
            angle_rad = np.radians(angle_deg)
            fx = magnitude * np.cos(angle_rad)
            fy = magnitude * np.sin(angle_rad)
            
            dof_x, dof_y = self._get_dof_indices(node_id)
            self.F_global[dof_x] += fx
            self.F_global[dof_y] += fy
    
    def _apply_boundary_conditions(self):
        """Apply support conditions using penalty method"""
        penalty = 1e10 * np.max(np.abs(self.K_global)) if np.max(np.abs(self.K_global)) > 0 else 1e10
        
        for node_id, support_type in self.supports.items():
            dof_x, dof_y = self._get_dof_indices(node_id)
            
            if support_type == 'pinned':
                # Fix both X and Y
                self.K_global[dof_x, dof_x] += penalty
                self.K_global[dof_y, dof_y] += penalty
            elif support_type == 'roller_x':
                # Fix Y only (free in X)
                self.K_global[dof_y, dof_y] += penalty
            elif support_type == 'roller_y':
                # Fix X only (free in Y)
                self.K_global[dof_x, dof_x] += penalty
    
    def _solve(self):
        """Solve system and compute results"""
        try:
            # Check if matrix is invertible
            if np.linalg.matrix_rank(self.K_global) < self.n_dofs - len(self.supports):
                raise np.linalg.LinAlgError("Singular matrix")
            
            # Solve for displacements
            self.U_global = np.linalg.solve(self.K_global, self.F_global)
            
            # Calculate member forces
            for member_id, node_i, node_j in self.members:
                L, c, s = self._calculate_member_length_angle(node_i, node_j)
                
                if L == 0:
                    self.member_forces[member_id] = 0
                    continue
                
                # Get displacements
                dof_i = self._get_dof_indices(node_i)
                dof_j = self._get_dof_indices(node_j)
                
                u_i = self.U_global[dof_i[0]]
                v_i = self.U_global[dof_i[1]]
                u_j = self.U_global[dof_j[0]]
                v_j = self.U_global[dof_j[1]]
                
                # Calculate axial force
                A = 0.01
                force = (self.E * A / L) * (c*(u_j - u_i) + s*(v_j - v_i))
                self.member_forces[member_id] = force
            
            # Calculate reactions
            for node_id, support_type in self.supports.items():
                dof_x, dof_y = self._get_dof_indices(node_id)
                
                # Reaction = K * U - F at support DOFs
                reaction_x = np.dot(self.K_global[dof_x, :], self.U_global) - self.F_global[dof_x]
                reaction_y = np.dot(self.K_global[dof_y, :], self.U_global) - self.F_global[dof_y]
                
                self.reactions[node_id] = (reaction_x, reaction_y)
                
        except np.linalg.LinAlgError:
            st.error("Structure is unstable or has insufficient supports. Check your boundary conditions.")
            self.U_global = None
            self.member_forces = {}
            self.reactions = {}

# ============================================================================
# VISUALIZATION MODULE
# ============================================================================

def plot_truss(nodes, members, supports, loads, member_forces=None, reactions=None, lang_dict=None):
    """Create professional truss visualization"""
    if lang_dict is None:
        lang_dict = LANGUAGES["English"]
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('X (m)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Y (m)', fontsize=12, fontweight='bold')
    ax.set_title('2D Truss Structure Analysis', fontsize=14, fontweight='bold')
    
    # Find bounds for scaling
    all_x = [coord[0] for coord in nodes.values()]
    all_y = [coord[1] for coord in nodes.values()]
    
    x_min, x_max = min(all_x), max(all_x)
    y_min, y_max = min(all_y), max(all_y)
    
    margin = max(x_max - x_min, y_max - y_min) * 0.2 + 1
    ax.set_xlim(x_min - margin, x_max + margin)
    ax.set_ylim(y_min - margin, y_max + margin)
    
    # Draw members
    for member_id, node_i, node_j in members:
        xi, yi = nodes[node_i]
        xj, yj = nodes[node_j]
        
        if member_forces and member_id in member_forces:
            force = member_forces[member_id]
            color = 'blue' if force >= 0 else 'red'
            linewidth = 2.5
        else:
            color = 'gray'
            linewidth = 2
        
        ax.plot([xi, xj], [yi, yj], color=color, linewidth=linewidth, zorder=2)
        
        # Label member
        mid_x, mid_y = (xi + xj) / 2, (yi + yj) / 2
        if member_forces and member_id in member_forces:
            force_val = abs(member_forces[member_id])
            force_type = 'T' if member_forces[member_id] >= 0 else 'C'
            ax.annotate(f'M{member_id}: {force_val:.1f} kN ({force_type})', 
                       (mid_x, mid_y), fontsize=8, ha='center',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # Draw nodes
    for node_id, (x, y) in nodes.items():
        ax.plot(x, y, 'ko', markersize=10, zorder=3)
        ax.annotate(f' {node_id}', (x, y), fontsize=10, fontweight='bold', 
                   xytext=(5, 5), textcoords='offset points')
    
    # Draw supports
    for node_id, support_type in supports.items():
        x, y = nodes[node_id]
        if support_type == 'pinned':
            # Triangle support (pinned)
            triangle = plt.Polygon([[x-0.3, y-0.3], [x+0.3, y-0.3], [x, y]], 
                                  facecolor='gray', edgecolor='black', zorder=3)
            ax.add_patch(triangle)
            # Hash marks
            for i in range(3):
                ax.plot([x-0.3+i*0.3, x-0.2+i*0.3], [y-0.3, y-0.5], 'k-', linewidth=1.5)
        elif support_type == 'roller_x':
            # Circle + horizontal lines (roller in X)
            circle = plt.Circle((x, y-0.2), 0.15, facecolor='white', edgecolor='black', zorder=3)
            ax.add_patch(circle)
            ax.plot([x-0.3, x+0.3], [y-0.5, y-0.5], 'k-', linewidth=1.5)
        elif support_type == 'roller_y':
            # Circle + vertical lines (roller in Y)
            circle = plt.Circle((x-0.2, y), 0.15, facecolor='white', edgecolor='black', zorder=3)
            ax.add_patch(circle)
            ax.plot([x-0.5, x-0.5], [y-0.3, y+0.3], 'k-', linewidth=1.5)
    
    # Draw loads
    max_force = max([magnitude for magnitude, _ in loads.values()]) if loads else 1
    scale_factor = (x_max - x_min) / max_force * 0.15 if max_force > 0 else 0.5
    
    for node_id, (magnitude, angle_deg) in loads.items():
        x, y = nodes[node_id]
        angle_rad = np.radians(angle_deg)
        dx = -magnitude * np.cos(angle_rad) * scale_factor
        dy = -magnitude * np.sin(angle_rad) * scale_factor
        
        arrow = FancyArrowPatch(
            (x + dx, y + dy), (x, y),
            arrowstyle='->', mutation_scale=20, 
            color='green', linewidth=2, zorder=4
        )
        ax.add_patch(arrow)
        ax.annotate(f'{magnitude:.1f} kN', (x + dx, y + dy), 
                   fontsize=8, color='green', fontweight='bold',
                   ha='center', va='bottom')
    
    # Draw reactions
    if reactions:
        for node_id, (rx, ry) in reactions.items():
            x, y = nodes[node_id]
            if abs(rx) > 0.01 or abs(ry) > 0.01:
                scale = scale_factor
                dx, dy = rx * scale, ry * scale
                arrow = FancyArrowPatch(
                    (x - dx, y - dy), (x, y),
                    arrowstyle='->', mutation_scale=20,
                    color='orange', linewidth=2, zorder=4
                )
                ax.add_patch(arrow)
                resultant = np.sqrt(rx**2 + ry**2)
                ax.annotate(f'R={resultant:.1f} kN', (x - dx, y - dy),
                           fontsize=8, color='orange', fontweight='bold')
    
    # Add color legend
    legend_text = f"{lang_dict['legend_tension']} | {lang_dict['legend_compression']}"
    ax.text(0.02, 0.98, legend_text, transform=ax.transAxes,
           fontsize=9, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    return fig

# ============================================================================
# STREAMLIT UI - MAIN APPLICATION
# ============================================================================

def main():
    # Page configuration
    st.set_page_config(
        page_title="2D Truss Analysis",
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for modern engineering look
    st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
            padding: 1.5rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        .stButton>button {
            background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            font-weight: bold;
            padding: 0.5rem 2rem;
            border-radius: 5px;
            border: none;
            transition: transform 0.2s;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            background: linear-gradient(90deg, #2a5298 0%, #1e3c72 100%);
        }
        .card {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Language selection
    if 'language' not in st.session_state:
        st.session_state.language = "English"
    
    col_lang, col_title = st.columns([1, 4])
    with col_lang:
        st.session_state.language = st.selectbox(
            "🌐 Language / زبان",
            ["English", "Persian"],
            key="lang_selector"
        )
    
    lang = LANGUAGES[st.session_state.language]
    
    # Main title
    st.markdown(f"""
        <div class="main-header">
            <h1>{lang['title']}</h1>
            <p>{lang['subtitle']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for data
    if 'nodes' not in st.session_state:
        st.session_state.nodes = {}
    if 'members' not in st.session_state:
        st.session_state.members = []
    if 'supports' not in st.session_state:
        st.session_state.supports = {}
    if 'loads' not in st.session_state:
        st.session_state.loads = {}
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'member_counter' not in st.session_state:
        st.session_state.member_counter = 1
    
    # Create tabs for input
    tab1, tab2, tab3, tab4 = st.tabs([
        lang['node_tab'], 
        lang['member_tab'], 
        lang['support_tab'], 
        lang['load_tab']
    ])
    
    # ===== NODES TAB =====
    with tab1:
        st.markdown(f"### {lang['node_table_title']}")
        
        # Display current nodes
        if st.session_state.nodes:
            node_df = pd.DataFrame([
                {"Node ID": nid, "X (m)": coord[0], "Y (m)": coord[1]}
                for nid, coord in st.session_state.nodes.items()
            ])
            st.dataframe(node_df, use_container_width=True)
        else:
            st.info("No nodes added yet. Add nodes using the form below.")
        
        # Add node form
        with st.form("add_node_form", clear_on_submit=True):
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                node_id = st.number_input(lang['node_id'], min_value=1, step=1, key="node_id")
            with col2:
                x_coord = st.number_input(lang['x_coord'], value=0.0, step=0.1, key="x_coord")
            with col3:
                y_coord = st.number_input(lang['y_coord'], value=0.0, step=0.1, key="y_coord")
            
            if st.form_submit_button(lang['add_node']):
                if node_id in st.session_state.nodes:
                    st.warning(f"Node {node_id} already exists! Use a different ID.")
                else:
                    st.session_state.nodes[node_id] = (x_coord, y_coord)
                    st.success(f"Node {node_id} added successfully!")
                    st.rerun()
    
    # ===== MEMBERS TAB =====
    with tab2:
        st.markdown(f"### {lang['member_table_title']}")
        
        # Display current members
        if st.session_state.members:
            member_df = pd.DataFrame([
                {"Member ID": mid, "Start Node": ni, "End Node": nj}
                for mid, ni, nj in st.session_state.members
            ])
            st.dataframe(member_df, use_container_width=True)
        else:
            st.info("No members added yet.")
        
        # Add member form
        with st.form("add_member_form", clear_on_submit=True):
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                member_id = st.number_input(
                    lang['member_id'], 
                    min_value=1, 
                    value=st.session_state.member_counter,
                    step=1, 
                    key="member_id"
                )
            with col2:
                start_node = st.selectbox(
                    lang['start_node'],
                    options=list(st.session_state.nodes.keys()) if st.session_state.nodes else [0],
                    key="start_node"
                )
            with col3:
                end_node = st.selectbox(
                    lang['end_node'],
                    options=list(st.session_state.nodes.keys()) if st.session_state.nodes else [0],
                    key="end_node"
                )
            
            if st.form_submit_button(lang['add_member']):
                if not st.session_state.nodes:
                    st.error("Please add nodes first!")
                elif start_node == end_node:
                    st.error("Start and end nodes must be different!")
                elif any(m[0] == member_id for m in st.session_state.members):
                    st.warning(f"Member {member_id} already exists!")
                else:
                    st.session_state.members.append((member_id, start_node, end_node))
                    st.session_state.member_counter = max(member_id + 1, st.session_state.member_counter)
                    st.success(f"Member {member_id} added!")
                    st.rerun()
    
    # ===== SUPPORTS TAB =====
    with tab3:
        st.markdown(f"### {lang['support_table_title']}")
        
        # Display current supports
        if st.session_state.supports:
            support_df = pd.DataFrame([
                {"Node ID": nid, "Support Type": stype}
                for nid, stype in st.session_state.supports.items()
            ])
            st.dataframe(support_df, use_container_width=True)
        else:
            st.info("No supports defined yet.")
        
        # Add support form
        with st.form("add_support_form", clear_on_submit=True):
            col1, col2 = st.columns([1, 1])
            with col1:
                support_node = st.selectbox(
                    lang['support_node'],
                    options=list(st.session_state.nodes.keys()) if st.session_state.nodes else [0],
                    key="support_node"
                )
            with col2:
                support_type = st.selectbox(
                    lang['support_type'],
                    options=lang['support_types'],
                    key="support_type"
                )
            
            if st.form_submit_button(lang['add_support']):
                if not st.session_state.nodes:
                    st.error("Please add nodes first!")
                else:
                    # Map selection to internal code
                    type_map = {
                        lang['support_types'][0]: 'pinned',
                        lang['support_types'][1]: 'roller_x',
                        lang['support_types'][2]: 'roller_y'
                    }
                    st.session_state.supports[support_node] = type_map[support_type]
                    st.success(f"Support added at node {support_node}!")
                    st.rerun()
    
    # ===== LOADS TAB =====
    with tab4:
        st.markdown(f"### {lang['load_table_title']}")
        
        # Display current loads
        if st.session_state.loads:
            load_df = pd.DataFrame([
                {"Node ID": nid, "Magnitude (kN)": mag, "Angle (deg)": ang}
                for nid, (mag, ang) in st.session_state.loads.items()
            ])
            st.dataframe(load_df, use_container_width=True)
        else:
            st.info("No loads applied yet.")
        
        # Add load form
        with st.form("add_load_form", clear_on_submit=True):
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                load_node = st.selectbox(
                    lang['load_node'],
                    options=list(st.session_state.nodes.keys()) if st.session_state.nodes else [0],
                    key="load_node"
                )
            with col2:
                magnitude = st.number_input(
                    lang['load_magnitude'],
                    value=10.0,
                    step=1.0,
                    key="magnitude"
                )
            with col3:
                angle = st.number_input(
                    lang['load_angle'],
                    value=270.0,
                    step=1.0,
                    key="angle"
                )
            
            if st.form_submit_button(lang['add_load']):
                if not st.session_state.nodes:
                    st.error("Please add nodes first!")
                else:
                    st.session_state.loads[load_node] = (magnitude, angle)
                    st.success(f"Load applied at node {load_node}!")
                    st.rerun()
    
    # Action buttons
    st.markdown("---")
    col_analyze, col_reset = st.columns([1, 1])
    
    with col_analyze:
        analyze_clicked = st.button(lang['analyze_btn'], use_container_width=True)
    
    with col_reset:
        if st.button(lang['reset_btn'], use_container_width=True):
            st.session_state.nodes = {}
            st.session_state.members = []
            st.session_state.supports = {}
            st.session_state.loads = {}
            st.session_state.results = None
            st.session_state.member_counter = 1
            st.rerun()
    
    # Perform analysis
    if analyze_clicked:
        if len(st.session_state.nodes) < 2 or len(st.session_state.members) < 1:
            st.error(lang['warning_message'])
        else:
            with st.spinner("Analyzing structure..."):
                try:
                    analyzer = TrussAnalyzer(
                        nodes=st.session_state.nodes,
                        members=st.session_state.members,
                        supports=st.session_state.supports,
                        loads=st.session_state.loads
                    )
                    
                    if analyzer.U_global is not None:
                        st.session_state.results = {
                            'analyzer': analyzer,
                            'displacements': analyzer.U_global,
                            'member_forces': analyzer.member_forces,
                            'reactions': analyzer.reactions
                        }
                        st.success("✅ Analysis completed successfully!")
                    else:
                        st.error(lang['error_singular'])
                except Exception as e:
                    st.error(f"{lang['error_geometry']}: {str(e)}")
    
    # ===== RESULTS SECTION =====
    if st.session_state.results:
        st.markdown("---")
        st.markdown("## 📊 Analysis Results")
        
        results = st.session_state.results
        analyzer = results['analyzer']
        
        # Create tabs for results
        res_tab1, res_tab2, res_tab3, res_tab4 = st.tabs([
            lang['reactions_title'],
            lang['member_forces_title'],
            lang['displacements_title'],
            lang['visualization_tab']
        ])
        
        # Reactions
        with res_tab1:
            if results['reactions']:
                reaction_data = []
                for node_id, (fx, fy) in results['reactions'].items():
                    resultant = np.sqrt(fx**2 + fy**2)
                    angle = np.degrees(np.arctan2(fy, fx)) if resultant > 0.001 else 0
                    reaction_data.append({
                        lang['node_id']: node_id,
                        lang['fx']: round(fx, 3),
                        lang['fy']: round(fy, 3),
                        lang['resultant']: round(resultant, 3),
                        lang['angle']: round(angle, 2)
                    })
                
                reaction_df = pd.DataFrame(reaction_data)
                st.dataframe(reaction_df, use_container_width=True)
            else:
                st.info("No reactions computed.")
        
        # Member Forces
        with res_tab2:
            if results['member_forces']:
                force_data = []
                for member_id, force in results['member_forces'].items():
                    force_type = lang['tension'] if force >= 0 else lang['compression']
                    force_data.append({
                        lang['member_id']: member_id,
                        lang['force']: round(abs(force), 3),
                        lang['type']: force_type
                    })
                
                force_df = pd.DataFrame(force_data)
                st.dataframe(force_df, use_container_width=True)
            else:
                st.info("No member forces computed.")
        
        # Displacements
        with res_tab3:
            displacements = results['displacements']
            if displacements is not None:
                disp_data = []
                for node_id in st.session_state.nodes.keys():
                    dof_x, dof_y = 2*(node_id-1), 2*(node_id-1)+1
                    disp_data.append({
                        lang['node_id']: node_id,
                        lang['ux']: round(displacements[dof_x] * 1000, 4),  # Convert to mm
                        lang['uy']: round(displacements[dof_y] * 1000, 4)   # Convert to mm
                    })
                
                disp_df = pd.DataFrame(disp_data)
                st.dataframe(disp_df, use_container_width=True)
            else:
                st.info("No displacements computed.")
        
        # Visualization
        with res_tab4:
            fig = plot_truss(
                nodes=st.session_state.nodes,
                members=st.session_state.members,
                supports=st.session_state.supports,
                loads=st.session_state.loads,
                member_forces=results['member_forces'],
                reactions=results['reactions'],
                lang_dict=lang
            )
            st.pyplot(fig)
        
        # Export functionality
        st.markdown("---")
        col_exp1, col_exp2 = st.columns([1, 3])
        with col_exp1:
            if st.button(lang['export_btn'], use_container_width=True):
                # Create export string
                buffer = io.StringIO()
                buffer.write("2D TRUSS ANALYSIS RESULTS\n")
                buffer.write("="*50 + "\n\n")
                
                buffer.write("SUPPORT REACTIONS\n")
                buffer.write("-"*30 + "\n")
                for node_id, (fx, fy) in results['reactions'].items():
                    R = np.sqrt(fx**2 + fy**2)
                    angle = np.degrees(np.arctan2(fy, fx))
                    buffer.write(f"Node {node_id}: Fx={fx:.3f} kN, Fy={fy:.3f} kN, R={R:.3f} kN, Angle={angle:.2f}°\n")
                
                buffer.write("\nMEMBER FORCES\n")
                buffer.write("-"*30 + "\n")
                for member_id, force in results['member_forces'].items():
                    ftype = "TENSION" if force >= 0 else "COMPRESSION"
                    buffer.write(f"Member {member_id}: {abs(force):.3f} kN ({ftype})\n")
                
                buffer.write("\nNODAL DISPLACEMENTS\n")
                buffer.write("-"*30 + "\n")
                for node_id in st.session_state.nodes.keys():
                    dof_x, dof_y = 2*(node_id-1), 2*(node_id-1)+1
                    ux = results['displacements'][dof_x] * 1000
                    uy = results['displacements'][dof_y] * 1000
                    buffer.write(f"Node {node_id}: Ux={ux:.4f} mm, Uy={uy:.4f} mm\n")
                
                st.download_button(
                    label="📥 Download Results",
                    data=buffer.getvalue(),
                    file_name="truss_analysis_results.txt",
                    mime="text/plain"
                )
    
    elif not analyze_clicked:
        st.info(lang['no_results'])

if __name__ == "__main__":
    main()