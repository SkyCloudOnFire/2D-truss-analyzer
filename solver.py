"""
Direct Stiffness Method solver for 2D truss analysis.
Handles statically determinate and indeterminate structures.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import math

@dataclass
class Node:
    name: str
    x: float
    y: float

@dataclass
class Member:
    name: str
    start_node: str
    end_node: str

@dataclass
class Support:
    node: str
    type: str
    angle: float

@dataclass
class Load:
    name: str
    node: str
    magnitude: float
    angle: float

class TrussSolver:
    """Solves 2D truss structures using Direct Stiffness Method."""
    
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
        """Get DOF index (0=x, 1=y)"""
        return self.node_dofs[node_name][direction]
    
    def get_constrained_dofs(self):
        """Get list of constrained DOF indices"""
        constrained = []
        
        for support in self.supports:
            if support.node not in self.nodes:
                continue
            
            if support.type == 'pinned' or support.type == 'fixed':
                constrained.append(self.get_dof(support.node, 0))
                constrained.append(self.get_dof(support.node, 1))
            
            elif support.type == 'roller':
                angle_rad = math.radians(support.angle)
                nx = math.cos(angle_rad)
                ny = math.sin(angle_rad)
                
                if abs(nx) >= abs(ny):
                    constrained.append(self.get_dof(support.node, 0))
                else:
                    constrained.append(self.get_dof(support.node, 1))
        
        return sorted(set(constrained))
    
    def solve(self):
        """Solve using penalty method"""
        try:
            n_dof = self.total_dofs
            K = np.zeros((n_dof, n_dof))
            F = np.zeros(n_dof)
            
            # Use a consistent EA value
            EA = 1.0
            
            # Assemble global stiffness matrix
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
                
                k = EA / L
                
                # Element stiffness matrix (4x4)
                ke = k * np.array([
                    [ c*c,  c*s, -c*c, -c*s],
                    [ c*s,  s*s, -c*s, -s*s],
                    [-c*c, -c*s,  c*c,  c*s],
                    [-c*s, -s*s,  c*s,  s*s]
                ])
                
                dof1 = [self.get_dof(member.start_node, 0), 
                       self.get_dof(member.start_node, 1)]
                dof2 = [self.get_dof(member.end_node, 0), 
                       self.get_dof(member.end_node, 1)]
                indices = dof1 + dof2
                
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
            
            # Apply constraints with penalty method
            constrained = self.get_constrained_dofs()
            
            # Calculate penalty factor
            max_K = max(1.0, np.max(np.abs(K)))
            penalty = 1e8 * max_K
            
            # Apply penalty
            K_mod = K.copy()
            F_mod = F.copy()
            
            for dof in constrained:
                K_mod[dof, dof] += penalty
                F_mod[dof] = 0.0
            
            # Solve
            U = np.linalg.solve(K_mod, F_mod)
            
            # Store displacements
            self.displacements = {}
            for name in self.nodes:
                dx = U[self.get_dof(name, 0)]
                dy = U[self.get_dof(name, 1)]
                self.displacements[name] = np.array([dx, dy])
            
            # Calculate reactions using EQUILIBRIUM method
            # This is more reliable than stiffness-based reactions
            self.reactions = {}
            
            # Initialize reactions to zero
            for support in self.supports:
                if support.node in self.nodes:
                    self.reactions[support.node] = np.array([0.0, 0.0])
            
            # Sum forces from members at each support
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
                
                # Elongation
                delta = (u2[0] - u1[0]) * c + (u2[1] - u1[1]) * s
                
                # Member force (positive = tension)
                force = (EA / L) * delta
                
                # Force components acting ON the nodes
                # On start node: force pulls towards end node
                # On end node: force pulls towards start node
                fx_start = force * c
                fy_start = force * s
                fx_end = -force * c
                fy_end = -force * s
                
                # Add to reactions if node is supported
                if member.start_node in self.reactions:
                    self.reactions[member.start_node][0] += fx_start
                    self.reactions[member.start_node][1] += fy_start
                
                if member.end_node in self.reactions:
                    self.reactions[member.end_node][0] += fx_end
                    self.reactions[member.end_node][1] += fy_end
            
            # Subtract any applied loads at support nodes
            for load in self.loads:
                if load.node in self.reactions:
                    angle_rad = math.radians(load.angle)
                    fx = load.magnitude * math.cos(angle_rad)
                    fy = load.magnitude * math.sin(angle_rad)
                    self.reactions[load.node][0] -= fx
                    self.reactions[load.node][1] -= fy
            
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
                
                delta = (u2[0] - u1[0]) * c + (u2[1] - u1[1]) * s
                force = (EA / L) * delta
                
                self.member_forces[member.name] = force
            
            return True
            
        except Exception as e:
            print(f"Error in solve: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def validate_structure(self):
        """Validate structure"""
        errors = []
        
        if len(self.nodes) < 2:
            errors.append("Need at least 2 nodes")
        
        if len(self.members) < 1:
            errors.append("Need at least 1 member")
        
        if len(self.supports) < 1:
            errors.append("Need at least 1 support")
        
        constrained = self.get_constrained_dofs()
        if len(constrained) < 3:
            errors.append(f"Need at least 3 constraints (currently {len(constrained)}). Add more supports.")
        
        for member in self.members:
            if member.start_node not in self.nodes:
                errors.append(f"Node '{member.start_node}' not found")
            if member.end_node not in self.nodes:
                errors.append(f"Node '{member.end_node}' not found")
        
        for load in self.loads:
            if load.node not in self.nodes:
                errors.append(f"Node '{load.node}' not found")
        
        return errors