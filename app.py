"""
Main Streamlit application for 2D Truss Analysis System.
Professional engineering web interface with modern SaaS design.
"""

import streamlit as st
import pandas as pd
import math
from typing import List, Dict
import io

# Import local modules
from solver import Node, Member, Support, Load, TrussSolver
from plotting import TrussPlotter
from localization import Localization
from pdf_export import PDFExporter
from styles import get_css

# Page configuration
st.set_page_config(
    page_title="2D Truss Analysis System",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def init_session_state():
    """Initialize all session state variables."""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'system'
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    if 'nodes' not in st.session_state:
        st.session_state.nodes = []
    if 'members' not in st.session_state:
        st.session_state.members = []
    if 'supports' not in st.session_state:
        st.session_state.supports = []
    if 'loads' not in st.session_state:
        st.session_state.loads = []
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'unit' not in st.session_state:
        st.session_state.unit = 'N'
    if 'show_delete_confirm' not in st.session_state:
        st.session_state.show_delete_confirm = None
    if 'show_reset_confirm' not in st.session_state:
        st.session_state.show_reset_confirm = False
    if 'errors' not in st.session_state:
        st.session_state.errors = []

init_session_state()

# Initialize localization
loc = Localization(st.session_state.language)

# Apply theme
theme_to_use = st.session_state.theme
if theme_to_use == 'system':
    # Detect system theme (simplified - Streamlit handles this automatically)
    theme_to_use = 'light'  # Default fallback

st.markdown(get_css(theme_to_use), unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.markdown(f"### {loc('app_title')}")
    st.markdown(f"*{loc('app_subtitle')}*")
    st.divider()
    
    # Theme selection
    st.markdown(f"**{loc('theme_light').replace('Light', 'Theme')}**")
    theme_options = ['system', 'light', 'dark']
    theme_labels = [loc('theme_system'), loc('theme_light'), loc('theme_dark')]
    theme_idx = st.selectbox(
        "Theme",
        range(len(theme_options)),
        format_func=lambda x: theme_labels[x],
        key='theme_select',
        label_visibility='collapsed'
    )
    st.session_state.theme = theme_options[theme_idx]
    
    # Language selection
    st.markdown(f"**{loc('language')}**")
    lang_options = ['en', 'fa']
    lang_labels = [loc('lang_en'), loc('lang_fa')]
    lang_idx = st.selectbox(
        "Language",
        range(len(lang_options)),
        format_func=lambda x: lang_labels[x],
        key='language_select',
        label_visibility='collapsed'
    )
    st.session_state.language = lang_options[lang_idx]
    loc = Localization(st.session_state.language)
    
    # Unit system
    st.markdown(f"**{loc('unit_system')}**")
    unit_options = ['N', 'kN', 'lbf']
    unit_labels = [loc('unit_n'), loc('unit_kn'), loc('unit_lbf')]
    unit_idx = st.selectbox(
        "Units",
        range(len(unit_options)),
        format_func=lambda x: unit_labels[x],
        key='unit_select',
        label_visibility='collapsed'
    )
    st.session_state.unit = unit_options[unit_idx]
    
    st.divider()
    
    # Project info
    st.markdown("### Project Info")
    st.metric(loc('table_nodes'), len(st.session_state.nodes))
    st.metric(loc('table_members'), len(st.session_state.members))
    st.metric(loc('table_supports'), len(st.session_state.supports))
    st.metric(loc('table_loads'), len(st.session_state.loads))

# Main content area
st.title(loc('app_title'))
st.caption(loc('app_subtitle'))

# Input Tabs
tab_nodes, tab_members, tab_supports, tab_loads = st.tabs([
    loc('tab_nodes'),
    loc('tab_members'),
    loc('tab_supports'),
    loc('tab_loads')
])

# Node Input Tab
with tab_nodes:
    st.markdown("### " + loc('tab_nodes'))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        node_name = st.text_input(
            loc('node_name'),
            placeholder=loc('node_name_placeholder'),
            key='input_node_name'
        )
    
    with col2:
        node_x = st.number_input(
            loc('node_x'),
            value=0.0,
            step=0.5,
            format="%.2f",
            key='input_node_x'
        )
    
    with col3:
        node_y = st.number_input(
            loc('node_y'),
            value=0.0,
            step=0.5,
            format="%.2f",
            key='input_node_y'
        )
    
    if st.button(loc('add_node'), use_container_width=True, type='primary'):
        if node_name:
            # Check for duplicates
            if any(n.name == node_name for n in st.session_state.nodes):
                st.error(loc('error_duplicate_node'))
            else:
                new_node = Node(name=node_name, x=node_x, y=node_y)
                st.session_state.nodes.append(new_node)
                st.rerun()

# Member Input Tab
with tab_members:
    st.markdown("### " + loc('tab_members'))
    
    if len(st.session_state.nodes) < 2:
        st.info(loc('no_nodes'))
    else:
        col1, col2 = st.columns(2)
        
        node_names = [n.name for n in st.session_state.nodes]
        
        with col1:
            start_node = st.selectbox(
                loc('member_start'),
                options=node_names,
                key='input_member_start'
            )
        
        with col2:
            end_node = st.selectbox(
                loc('member_end'),
                options=node_names,
                key='input_member_end'
            )
        
        if st.button(loc('add_member'), use_container_width=True, type='primary'):
            if start_node and end_node:
                if start_node == end_node:
                    st.error(loc('error_zero_length'))
                else:
                    # Auto-generate member name
                    member_name = f"{start_node}{end_node}"
                    
                    # Check for duplicate
                    if any(m.name == member_name for m in st.session_state.members):
                        st.error("Member already exists")
                    else:
                        new_member = Member(
                            name=member_name,
                            start_node=start_node,
                            end_node=end_node
                        )
                        st.session_state.members.append(new_member)
                        st.rerun()

# Support Input Tab
with tab_supports:
    st.markdown("### " + loc('tab_supports'))
    
    if not st.session_state.nodes:
        st.info(loc('no_nodes'))
    else:
        col1, col2, col3 = st.columns(3)
        
        node_names = [n.name for n in st.session_state.nodes]
        
        with col1:
            support_node = st.selectbox(
                loc('support_node'),
                options=node_names,
                key='input_support_node'
            )
        
        with col2:
            support_type = st.selectbox(
                loc('support_type'),
                options=['pinned', 'roller', 'fixed'],
                format_func=lambda x: loc(x),
                key='input_support_type'
            )
        
        with col3:
            support_angle = st.number_input(
                loc('support_angle'),
                value=0.0,
                step=15.0,
                format="%.1f",
                key='input_support_angle'
            )
        
        if st.button(loc('add_support'), use_container_width=True, type='primary'):
            if support_node:
                # Check if support already exists at this node
                if any(s.node == support_node for s in st.session_state.supports):
                    st.error("Support already exists at this node")
                else:
                    new_support = Support(
                        node=support_node,
                        type=support_type,
                        angle=support_angle
                    )
                    st.session_state.supports.append(new_support)
                    st.rerun()

# Load Input Tab
with tab_loads:
    st.markdown("### " + loc('tab_loads'))
    
    if not st.session_state.nodes:
        st.info(loc('no_nodes'))
    else:
        col1, col2, col3 = st.columns(3)
        
        node_names = [n.name for n in st.session_state.nodes]
        
        with col1:
            load_name = st.text_input(
                loc('load_name'),
                placeholder=loc('load_name_placeholder'),
                key='input_load_name'
            )
        
        with col2:
            load_node = st.selectbox(
                loc('load_node'),
                options=node_names,
                key='input_load_node'
            )
        
        with col3:
            load_magnitude = st.number_input(
                loc('load_magnitude'),
                value=1.0,
                step=0.5,
                format="%.2f",
                key='input_load_magnitude',
                min_value=0.0
            )
        
        load_angle = st.number_input(
            loc('load_angle'),
            value=0.0,
            step=15.0,
            format="%.1f",
            key='input_load_angle'
        )
        
        if st.button(loc('add_load'), use_container_width=True, type='primary'):
            if load_name and load_node:
                # Check for duplicate load names
                if any(l.name == load_name for l in st.session_state.loads):
                    st.error("Load name already exists")
                else:
                    new_load = Load(
                        name=load_name,
                        node=load_node,
                        magnitude=load_magnitude,
                        angle=load_angle
                    )
                    st.session_state.loads.append(new_load)
                    st.rerun()

# Live Preview
st.divider()
st.markdown(f"### {loc('live_preview')}")

if st.session_state.nodes and st.session_state.members:
    plotter = TrussPlotter(
        st.session_state.nodes,
        st.session_state.members,
        st.session_state.supports,
        st.session_state.loads
    )
    fig = plotter.create_preview_figure(figsize=(8, 6))
    st.pyplot(fig)
else:
    st.info(loc('no_structure'))

# Data Tables
st.divider()
st.markdown("### Project Data")

# Create tabs for each data type
data_tabs = st.tabs([
    f"{loc('table_nodes')} ({len(st.session_state.nodes)})",
    f"{loc('table_members')} ({len(st.session_state.members)})",
    f"{loc('table_supports')} ({len(st.session_state.supports)})",
    f"{loc('table_loads')} ({len(st.session_state.loads)})"
])

# Nodes Table
with data_tabs[0]:
    if st.session_state.nodes:
        nodes_df = pd.DataFrame([
            {'Name': n.name, 'X': n.x, 'Y': n.y}
            for n in st.session_state.nodes
        ])
        st.dataframe(nodes_df, use_container_width=True, hide_index=True)
        
        # Delete functionality
        for i, node in enumerate(st.session_state.nodes):
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.button(loc('delete'), key=f'del_node_{i}'):
                    if st.session_state.show_delete_confirm == f'node_{i}':
                        st.session_state.nodes.pop(i)
                        st.session_state.show_delete_confirm = None
                        st.rerun()
                    else:
                        st.session_state.show_delete_confirm = f'node_{i}'
                        st.warning(loc('confirm_delete'))
            with col1:
                if st.session_state.show_delete_confirm == f'node_{i}':
                    if st.button(loc('confirm'), key=f'confirm_node_{i}'):
                        st.session_state.nodes.pop(i)
                        st.session_state.show_delete_confirm = None
                        st.rerun()

# Members Table
with data_tabs[1]:
    if st.session_state.members:
        members_df = pd.DataFrame([
            {'Name': m.name, 'Start': m.start_node, 'End': m.end_node}
            for m in st.session_state.members
        ])
        st.dataframe(members_df, use_container_width=True, hide_index=True)
        
        for i, member in enumerate(st.session_state.members):
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.button(loc('delete'), key=f'del_member_{i}'):
                    st.session_state.members.pop(i)
                    st.rerun()

# Supports Table
with data_tabs[2]:
    if st.session_state.supports:
        supports_df = pd.DataFrame([
            {'Node': s.node, 'Type': loc(s.type), 'Angle': f"{s.angle}°"}
            for s in st.session_state.supports
        ])
        st.dataframe(supports_df, use_container_width=True, hide_index=True)
        
        for i, support in enumerate(st.session_state.supports):
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.button(loc('delete'), key=f'del_support_{i}'):
                    st.session_state.supports.pop(i)
                    st.rerun()

# Loads Table
with data_tabs[3]:
    if st.session_state.loads:
        loads_df = pd.DataFrame([
            {'Name': l.name, 'Node': l.node, 'Magnitude': l.magnitude, 'Angle': f"{l.angle}°"}
            for l in st.session_state.loads
        ])
        st.dataframe(loads_df, use_container_width=True, hide_index=True)
        
        for i, load in enumerate(st.session_state.loads):
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.button(loc('delete'), key=f'del_load_{i}'):
                    st.session_state.loads.pop(i)
                    st.rerun()

# Action Buttons
st.divider()
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    if st.button(loc('analyze'), use_container_width=True, type='primary', key='analyze_button'):
        # Validate structure
        solver = TrussSolver(
            st.session_state.nodes,
            st.session_state.members,
            st.session_state.supports,
            st.session_state.loads
        )
        
        errors = solver.validate_structure()
        
        if errors:
            st.session_state.errors = errors
            st.session_state.analysis_complete = False
            for error in errors:
                st.error(error)
        else:
            success = solver.solve()
            if success:
                st.session_state.analysis_complete = True
                st.session_state.results = {
                    'reactions': solver.reactions,
                    'member_forces': solver.member_forces,
                    'displacements': solver.displacements
                }
                st.session_state.errors = []
                st.success(loc('analysis_complete'))
            else:
                st.session_state.analysis_complete = False
                st.session_state.errors = ['error_unstable']
                st.error(loc('error_unstable'))

with col2:
    if st.button(loc('export_pdf'), use_container_width=True):
        if st.session_state.analysis_complete:
            # Create preview figure
            plotter = TrussPlotter(
                st.session_state.nodes,
                st.session_state.members,
                st.session_state.supports,
                st.session_state.loads
            )
            preview_fig = plotter.create_preview_figure()
            
            # Create result figure
            plotter.set_results(
                st.session_state.results['reactions'],
                st.session_state.results['member_forces']
            )
            result_fig = plotter.create_result_figure()
            
            # Generate PDF
            exporter = PDFExporter()
            input_data = {
                'nodes': st.session_state.nodes,
                'members': st.session_state.members,
                'supports': st.session_state.supports,
                'loads': st.session_state.loads
            }
            
            pdf_buffer = exporter.create_report(
                input_data,
                st.session_state.results,
                preview_fig,
                result_fig,
                st.session_state.unit
            )
            
            # Download button
            st.download_button(
                label="Download PDF",
                data=pdf_buffer,
                file_name="truss_analysis_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.warning("Run analysis first")

with col3:
    if st.button(loc('reset'), use_container_width=True, type='secondary'):
        if st.session_state.show_reset_confirm:
            # Perform reset
            st.session_state.nodes = []
            st.session_state.members = []
            st.session_state.supports = []
            st.session_state.loads = []
            st.session_state.analysis_complete = False
            st.session_state.results = None
            st.session_state.errors = []
            st.session_state.show_reset_confirm = False
            st.rerun()
        else:
            st.session_state.show_reset_confirm = True
            st.warning(loc('confirm_reset'))
            if st.button(loc('confirm')):
                st.session_state.nodes = []
                st.session_state.members = []
                st.session_state.supports = []
                st.session_state.loads = []
                st.session_state.analysis_complete = False
                st.session_state.results = None
                st.session_state.errors = []
                st.session_state.show_reset_confirm = False
                st.rerun()

# Results Section
if st.session_state.analysis_complete and st.session_state.results:
    st.divider()
    st.markdown("## Analysis Results")
    
    # Result visualization
    plotter = TrussPlotter(
        st.session_state.nodes,
        st.session_state.members,
        st.session_state.supports,
        st.session_state.loads
    )
    plotter.set_results(
        st.session_state.results['reactions'],
        st.session_state.results['member_forces']
    )
    result_fig = plotter.create_result_figure(figsize=(10, 7))
    st.pyplot(result_fig)
    
    # Results tables
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### {loc('reaction_forces')}")
        if st.session_state.results['reactions']:
            reactions_data = []
            for node_name, reaction in st.session_state.results['reactions'].items():
                magnitude = math.sqrt(reaction[0]**2 + reaction[1]**2)
                angle = math.degrees(math.atan2(reaction[1], reaction[0])) if magnitude > 1e-10 else 0
                reactions_data.append({
                    loc('support'): node_name,
                    f"{loc('force_fx')} ({st.session_state.unit})": f"{reaction[0]:.3f}",
                    f"{loc('force_fy')} ({st.session_state.unit})": f"{reaction[1]:.3f}",
                    f"{loc('resultant')} ({st.session_state.unit})": f"{magnitude:.3f}",
                    f"{loc('angle')} (°)": f"{angle:.1f}"
                })
            
            reactions_df = pd.DataFrame(reactions_data)
            st.dataframe(reactions_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown(f"### {loc('member_forces')}")
        if st.session_state.results['member_forces']:
            members_data = []
            for member_name, force in st.session_state.results['member_forces'].items():
                force_type = loc('tension') if force > 1e-10 else loc('compression') if force < -1e-10 else 'Zero'
                members_data.append({
                    loc('member'): member_name,
                    f"{loc('force_value')} ({st.session_state.unit})": f"{abs(force):.3f}",
                    loc('type'): force_type
                })
            
            members_df = pd.DataFrame(members_data)
            
            # Apply styling to force type column
            def color_force_type(val):
                if val == loc('tension'):
                    return 'color: #3B82F6; font-weight: bold'
                elif val == loc('compression'):
                    return 'color: #EF4444; font-weight: bold'
                return ''
            
            styled_df = members_df.style.map(color_force_type, subset=[loc('type')])
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Summary metrics
    st.divider()
    st.markdown("### Summary")
    
    metric_cols = st.columns(4)
    
    with metric_cols[0]:
        max_tension = max(
            [f for f in st.session_state.results['member_forces'].values() if f > 0],
            default=0
        )
        st.metric(
            "Max Tension",
            f"{max_tension:.3f} {st.session_state.unit}",
            delta=None
        )
    
    with metric_cols[1]:
        max_compression = min(
            [f for f in st.session_state.results['member_forces'].values() if f < 0],
            default=0
        )
        st.metric(
            "Max Compression",
            f"{abs(max_compression):.3f} {st.session_state.unit}",
            delta=None
        )
    
    with metric_cols[2]:
        max_reaction = max(
            [math.sqrt(r[0]**2 + r[1]**2) 
             for r in st.session_state.results['reactions'].values()],
            default=0
        )
        st.metric(
            "Max Reaction",
            f"{max_reaction:.3f} {st.session_state.unit}",
            delta=None
        )
    
    with metric_cols[3]:
        zero_force_members = sum(
            1 for f in st.session_state.results['member_forces'].values()
            if abs(f) < 1e-10
        )
        st.metric(
            "Zero-Force Members",
            str(zero_force_members),
            delta=None
        )

# Footer
st.divider()
st.caption("2D Truss Analysis System | Professional Engineering Software | v1.0.0")