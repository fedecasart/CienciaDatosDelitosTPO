"""
Module containing reusable plotting functions to maintain visual consistency
across notebooks, reports, and presentation materials.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Define a cohesive academic color palette (e.g., deep blues and neutrals)
ACADEMIC_PALETTE = ["#1a436d", "#337ab7", "#e74c3c", "#f39c12", "#2ecc71", "#7f8c8d"]

def set_academic_style():
    """
    Sets default parameters for matplotlib and seaborn to output
    clean, consistent, high-DPI figures suitable for publications.
    """
    plt.style.use('ggplot')
    sns.set_theme(style="whitegrid", context="paper")
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['DejaVu Sans', 'Arial', 'Liberation Sans'],
        'figure.autolayout': True
    })

def plot_hourly_heatmap(df: pd.DataFrame, save_path: str = None) -> plt.Figure:
    """
    Creates a heatmap demonstrating the density of incidents by hour of day
    and day of the week. Useful for identifying temporal hot spots.
    """
    set_academic_style()
    
    # Check if necessary fields exist in df
    if 'hour' not in df.columns or 'day_of_week' not in df.columns:
        print("Dataframe must contain 'hour' and 'day_of_week' columns.")
        return None
    
    # Sort order of days of the week
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    pivot_df = pd.crosstab(df['hour'], df['day_of_week'])
    # Reorder columns to standard week
    existing_days = [d for d in days_order if d in pivot_df.columns]
    pivot_df = pivot_df[existing_days]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(
        pivot_df, 
        cmap="YlOrRd", 
        annot=False, 
        cbar_kws={'label': 'Incident count'}, 
        ax=ax
    )
    
    ax.set_title("Crime Density by Day & Hour", fontsize=16, pad=15)
    ax.set_xlabel("Day of Week", fontsize=12)
    ax.set_ylabel("Hour of Day", fontsize=12)
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Heatmap saved to: {save_path}")
        
    return fig

def plot_top_categories(df: pd.DataFrame, cat_column: str, top_n: int = 10, save_path: str = None) -> plt.Figure:
    """
    Plots a horizontal bar chart displaying the frequency of the top N
    categories for a specific variable (e.g., crime types, location description).
    """
    set_academic_style()
    
    if cat_column not in df.columns:
        print(f"Column '{cat_column}' not found in DataFrame.")
        return None
        
    counts = df[cat_column].value_counts().head(top_n)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        x=counts.values, 
        y=counts.index, 
        palette=sns.color_palette("Blues_d", n_colors=top_n), 
        ax=ax
    )
    
    ax.set_title(f"Top {top_n} Categories: {cat_column.replace('_', ' ').title()}", fontsize=16, pad=15)
    ax.set_xlabel("Count of Incidents", fontsize=12)
    ax.set_ylabel("Category", fontsize=12)
    
    # Add count labels to the ends of the bars
    for i, v in enumerate(counts.values):
        ax.text(v + (max(counts.values) * 0.01), i, f" {v:,}", va='center', fontsize=10)
        
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Bar plot saved to: {save_path}")
        
    return fig
