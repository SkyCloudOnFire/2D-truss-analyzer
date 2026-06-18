"""
Visualization module for 2D truss analysis.
Provides live preview and result visualization using matplotlib.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.figure import Figure
import numpy as np
import math
from typing import Dict, List, Optional
from solver import Node, Member, Support, Load

# Use a modern matplotlib style
plt.style.use('seaborn-v0_8-whitegrid')

class TrussPlotter:
    """Creates visualizations for truss structures."""
    
    def __init__(self, nodes: List[Node], members: List[Member], 
                 supports: List[Support], loads: List[Load]):
        self.nodes = {n.name: n for n in nodes}
        self.members = members
        self.supports = supports
        self.loads = loads
        
        # Results (optional)
        self.reactions: Optional[Dict[str, np.ndarray]] = None
        self.member_forces: Optional[Dict[str, float]] = None
    
    def set_results(self, reactions: Dict[str, np.ndarray], 
                    member_forces: Dict[str, float]):
        """Set analysis results for visualization."""
        self.reactions = reactions
        self.member_forces = member_forces
    
    def _draw_support_symbol(self, ax, node: Node, support: Support):
        """Draw support symbol at the specified node."""
        # Support triangle size
        size = 0.3
        x, y = node.x, node.y
        angle_rad = math.radians(support.angle)
        
        if support.type == 'pinned':
            # Triangle with circle
            triangle = patches.RegularPolygon(
                (x, y - size/2), 3, radius=size/1.5, 
                orientation=math.pi, color='#64748B', zorder=3
            )
            ax.add_patch(triangle)
            circle = plt.Circle((x, y), size/3, fill=False, 
                              color='#64748B', linewidth=2, zorder=4)
            ax.add_patch(circle)
            
        elif support.type == 'roller':
            # Triangle with circles below
            triangle = patches.RegularPolygon(
                (x, y - size/2), 3, radius=size/1.5,
                orientation=math.pi, color='#64748B', zorder=3
            )
            ax.add_patch(triangle)
            # Draw rollers
            for offset in [-size/3, 0, size/3]:
                circle = plt.Circle(
                    (x + offset, y - size - size/4), 
                    size/5, fill=False, color='#64748B', linewidth=1.5, zorder=4
                )
                ax.add_patch(circle)
                
        elif support.type == 'fixed':
            # Fixed support symbol
            hatching = patches.Rectangle(
                (x - size/2, y - size), size, size/3,
                color='#64748B', zorder=3, hatch='////', fill=True,
                alpha=0.3
            )
            ax.add_patch(hatching)
    
    def _draw_load_arrow(self, ax, node: Node, load: Load):
        """Draw load arrow at the specified node."""
        angle_rad = math.radians(load.angle)
        magnitude = load.magnitude
        
        # Arrow length proportional to magnitude (with scaling)
        scale = 0.5
        dx = scale * math.cos(angle_rad)
        dy = scale * math.sin(angle_rad)
        
        # Draw arrow
        ax.arrow(node.x - dx, node.y - dy, dx, dy,
                head_width=0.1, head_length=0.15,
                fc='#EF4444', ec='#EF4444',
                linewidth=2, zorder=5)
        
        # Add load label
        label_offset = 0.2
        ax.text(node.x - dx - label_offset * math.cos(angle_rad),
                node.y - dy - label_offset * math.sin(angle_rad),
                f'{load.name}: {magnitude:.1f}',
                fontsize=8, color='#EF4444',
                ha='center', va='center', zorder=5,
                bbox=dict(boxstyle='round,pad=0.1', 
                         facecolor='white', alpha=0.8, edgecolor='none'))
    
    def create_preview_figure(self, figsize=(10, 8)) -> Figure:
        """Create a preview figure of the truss structure."""
        fig, ax = plt.subplots(figsize=figsize, facecolor='white')
        ax.set_facecolor('#F8FAFC')
        
        # Set equal aspect ratio
        ax.set_aspect('equal')
        
        # Draw members
        for member in self.members:
            if member.start_node in self.nodes and member.end_node in self.nodes:
                start = self.nodes[member.start_node]
                end = self.nodes[member.end_node]
                ax.plot([start.x, end.x], [start.y, end.y], 
                       'b-', linewidth=2.5, color='#3B82F6', zorder=1,
                       alpha=0.7)
        
        # Draw nodes
        for node in self.nodes.values():
            ax.plot(node.x, node.y, 'o', markersize=8, 
                   color='#1E293B', zorder=2, markeredgecolor='white',
                   markeredgewidth=1.5)
            ax.text(node.x + 0.15, node.y + 0.15, node.name,
                   fontsize=10, fontweight='bold', color='#0F172A',
                   ha='left', va='bottom', zorder=6)
        
        # Draw supports
        for support in self.supports:
            if support.node in self.nodes:
                self._draw_support_symbol(ax, self.nodes[support.node], support)
        
        # Draw loads
        for load in self.loads:
            if load.node in self.nodes:
                self._draw_load_arrow(ax, self.nodes[load.node], load)
        
        # Style the plot
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xlabel('X Coordinate', fontsize=10, color='#64748B')
        ax.set_ylabel('Y Coordinate', fontsize=10, color='#64748B')
        ax.tick_params(colors='#64748B')
        
        # Remove top and right spines for cleaner look
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        return fig
    
    def create_result_figure(self, figsize=(10, 8)) -> Figure:
        """Create a result visualization figure."""
        fig, ax = plt.subplots(figsize=figsize, facecolor='white')
        ax.set_facecolor('#F8FAFC')
        ax.set_aspect('equal')
        
        if self.member_forces:
            max_force = max(abs(f) for f in self.member_forces.values() if abs(f) > 1e-10)
        else:
            max_force = 1.0
        
        # Draw members with force coloring
        for member in self.members:
            if member.start_node in self.nodes and member.end_node in self.nodes:
                start = self.nodes[member.start_node]
                end = self.nodes[member.end_node]
                
                force = self.member_forces.get(member.name, 0) if self.member_forces else 0
                
                # Color based on tension (blue) or compression (red)
                if force > 1e-10:
                    color = '#3B82F6'  # Blue for tension
                    alpha = min(0.3 + abs(force) / max_force * 0.7, 1.0)
                elif force < -1e-10:
                    color = '#EF4444'  # Red for compression
                    alpha = min(0.3 + abs(force) / max_force * 0.7, 1.0)
                else:
                    color = '#64748B'  # Gray for zero force
                    alpha = 0.5
                
                linewidth = 2.5 + abs(force) / max_force * 3
                ax.plot([start.x, end.x], [start.y, end.y],
                       linewidth=linewidth, color=color, alpha=alpha, zorder=1)
                
                # Add force label on member
                mid_x, mid_y = (start.x + end.x) / 2, (start.y + end.y) / 2
                offset_x = (end.y - start.y) * 0.1
                offset_y = -(end.x - start.x) * 0.1
                ax.text(mid_x + offset_x, mid_y + offset_y,
                       f'{force:.2f}',
                       fontsize=8, color=color, fontweight='bold',
                       ha='center', va='center', zorder=7,
                       bbox=dict(boxstyle='round,pad=0.1',
                                facecolor='white', alpha=0.9, edgecolor='none'))
        
        # Draw nodes
        for node in self.nodes.values():
            ax.plot(node.x, node.y, 'o', markersize=8,
                   color='#1E293B', zorder=2, markeredgecolor='white',
                   markeredgewidth=1.5)
            ax.text(node.x + 0.15, node.y + 0.15, node.name,
                   fontsize=10, fontweight='bold', color='#0F172A',
                   ha='left', va='bottom', zorder=6)
        
        # Draw supports with reactions
        if self.reactions:
            for support in self.supports:
                if support.node in self.nodes:
                    self._draw_support_symbol(ax, self.nodes[support.node], support)
                    
                    # Draw reaction arrows
                    node = self.nodes[support.node]
                    reaction = self.reactions.get(support.node, np.array([0, 0]))
                    magnitude = np.linalg.norm(reaction)
                    
                    if magnitude > 1e-10:
                        scale = 0.3
                        dx = scale * reaction[0] / magnitude
                        dy = scale * reaction[1] / magnitude
                        
                        ax.arrow(node.x, node.y, dx, dy,
                                head_width=0.1, head_length=0.15,
                                fc='#10B981', ec='#10B981',
                                linewidth=2, zorder=5)
                        
                        ax.text(node.x + dx * 1.5, node.y + dy * 1.5,
                               f'R: {magnitude:.2f}',
                               fontsize=8, color='#10B981',
                               fontweight='bold', zorder=7,
                               bbox=dict(boxstyle='round,pad=0.1',
                                        facecolor='white', alpha=0.9, edgecolor='none'))
        
        # Draw loads
        for load in self.loads:
            if load.node in self.nodes:
                self._draw_load_arrow(ax, self.nodes[load.node], load)
        
        # Legend
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], color='#3B82F6', lw=3, label='Tension'),
            Line2D([0], [0], color='#EF4444', lw=3, label='Compression'),
            Line2D([0], [0], color='#10B981', lw=3, label='Reaction')
        ]
        ax.legend(handles=legend_elements, loc='upper right',
                 frameon=True, facecolor='white', edgecolor='#E2E8F0')
        
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xlabel('X Coordinate', fontsize=10, color='#64748B')
        ax.set_ylabel('Y Coordinate', fontsize=10, color='#64748B')
        ax.tick_params(colors='#64748B')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        return fig