"""
Direct Stiffness Method solver for 2D truss analysis.
Properly handles support conditions and calculates reactions.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import math

@dataclass
class Node:
    """Represents a node in the truss structure."""
    name: str
    x: float
    y: float

@dataclass
class Member:
    """Represents a member connecting two nodes."""
    name: str
    start_node: str
    end_node: str

@dataclass
class Support:
    """Represents a support condition at a node."""
    node: str
    type: str  # 'pinned', 'roller', 'fixed'
    angle: float  # degrees, counterclockwise from positive X

@dataclass
class Load:
    """Represents a concentrated load at a node."""
    name: str
    node: str
    magnitude: float
    angle: float  # degrees, counterclockwise from positive X

class TrussSolver:
    """Solves 2D truss structures using the Direct Stiffness Method."""
    
    def __init__(self, nodes: List[Node], members: List[Member], 
                 supports: List[Support], loads: List[Load]):
        self.nodes = {n.name: n for n in nodes}
        self.members = members
        self.supports = supports
        self.loads = loads
        
        # Results storage
        self.displacements = None
        self.reactions = None
        self.member_forces = None
        
        # Build DOF mapping
        self.node_dof_map = {}
        self._build_dof_mapping()
    
    def _build_dof_mapping(self):
        """Map each node to its global degree of freedom indices."""
        dof_count = 0
        for node_name in sorted(self.nodes.keys()):
            self.node_dof_map[node_name] = dof_count
            dof_count += 2
    
    def _get_node_dofs(self, node_name):
        """Get global DOF indices for a node."""
        start_idx = self.node_dof_map[node_name]
        return start_idx, start_idx + 1
    
    def _calculate_member_properties(self, member):
        """Calculate length and direction cosines for a member."""
        start = self.nodes[member.start_node]
        end = self.nodes[member.end_node]
        dx = end.x - start.x
        dy = end.y - start.y
        length = math.sqrt(dx**2 + dy**2)
        
        if length < 1e-10:
            raise ValueError(f"Zero-length member: {member.name}")
        
        cx = dx / length
        cy = dy / length
        return length, cx, cy
    
    def _get_member_stiffness_global(self, member):
        """Get member stiffness matrix in global coordinates."""
        length, cx, cy = self._calculate_member_properties(member)
        EA = 1.0  # Unit stiffness for now
        
        # Element stiffness in global coordinates (4x4)
        k = (EA / length) * np.array([
            [cx*cx, cx*cy, -cx*cx, -cx*cy],
            [cx*cy, cy*cy, -cx*cy, -cy*cy],
            [-cx*cx, -cx*cy, cx*cx, cx*cy],
            [-cx*cy, -cy*cy, cx*cy, cy*cy]
        ])
        
        return k
    
    def _get_support_constraints(self):
        """
        Determine which DOFs are constrained by supports.
        Returns a list of constrained DOF indices.
        """
        constrained = []
        
        for support in self.supports:
            if support.node not in self.nodes:
                continue
            
            dof_x, dof_y = self._get_node_dofs(support.node)
            
            if support.type == 'fixed' or support.type == 'pinned':
                # Both DOFs constrained
                constrained.append(dof_x)
                constrained.append(dof_y)
                
            elif support.type == 'roller':
                # One DOF constrained based on angle
                angle_rad = math.radians(support.angle)
                
                # The normal direction (perpendicular to rolling surface)
                # is what's constrained
                if abs(math.cos(angle_rad)) >= abs(math.sin(angle_rad)):
                    constrained.append(dof_x)
                else:
                    constrained.append(dof_y)
        
        return sorted(set(constrained))
    
    def solve(self):
        """Solve the truss structure."""
        try:
            total_dofs = len(self.nodes) * 2
            
            # Initialize global stiffness matrix
            K = np.zeros((total_dofs, total_dofs))
            
            # Assemble global stiffness matrix
            for member in self.members:
                if member.start_node not in self.nodes or member.end_node not in self.nodes:
                    continue
                
                k_member = self._get_member_stiffness_global(member)
                dof_start = list(self._get_node_dofs(member.start_node))
                dof_end = list(self._get_node_dofs(member.end_node))
                dof_indices = dof_start + dof_end
                
                for i in range(4):
                    for j in range(4):
                        K[dof_indices[i], dof_indices[j]] += k_member[i, j]
            
            # Build force vector
            F = np.zeros(total_dofs)
            for load in self.loads:
                if load.node not in self.nodes:
                    continue
                dof_x, dof_y = self._get_node_dofs(load.node)
                angle_rad = math.radians(load.angle)
                F[dof_x] += load.magnitude * math.cos(angle_rad)
                F[dof_y] += load.magnitude * math.sin(angle_rad)
            
            # Get constrained DOFs
            constrained = self._get_support_constraints()
            free = [i for i in range(total_dofs) if i not in constrained]
            
            # DEBUG: Print info about the system
            print(f"Total DOFs: {total_dofs}")
            print(f"Free DOFs: {free}")
            print(f"Constrained DOFs: {constrained}")
            print(f"Number of supports: {len(self.supports)}")
            print(f"Number of members: {len(self.members)}")
            print(f"Force vector: {F}")
            
            if len(free) == 0:
                print("ERROR: All DOFs are constrained")
                return False
            
            # Partition matrices
            K_ff = K[np.ix_(free, free)]
            F_f = F[free]
            
            print(f"K_ff shape: {K_ff.shape}")
            print(f"K_ff:\n{K_ff}")
            print(f"K_ff rank: {np.linalg.matrix_rank(K_ff)}")
            
            # Check conditioning
            cond = np.linalg.cond(K_ff)
            print(f"Condition number: {cond}")
            
            if cond > 1e10:
                print("ERROR: Matrix is nearly singular")
                return False
            
            # Solve for free displacements
            U_f = np.linalg.solve(K_ff, F_f)
            
            # Build complete displacement vector
            U = np.zeros(total_dofs)
            U[free] = U_f
            
            # Store displacements
            self.displacements = {}
            for node_name in self.nodes:
                dof_x, dof_y = self._get_node_dofs(node_name)
                self.displacements[node_name] = np.array([U[dof_x], U[dof_y]])
            
            # Calculate ALL nodal forces (internal)
            F_internal = K @ U
            
            # Reactions are the internal forces at constrained DOFs
            # minus any applied loads at those DOFs
            self.reactions = {}
            for support in self.supports:
                if support.node not in self.nodes:
                    continue
                dof_x, dof_y = self._get_node_dofs(support.node)
                
                rx = F_internal[dof_x] - F[dof_x]
                ry = F_internal[dof_y] - F[dof_y]
                
                self.reactions[support.node] = np.array([rx, ry])
            
            # Calculate member forces
            self.member_forces = {}
            for member in self.members:
                if member.start_node not in self.nodes or member.end_node not in self.nodes:
                    continue
                
                length, cx, cy = self._calculate_member_properties(member)
                EA = 1.0
                
                start_disp = self.displacements[member.start_node]
                end_disp = self.displacements[member.end_node]
                
                # Axial deformation in local coordinates
                u_start = cx * start_disp[0] + cy * start_disp[1]
                u_end = cx * end_disp[0] + cy * end_disp[1]
                
                # Force = EA/L * (elongation)
                force = (EA / length) * (u_end - u_start)
                self.member_forces[member.name] = force
            
            return True
            
        except np.linalg.LinAlgError as e:
            print(f"Linear algebra error: {e}")
            return False
        except Exception as e:
            print(f"Solver error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_reaction_resultant(self, support_node):
        """Get reaction force resultant magnitude and direction."""
        if self.reactions is None or support_node not in self.reactions:
            return 0.0, 0.0
        
        reaction = self.reactions[support_node]
        magnitude = np.linalg.norm(reaction)
        if magnitude < 1e-10:
            return 0.0, 0.0
        
        angle = math.degrees(math.atan2(reaction[1], reaction[0]))
        return magnitude, angle
    
    def validate_structure(self):
        """Validate the structure."""
        errors = []
        
        if not self.nodes:
            errors.append('No nodes defined')
        
        if not self.members:
            errors.append('No members defined')
        
        if not self.supports:
            errors.append('No supports defined - structure needs supports to be stable')
        
        # Check minimum supports for stability
        if self.supports:
            constrained_dofs = self._get_support_constraints()
            if len(constrained_dofs) < 3:
                errors.append(f'Structure may be unstable: only {len(constrained_dofs)} DOFs constrained. Need at least 3 for 2D stability.')
        
        for member in self.members:
            if member.start_node not in self.nodes:
                errors.append(f"Member {member.name}: Start node '{member.start_node}' not found")
            if member.end_node not in self.nodes:
                errors.append(f"Member {member.name}: End node '{member.end_node}' not found")
            if member.start_node == member.end_node:
                errors.append(f"Member {member.name}: Zero-length member")
        
        for load in self.loads:
            if load.node not in self.nodes:
                errors.append(f"Load {load.name}: Node '{load.node}' not found")
        
        return errors