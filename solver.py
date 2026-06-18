"""
Direct Stiffness Method solver for 2D truss analysis.
Implements the matrix stiffness method with proper coordinate transformations.
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
    """
    Solves 2D truss structures using the Direct Stiffness Method.
    """
    
    def __init__(self, nodes: List[Node], members: List[Member], 
                 supports: List[Support], loads: List[Load]):
        self.nodes = {n.name: n for n in nodes}
        self.members = members
        self.supports = supports
        self.loads = loads
        
        # Results storage
        self.displacements: Optional[Dict[str, np.ndarray]] = None
        self.reactions: Optional[Dict[str, np.ndarray]] = None
        self.member_forces: Optional[Dict[str, float]] = None
        
        # Global DOF mapping
        self.node_dof_map: Dict[str, int] = {}
        self._build_dof_mapping()
    
    def _build_dof_mapping(self):
        """Map each node to its global degree of freedom indices."""
        dof_count = 0
        for node_name in sorted(self.nodes.keys()):
            self.node_dof_map[node_name] = dof_count
            dof_count += 2  # 2 DOFs per node (x, y)
    
    def _get_node_dofs(self, node_name: str) -> Tuple[int, int]:
        """Get global DOF indices for a node."""
        start_idx = self.node_dof_map[node_name]
        return start_idx, start_idx + 1
    
    def _calculate_member_length(self, member: Member) -> float:
        """Calculate the length of a member."""
        start = self.nodes[member.start_node]
        end = self.nodes[member.end_node]
        dx = end.x - start.x
        dy = end.y - start.y
        return math.sqrt(dx**2 + dy**2)
    
    def _calculate_direction_cosines(self, member: Member) -> Tuple[float, float]:
        """Calculate direction cosines (cx, cy) for a member."""
        start = self.nodes[member.start_node]
        end = self.nodes[member.end_node]
        length = self._calculate_member_length(member)
        
        if length < 1e-10:
            raise ValueError(f"Zero-length member: {member.name}")
        
        cx = (end.x - start.x) / length
        cy = (end.y - start.y) / length
        return cx, cy
    
    def _create_local_stiffness_matrix(self, member: Member) -> np.ndarray:
        """Create 4x4 local stiffness matrix for a truss element."""
        length = self._calculate_member_length(member)
        EA = 1.0  # Assume EA = 1 (unit stiffness)
        
        # Local stiffness matrix (4x4)
        k_local = (EA / length) * np.array([
            [1, 0, -1, 0],
            [0, 0, 0, 0],
            [-1, 0, 1, 0],
            [0, 0, 0, 0]
        ])
        
        return k_local
    
    def _create_transformation_matrix(self, cx: float, cy: float) -> np.ndarray:
        """Create 4x4 transformation matrix from local to global coordinates."""
        T = np.array([
            [cx, cy, 0, 0],
            [-cy, cx, 0, 0],
            [0, 0, cx, cy],
            [0, 0, -cy, cx]
        ])
        return T
    
    def _get_global_stiffness_matrix(self, member: Member) -> np.ndarray:
        """Get member stiffness matrix in global coordinates."""
        cx, cy = self._calculate_direction_cosines(member)
        k_local = self._create_local_stiffness_matrix(member)
        T = self._create_transformation_matrix(cx, cy)
        return T.T @ k_local @ T
    
    def _get_constrained_dofs(self) -> List[int]:
        """
        Get list of constrained DOF indices based on support conditions.
        Returns list of DOF indices that are fixed.
        """
        constrained_dofs = []
        
        for support in self.supports:
            node_name = support.node
            if node_name not in self.nodes:
                continue
            
            dof_x, dof_y = self._get_node_dofs(node_name)
            angle_rad = math.radians(support.angle)
            
            if support.type == 'fixed':
                # Fixed: constrain both X and Y
                constrained_dofs.extend([dof_x, dof_y])
            elif support.type == 'pinned':
                # Pinned: constrain both X and Y (like fixed for 2D truss)
                constrained_dofs.extend([dof_x, dof_y])
            elif support.type == 'roller':
                # Roller: constrain perpendicular to the rolling direction
                # The roller allows movement ALONG the support surface
                # Support angle defines the direction of the normal (constrained direction)
                normal_x = math.cos(angle_rad)
                normal_y = math.sin(angle_rad)
                
                # If normal is closer to X direction, constrain X
                if abs(normal_x) > abs(normal_y):
                    constrained_dofs.append(dof_x)
                else:
                    constrained_dofs.append(dof_y)
        
        return constrained_dofs
    
    def solve(self) -> bool:
        """
        Solve the truss structure using Direct Stiffness Method.
        Returns True if solution converged, False otherwise.
        """
        try:
            total_dofs = len(self.nodes) * 2
            
            # Initialize global stiffness matrix and force vector
            K_global = np.zeros((total_dofs, total_dofs))
            F = np.zeros(total_dofs)
            
            # Assemble global stiffness matrix
            for member in self.members:
                if member.start_node not in self.nodes or member.end_node not in self.nodes:
                    continue
                
                k_global_member = self._get_global_stiffness_matrix(member)
                dof_start_x, dof_start_y = self._get_node_dofs(member.start_node)
                dof_end_x, dof_end_y = self._get_node_dofs(member.end_node)
                
                # Assembly indices
                indices = [dof_start_x, dof_start_y, dof_end_x, dof_end_y]
                for i in range(4):
                    for j in range(4):
                        K_global[indices[i], indices[j]] += k_global_member[i, j]
            
            # Build force vector
            for load in self.loads:
                if load.node not in self.nodes:
                    continue
                dof_x, dof_y = self._get_node_dofs(load.node)
                angle_rad = math.radians(load.angle)
                F[dof_x] += load.magnitude * math.cos(angle_rad)
                F[dof_y] += load.magnitude * math.sin(angle_rad)
            
            # Get constrained DOFs
            constrained_dofs = self._get_constrained_dofs()
            constrained_dofs = sorted(set(constrained_dofs))  # Remove duplicates and sort
            free_dofs = [i for i in range(total_dofs) if i not in constrained_dofs]
            
            if not free_dofs:
                return False  # All DOFs constrained
            
            # Extract free DOF submatrices
            K_ff = K_global[np.ix_(free_dofs, free_dofs)]
            K_fc = K_global[np.ix_(free_dofs, constrained_dofs)]
            K_cf = K_global[np.ix_(constrained_dofs, free_dofs)]
            K_cc = K_global[np.ix_(constrained_dofs, constrained_dofs)]
            
            F_f = F[free_dofs]
            
            # Check for singularity
            if np.linalg.cond(K_ff) > 1e12:
                return False
            
            # Solve for displacements (free DOFs only)
            U_f = np.linalg.solve(K_ff, F_f)
            
            # Reconstruct full displacement vector
            U = np.zeros(total_dofs)
            U[free_dofs] = U_f
            # Constrained DOFs have zero displacement (already zero)
            
            # Store displacements
            self.displacements = {}
            for node_name in self.nodes:
                dof_x, dof_y = self._get_node_dofs(node_name)
                self.displacements[node_name] = np.array([U[dof_x], U[dof_y]])
            
            # Calculate reactions using the FULL stiffness matrix
            # Reactions = K * U - F_applied (for constrained DOFs)
            self.reactions = {}
            
            # Method: R = K * U (gives forces at all DOFs)
            all_forces = K_global @ U
            
            # Reactions are the forces at constrained DOFs
            # But we need to subtract any applied loads at those DOFs
            for support in self.supports:
                node_name = support.node
                if node_name not in self.nodes:
                    continue
                
                dof_x, dof_y = self._get_node_dofs(node_name)
                
                # Reaction = Internal force - Applied load at that DOF
                rx = all_forces[dof_x] - F[dof_x]
                ry = all_forces[dof_y] - F[dof_y]
                
                self.reactions[node_name] = np.array([rx, ry])
            
            # Calculate member forces
            self.member_forces = {}
            for member in self.members:
                if member.start_node not in self.nodes or member.end_node not in self.nodes:
                    continue
                
                cx, cy = self._calculate_direction_cosines(member)
                length = self._calculate_member_length(member)
                EA = 1.0
                
                # Get displacements at both ends
                start_disp = self.displacements[member.start_node]
                end_disp = self.displacements[member.end_node]
                
                # Transform to local coordinates
                u_local_start = cx * start_disp[0] + cy * start_disp[1]
                u_local_end = cx * end_disp[0] + cy * end_disp[1]
                
                # Axial force (positive = tension)
                force = (EA / length) * (u_local_end - u_local_start)
                self.member_forces[member.name] = force
            
            return True
            
        except Exception as e:
            print(f"Solution error: {e}")
            return False
    
    def get_reaction_resultant(self, support_node: str) -> Tuple[float, float]:
        """Get reaction force resultant magnitude and direction."""
        if self.reactions is None or support_node not in self.reactions:
            return 0.0, 0.0
        
        reaction = self.reactions[support_node]
        magnitude = np.linalg.norm(reaction)
        if magnitude < 1e-10:
            return 0.0, 0.0
        
        angle = math.degrees(math.atan2(reaction[1], reaction[0]))
        return magnitude, angle
    
    def validate_structure(self) -> List[str]:
        """
        Validate the structure and return list of error messages.
        Returns empty list if structure is valid.
        """
        errors = []
        
        # Check for nodes
        if not self.nodes:
            errors.append('No nodes defined')
        
        # Check for members
        if not self.members:
            errors.append('No members defined')
        
        # Check for supports
        if not self.supports:
            errors.append('No supports defined')
        
        # Check member connections
        for member in self.members:
            if member.start_node not in self.nodes:
                errors.append(f"Member {member.name}: Start node '{member.start_node}' not found")
            if member.end_node not in self.nodes:
                errors.append(f"Member {member.name}: End node '{member.end_node}' not found")
            if member.start_node == member.end_node:
                errors.append(f"Member {member.name}: Zero-length member")
        
        # Check load nodes exist
        for load in self.loads:
            if load.node not in self.nodes:
                errors.append(f"Load {load.name}: Node '{load.node}' not found")
        
        return errors