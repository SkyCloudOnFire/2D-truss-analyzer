"""
PDF export module for 2D truss analysis.
Generates professional engineering report summaries.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import mm, cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, 
                               Table, TableStyle, Image, PageBreak)
from reportlab.graphics.shapes import Drawing
import matplotlib.pyplot as plt
from io import BytesIO
import datetime
from typing import Dict, List, Any
import plotly.io as pio

class PDFExporter:
    """Generates professional PDF reports for truss analysis."""
    
    def __init__(self, project_name: str = "2D Truss Analysis Report"):
        self.project_name = project_name
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles for the report."""
        self.custom_styles = {
            'Title': ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                spaceAfter=12,
                textColor=HexColor('#0F172A'),
                fontName='Helvetica-Bold'
            ),
            'Subtitle': ParagraphStyle(
                'Subtitle',
                parent=self.styles['Normal'],
                fontSize=12,
                textColor=HexColor('#64748B'),
                fontName='Helvetica'
            ),
            'SectionHeading': ParagraphStyle(
                'SectionHeading',
                parent=self.styles['Heading2'],
                fontSize=18,
                spaceBefore=20,
                spaceAfter=10,
                textColor=HexColor('#1E293B'),
                fontName='Helvetica-Bold',
                borderPadding=(0, 0, 1, 0),
                borderColor=HexColor('#E2E8F0'),
                borderWidth=1
            ),
            'TableCell': ParagraphStyle(
                'TableCell',
                parent=self.styles['Normal'],
                fontSize=10,
                fontName='Helvetica'
            ),
            'TableHeader': ParagraphStyle(
                'TableHeader',
                parent=self.styles['Normal'],
                fontSize=11,
                textColor=white,
                fontName='Helvetica-Bold'
            ),
            'ForcePositive': ParagraphStyle(
                'ForcePositive',
                parent=self.styles['Normal'],
                fontSize=10,
                textColor=HexColor('#3B82F6'),  # Blue for tension
                fontName='Helvetica-Bold'
            ),
            'ForceNegative': ParagraphStyle(
                'ForceNegative',
                parent=self.styles['Normal'],
                fontSize=10,
                textColor=HexColor('#EF4444'),  # Red for compression
                fontName='Helvetica-Bold'
            ),
            'Footer': ParagraphStyle(
                'Footer',
                parent=self.styles['Normal'],
                fontSize=8,
                textColor=HexColor('#94A3B8'),
                fontName='Helvetica'
            )
        }
    
    def create_report(self, input_data: Dict, results: Dict, 
                     preview_fig, result_fig, unit: str = 'N') -> BytesIO:
        """
        Create a complete PDF report.
        
        Args:
            input_data: Dictionary containing nodes, members, supports, loads
            results: Dictionary containing reactions and member forces
            preview_fig: Matplotlib figure for preview
            result_fig: Matplotlib figure for results
            unit: Unit system used
        
        Returns:
            BytesIO buffer containing the PDF
        """
        buffer = BytesIO()
        
        # Create document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Build story (content elements)
        story = []
        
        # Header
        story.append(Paragraph(self.project_name, self.custom_styles['Title']))
        story.append(Paragraph(
            f"Generated on {datetime.datetime.now().strftime('%B %d, %Y at %H:%M')}",
            self.custom_styles['Subtitle']
        ))
        story.append(Spacer(1, 20))
        
        # Project Information
        story.append(Paragraph('Project Information', self.custom_styles['SectionHeading']))
        info_data = [
            ['Total Nodes', str(len(input_data.get('nodes', [])))],
            ['Total Members', str(len(input_data.get('members', [])))],
            ['Total Supports', str(len(input_data.get('supports', [])))],
            ['Total Loads', str(len(input_data.get('loads', [])))],
            ['Unit System', unit],
            ['Analysis Method', 'Direct Stiffness Method']
        ]
        info_table = Table(info_data, colWidths=[200, 200])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), HexColor('#F1F5F9')),
            ('TEXTCOLOR', (0, 0), (-1, -1), HexColor('#0F172A')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#E2E8F0')),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Input Data Summary
        story.append(Paragraph('Input Data Summary', self.custom_styles['SectionHeading']))
        
        # Nodes table
        story.append(Paragraph('Nodes', self.custom_styles['SectionHeading'].clone('NodesSub')))
        if input_data.get('nodes'):
            nodes_data = [['Name', 'X Coordinate', 'Y Coordinate']]
            for node in input_data['nodes']:
                nodes_data.append([node.name, f"{node.x:.2f}", f"{node.y:.2f}"])
            
            nodes_table = Table(nodes_data, colWidths=[133, 133, 133])
            nodes_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#3B82F6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#E2E8F0')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#F8FAFC')])
            ]))
            story.append(nodes_table)
        
        story.append(Spacer(1, 20))
        
        # Truss Preview Image
        story.append(Paragraph('Structure Preview', self.custom_styles['SectionHeading']))
        if preview_fig:
            img_buffer = BytesIO()
            preview_fig.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            img = Image(img_buffer, width=450, height=350)
            story.append(img)
        
        story.append(PageBreak())
        
        # Analysis Results
        story.append(Paragraph('Analysis Results', self.custom_styles['SectionHeading']))
        
        # Reaction Forces
        story.append(Paragraph('Reaction Forces', self.custom_styles['SectionHeading']))
        if results.get('reactions'):
            reactions_data = [['Support Node', 'Fx', 'Fy', 'Resultant', 'Angle (°)']]
            for node_name, reaction in results['reactions'].items():
                magnitude = (reaction[0]**2 + reaction[1]**2)**0.5
                angle = 0
                if magnitude > 1e-10:
                    import math
                    angle = math.degrees(math.atan2(reaction[1], reaction[0]))
                reactions_data.append([
                    node_name,
                    f"{reaction[0]:.2f} {unit}",
                    f"{reaction[1]:.2f} {unit}",
                    f"{magnitude:.2f} {unit}",
                    f"{angle:.1f}°"
                ])
            
            reactions_table = Table(reactions_data, colWidths=[80, 80, 80, 80, 80])
            reactions_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#10B981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#E2E8F0')),
            ]))
            story.append(reactions_table)
        
        story.append(Spacer(1, 20))
        
        # Member Forces
        story.append(Paragraph('Member Forces', self.custom_styles['SectionHeading']))
        if results.get('member_forces'):
            members_data = [['Member', 'Force', 'Type']]
            for member_name, force in results['member_forces'].items():
                force_type = 'TENSION' if force > 0 else 'COMPRESSION' if force < 0 else 'ZERO'
                members_data.append([
                    member_name,
                    f"{abs(force):.2f} {unit}",
                    force_type
                ])
            
            members_table = Table(members_data, colWidths=[133, 133, 133])
            members_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#3B82F6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#E2E8F0')),
            ]))
            
            # Color code forces
            for i in range(1, len(members_data)):
                force_type = members_data[i][2]
                if force_type == 'TENSION':
                    members_table.setStyle(TableStyle([
                        ('TEXTCOLOR', (1, i), (1, i), HexColor('#3B82F6')),
                    ]))
                elif force_type == 'COMPRESSION':
                    members_table.setStyle(TableStyle([
                        ('TEXTCOLOR', (1, i), (1, i), HexColor('#EF4444')),
                    ]))
            
            story.append(members_table)
        
        story.append(PageBreak())
        
        # Result Visualization
        story.append(Paragraph('Result Visualization', self.custom_styles['SectionHeading']))
        if result_fig:
            img_buffer = BytesIO()
            result_fig.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            img = Image(img_buffer, width=450, height=350)
            story.append(img)
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph(
            "This report was generated automatically by the 2D Truss Analysis System. "
            "Results should be verified by a qualified engineer before use in design.",
            self.custom_styles['Footer']
        ))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer