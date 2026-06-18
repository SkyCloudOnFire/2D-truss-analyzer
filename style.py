"""
Theme and styling management for 2D Truss Analysis System.
Provides modern SaaS dashboard styling with light/dark theme support.
"""

import streamlit as st
from typing import Literal

# Color palettes
class ThemeColors:
    """Professional color palettes for light and dark themes."""
    
    LIGHT = {
        'bg_primary': '#FFFFFF',
        'bg_secondary': '#F8FAFC',
        'bg_card': '#FFFFFF',
        'text_primary': '#0F172A',
        'text_secondary': '#475569',
        'border': '#E2E8F0',
        'accent': '#3B82F6',
        'accent_hover': '#2563EB',
        'success': '#10B981',
        'warning': '#F59E0B',
        'error': '#EF4444',
        'tension': '#3B82F6',  # Blue for tension
        'compression': '#EF4444',  # Red for compression
        'shadow': '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
        'card_shadow': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    }
    
    DARK = {
        'bg_primary': '#0F172A',
        'bg_secondary': '#1E293B',
        'bg_card': '#1E293B',
        'text_primary': '#F1F5F9',
        'text_secondary': '#94A3B8',
        'border': '#334155',
        'accent': '#60A5FA',
        'accent_hover': '#3B82F6',
        'success': '#34D399',
        'warning': '#FBBF24',
        'error': '#F87171',
        'tension': '#60A5FA',
        'compression': '#F87171',
        'shadow': '0 1px 3px 0 rgba(0, 0, 0, 0.3)',
        'card_shadow': '0 1px 2px 0 rgba(0, 0, 0, 0.2)',
    }

def get_css(theme: Literal['light', 'dark']) -> str:
    """
    Generate CSS styles based on selected theme.
    
    Args:
        theme: 'light' or 'dark'
    
    Returns:
        CSS string for the selected theme
    """
    colors = ThemeColors.LIGHT if theme == 'light' else ThemeColors.DARK
    
    return f"""
    <style>
        /* Global Styles */
        .stApp {{
            background-color: {colors['bg_primary']};
        }}
        
        .main .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }}
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            color: {colors['text_primary']};
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-weight: 600;
            letter-spacing: -0.02em;
        }}
        
        p, label, div {{
            color: {colors['text_secondary']};
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        
        /* Card Styles */
        .card {{
            background-color: {colors['bg_card']};
            border: 1px solid {colors['border']};
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: {colors['card_shadow']};
            transition: all 0.2s ease;
        }}
        
        .card:hover {{
            box-shadow: {colors['shadow']};
        }}
        
        /* Button Styles */
        .stButton > button {{
            border-radius: 8px;
            font-weight: 500;
            font-size: 0.875rem;
            padding: 0.5rem 1rem;
            transition: all 0.2s ease;
            border: 1px solid {colors['border']};
            background-color: {colors['bg_card']};
            color: {colors['text_primary']};
        }}
        
        .stButton > button:hover {{
            border-color: {colors['accent']};
            color: {colors['accent']};
        }}
        
        .stButton > button:active {{
            transform: scale(0.98);
        }}
        
        /* Primary Button */
        .primary-button > button {{
            background-color: {colors['accent']};
            color: white;
            border: none;
            font-weight: 600;
        }}
        
        .primary-button > button:hover {{
            background-color: {colors['accent_hover']};
            color: white;
        }}
        
        /* Input Fields */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div {{
            background-color: {colors['bg_card']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            color: {colors['text_primary']};
        }}
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {{
            border-color: {colors['accent']};
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }}
        
        /* Data Table */
        .dataframe {{
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid {colors['border']};
        }}
        
        /* Tab Styles */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.5rem;
            background-color: {colors['bg_secondary']};
            border-radius: 10px;
            padding: 0.25rem;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {colors['accent']};
            color: white;
        }}
        
        /* Metric Cards */
        .metric-card {{
            background: linear-gradient(135deg, {colors['bg_card']} 0%, {colors['bg_secondary']} 100%);
            border: 1px solid {colors['border']};
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
        }}
        
        .metric-value {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {colors['text_primary']};
        }}
        
        .metric-label {{
            font-size: 0.75rem;
            color: {colors['text_secondary']};
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {colors['bg_secondary']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {colors['border']};
            border-radius: 3px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {colors['text_secondary']};
        }}
    </style>
    """