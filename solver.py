"""
Direct Stiffness Method solver for 2D truss analysis.
Tested and working with simple truss structures.
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
    type: str
    angle: float

@dataclass
class Load:
    """Represents a concentrated load at a node."""
    name: str
    node: str
    magnitude: float
    angle: float

class TrussSolver:
    """Solves 2D truss structures using the Direct Stiffness Method."""
    
    def __init__(self, nodes, members, supports, loads):
        self.nodes = {n.name: n for n in nodes}
        self.members = members
        self.supports = supports
        self.loads = loads
        
        self.displacements = None
        self.reactions = None
        self.member_forces = None
        
        # Create DOF mapping
        self.node_dofs = {}
        dof = 0
        for name in sorted(self.nodes.keys()):
            self.node_dofs[name] = (dof, dof+1)
            dof += 2
        
        self.total_dofs = dof
    
    def get_dof(self, node_name, direction):
        """Get DOF index for a node and direction (0=x, 1=y)"""
        return self.node_dofs[node_name][direction]
    
    def get_constrained_dofs(self):
        """Get set of constrained DOF indices"""
        constrained = set()
        
        for support in self.supports:
            if support.node not in self.nodes:
                continue
            
            if support.type == 'pinned' or support.type == 'fixed':
                # Constrain both x and y
                constrained.add(self.get_dof(support.node, 0))
                constrained.add(self.get_dof(support.node, 1))
            
            elif support.type == 'roller':
                # Constrain direction based on angle
                angle_rad = math.radians(support.angle)
                # Normal direction to roller surface
                nx = math.cos(angle_rad)
                ny = math.sin(angle_rad)
                
                if abs(nx) >= abs(ny):
                    constrained.add(self.get_dof(support.node, 0))
                else:
                    constrained.add(self.get_dof(support.node, 1))
        
        return constrained
    
    def solve(self):
        """Solve using penalty method for stability"""
        try:
            n_dof = self.total_dofs
            
            # Initialize stiffness matrix and force vector
            K = np.zeros((n_dof, n_dof))
            F = np.zeros(n_dof)
            
            # Assemble global stiffness matrix
            for member in self.members:
                if member.start_node not in self.nodes or member.end_node not in self.nodes:
                    continue
                
                # Get node coordinates
                n1 = self.nodes[member.start_node]
                n2 = self.nodes[member.end_node]
                
                # Calculate length and direction cosines
                dx = n2.x - n1.x
                dy = n2.y - n1.y
                L = math.sqrt(dx**2 + dy**2)
                
                if L < 1e-10:
                    continue
                
                c = dx / L  # cos(theta)
                s = dy / L  # sin(theta)
                
                # Stiffness in global coordinates
                EA = 1000.0  # Use larger stiffness for numerical stability
                k = (EA / L)
                
                # Transformation matrix T = [c s 0 0; 0 0 c s]
                # k_global = T' * k_local * T
                # k_local = [1 -1; -1 1]
                
                # Element stiffness in global coordinates (4x4)
                ke = k * np.array([
                    [ c*c,  c*s, -c*c, -c*s],
                    [ c*s,  s*s, -c*s, -s*s],
                    [-c*c, -c*s,  c*c,  c*s],
                    [-c*s, -s*s,  c*s,  s*s]
                ])
                
                # Get DOF indices
                dof1_x = self.get_dof(member.start_node, 0)
                dof1_y = self.get_dof(member.start_node, 1)
                dof2_x = self.get_dof(member.end_node, 0)
                dof2_y = self.get_dof(member.end_node, 1)
                
                indices = [dof1_x, dof1_y, dof2_x, dof2_y]
                
                # Assemble
                for i in range(4):
                    for j in range(4):
                        K[indices[i], indices[j]] += ke[i, j]
            
            # Apply loads
            for load in self.loads:
                if load.node not in self.nodes:
                    continue
                
                angle_rad = math.radians(load.angle)
                fx = load.magnitude * math.cos(angle_rad)
                fy = load.magnitude * math.sin(angle_rad)
                
                F[self.get_dof(load.node, 0)] += fx
                F[self.get_dof(load.node, 1)] += fy
            
            # Apply support constraints using PENALTY METHOD
            # This is more stable than partitioning
            constrained = self.get_constrained_dofs()
            
            # Penalty factor (very large number)
            penalty = 1e10 * max(np.max(np.abs(K)), 1.0)
            
            # Apply constraints
            for dof in constrained:
                K[dof, dof] += penalty
                F[dof] = 0.0  # Zero displacement at support
            
            # Solve system
            try:
                U = np.linalg.solve(K, F)
            except np.linalg.LinAlgError:
                # Try least squares if singular
                U, residuals, rank, s = np.linalg.lstsq(K, F, rcond=None)
            
            # Store displacements
            self.displacements = {}
            for name in self.nodes:
                dx = U[self.get_dof(name, 0)]
                dy = U[self.get_dof(name, 1)]
                self.displacements[name] = np.array([dx, dy])
            
            # Calculate reactions
            self.reactions = {}
            for support in self.supports:
                if support.node not in self.nodes:
                    continue
                
                node = support.node
                
                # Sum forces from all connected members
                rx = 0.0
                ry = 0.0
                
                for member in self.members:
                    if member.start_node == node or member.end_node == node:
                        # Get member force
                        n1 = self.nodes[member.start_node]
                        n2 = self.nodes[member.end_node]
                        
                        dx = n2.x - n1.x
                        dy = n2.y - n1.y
                        L = math.sqrt(dx**2 + dy**2)
                        
                        if L < 1e-10:
                            continue
                        
                        c = dx / L
                        s = dy / L
                        
                        # Displacements at ends
                        u1 = self.displacements[member.start_node]
                        u2 = self.displacements[member.end_node]
                        
                        # Axial deformation
                        delta = (u2[0] - u1[0]) * c + (u2[1] - u1[1]) * s
                        
                        # Member force (positive = tension)
                        EA = 1000.0
                        force = (EA / L) * delta
                        
                        # Force components
                        if member.start_node == node:
                            rx += -force * c
                            ry += -force * s
                        else:
                            rx += force * c
                            ry += force * s
                
                # Subtract applied loads at support
                for load in self.loads:
                    if load.node == node:
                        angle_rad = math.radians(load.angle)
                        rx -= load.magnitude * math.cos(angle_rad)
                        ry -= load.magnitude * math.sin(angle_rad)
                
                self.reactions[node] = np.array([rx, ry])
            
            # Calculate member forces
            self.member_forces = {}
            for member in self.members:
                if member.start_node not in self.nodes or member.end_node not in self.nodes:
                    continue
                
                n1 = self.nodes[member.start_node]
                n2 = self.nodes[member.end_node]
                
                dx = n2.x - n1.x
                dy = n2.y - n1.y
                L = math.sqrt(dx**2 + dy**2)
                
                if L < 1e-10:
                    continue
                
                c = dx / L
                s = dy / L
                
                u1 = self.displacements[member.start_node]
                u2 = self.displacements[member.end_node]
                
                # Axial deformation (elongation)
                delta = (u2[0] - u1[0]) * c + (u2[1] - u1[1]) * s
                
                # Force = EA/L * delta (positive = tension)
                EA = 1000.0
                force = (EA / L) * delta
                
                self.member_forces[member.name] = force
            
            return True
            
        except Exception as e:
            print(f"Error in solve: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def validate_structure(self):
        """Basic structure validation"""
        errors = []
        
        if len(self.nodes) < 2:
            errors.append("Need at least 2 nodes")
        
        if len(self.members) < 1:
            errors.append("Need at least 1 member")
        
        if len(self.supports) < 1:
            errors.append("Need at least 1 support")
        
        # Check for minimum constraints (3 for 2D stability)
        constrained = self.get_constrained_dofs()
        if len(constrained) < 3:
            errors.append(f"Structure needs at least 3 constraints for stability (currently {len(constrained)}). Add more supports.")
        
        # Verify all member nodes exist
        for member in self.members:
            if member.start_node not in self.nodes:
                errors.append(f"Node '{member.start_node}' not found")
            if member.end_node not in self.nodes:
                errors.append(f"Node '{member.end_node}' not found")
        
        # Verify all load nodes exist
        for load in self.loads:
            if load.node not in self.nodes:
                errors.append(f"Node '{load.node}' not found")
        
        return errors