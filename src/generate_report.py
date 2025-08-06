
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

def generate_report():
    """
    Generates a comprehensive and corrected PDF report with plots of the calculated metrics.
    """
    try:
        metrics_df = pd.read_csv('data/metrics.csv')
    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure you have run the calculate_metrics script first.")
        return

    # --- Data Preparation ---
    metrics_df['activity_start_date'] = pd.to_datetime(metrics_df['activity_start_date'])
    metrics_df = metrics_df.sort_values(by='activity_start_date')
    metrics_df['activity_display_date'] = metrics_df['activity_start_date'].dt.strftime('%Y-%m-%d')

    # --- Plot Generation ---
    plot_filenames = []

    # Plot 1: Pace vs. HR Efficiency
    plt.figure(figsize=(11, 6))
    plt.plot(metrics_df['activity_display_date'], metrics_df['first_half_avg_speed_hr_efficiency'], marker='o', linestyle='--', label='First Half')
    plt.plot(metrics_df['activity_display_date'], metrics_df['second_half_avg_speed_hr_efficiency'], marker='o', linestyle='-', label='Second Half')
    plt.title('Pace vs. Heart Rate Efficiency (First vs. Second Half)')
    plt.xlabel('Date')
    plt.ylabel('Speed / Heart Rate')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    filename = 'reports/1_speed_hr_efficiency.png'
    plt.savefig(filename)
    plot_filenames.append(filename)
    plt.close()

    # Plot 2: Cardiac Drift
    plt.figure(figsize=(11, 6))
    plt.plot(metrics_df['activity_display_date'], metrics_df['cardiac_drift'], marker='o', color='r', label='Cardiac Drift')
    plt.axhline(y=1.05, color='gray', linestyle='--', label='Acceptable Drift Ceiling (1.05)') # A 5% drift is often considered a max
    plt.title('Cardiac Drift Over Time')
    plt.xlabel('Date')
    plt.ylabel('Cardiac Drift Ratio')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    filename = 'reports/2_cardiac_drift.png'
    plt.savefig(filename)
    plot_filenames.append(filename)
    plt.close()

    # Plot 3: Heart Rate Standard Deviation
    plt.figure(figsize=(11, 6))
    plt.plot(metrics_df['activity_display_date'], metrics_df['first_half_hr_std_dev'], marker='o', linestyle='--', label='First Half')
    plt.plot(metrics_df['activity_display_date'], metrics_df['second_half_hr_std_dev'], marker='o', linestyle='-', label='Second Half')
    plt.title('Heart Rate Stability (Standard Deviation)')
    plt.xlabel('Date')
    plt.ylabel('HR Standard Deviation (bpm)')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    filename = 'reports/3_hr_std_dev.png'
    plt.savefig(filename)
    plot_filenames.append(filename)
    plt.close()

    # Plot 4: Heart Rate Zone Distribution
    zone_cols = sorted([c for c in metrics_df.columns if 'zone_' in c and '_dist' in c])
    zone_data = metrics_df[['activity_display_date'] + zone_cols].set_index('activity_display_date')
    zone_data.columns = [c.replace('_dist', '').replace('zone_', 'Zone ').replace('_', ' ') for c in zone_data.columns]
    
    if not zone_data.empty:
        plt.figure(figsize=(12, 7))
        zone_data.plot(kind='bar', stacked=True, colormap='Spectral')
        plt.title('Heart Rate Zone Distribution per Activity')
        plt.xlabel('Activity Date')
        plt.ylabel('Percentage of Time in Zone')
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='HR Zones', bbox_to_anchor=(1.02, 1), loc='upper left')
        plt.tight_layout()
        filename = 'reports/4_hr_zones.png'
        plt.savefig(filename)
        plot_filenames.append(filename)
        plt.close()

    # --- PDF Generation ---
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Strava Performance Report', 0, 1, 'C')
    pdf.ln(10)

    # Add plots to PDF
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Pace & Efficiency Trends', 0, 1)
    pdf.image(plot_filenames[0], w=190)
    pdf.ln(5)
    pdf.image(plot_filenames[1], w=190)
    pdf.ln(5)

    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Heart Rate Stability & Zone Analysis', 0, 1)
    pdf.image(plot_filenames[2], w=190)
    pdf.ln(5)
    if len(plot_filenames) > 3:
        pdf.image(plot_filenames[3], w=190)

    pdf.output('reports/report.pdf', 'F')

    # Clean up image files
    for f in plot_filenames:
        os.remove(f)

    print("Successfully generated corrected report to reports/report.pdf")

if __name__ == '__main__':
    generate_report()
