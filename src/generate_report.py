import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

def generate_report():
    """
    Generates a PDF report with metrics and plots segmented by activity type,
    with cleaned titles and specific ordering.
    """
    try:
        metrics_df = pd.read_csv('data/metrics.csv')
    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure you have run the calculate_metrics script first.")
        return

    # --- Data Preparation ---
    metrics_df['activity_start_date'] = pd.to_datetime(metrics_df['activity_start_date']).dt.tz_convert('US/Central')
    metrics_df = metrics_df.sort_values(by='activity_start_date')

    # --- PDF Generation ---
    pdf = FPDF()
    
    # Get unique activity types and sort them
    # Clean the activity type strings as they are read from CSV
    metrics_df['activity_type'] = metrics_df['activity_type'].apply(lambda x: str(x).replace("root=", "").strip("'"))
    
    activity_types = metrics_df['activity_type'].unique().tolist()
    
    # Custom sort order: Run, then Ride, then others alphabetically
    custom_order = ['Run', 'Ride']
    sorted_activity_types = []
    for atype in custom_order:
        if atype in activity_types:
            sorted_activity_types.append(atype)
            activity_types.remove(atype)
    sorted_activity_types.extend(sorted(activity_types))

    for activity_type in sorted_activity_types:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 20)
        # Use the already cleaned activity_type for display
        display_activity_type = activity_type
        pdf.cell(0, 10, f'{display_activity_type} Performance Report', 0, 1, 'C')
        pdf.ln(10)

        activity_df = metrics_df[metrics_df['activity_type'] == activity_type].copy()
        activity_df['activity_display_date'] = activity_df['activity_start_date'].dt.strftime('%Y-%m-%d')
        
        plot_filenames = []

        # --- Plot Generation for each activity type ---
        # Plot 1: Efficiency Factor
        plt.figure(figsize=(11, 6))
        plt.plot(activity_df['activity_display_date'], activity_df['first_half_avg_efficiency_factor'], marker='o', linestyle='--', label='First Half')
        plt.plot(activity_df['activity_display_date'], activity_df['second_half_avg_efficiency_factor'], marker='o', linestyle='-', label='Second Half')
        plt.title(f'{display_activity_type} - Efficiency Factor')
        plt.xlabel('Date'); plt.ylabel('Efficiency Factor'); plt.xticks(rotation=45, ha='right'); plt.grid(True); plt.legend(); plt.tight_layout()
        filename = f'reports/{display_activity_type}_1.png'
        plt.savefig(filename); plot_filenames.append(filename); plt.close()

        # Plot 2: Cardiac Drift
        plt.figure(figsize=(11, 6))
        plt.plot(activity_df['activity_display_date'], activity_df['cardiac_drift'], marker='o', color='r', label='Cardiac Drift')
        plt.axhline(y=5, color='gray', linestyle='--', label='Acceptable Drift Ceiling (5%)')
        plt.title(f'{display_activity_type} - Cardiac Drift'); plt.xlabel('Date'); plt.ylabel('Cardiac Drift Ratio'); plt.xticks(rotation=45, ha='right'); plt.grid(True); plt.legend(); plt.tight_layout()
        filename = f'reports/{display_activity_type}_2.png'
        plt.savefig(filename); plot_filenames.append(filename); plt.close()

        # Plot 3: Heart Rate Standard Deviation
        plt.figure(figsize=(11, 6))
        plt.plot(activity_df['activity_display_date'], activity_df['first_half_hr_std_dev'], marker='o', linestyle='--', label='First Half')
        plt.plot(activity_df['activity_display_date'], activity_df['second_half_hr_std_dev'], marker='o', linestyle='-', label='Second Half')
        plt.title(f'{display_activity_type} - HR Stability'); plt.xlabel('Date'); plt.ylabel('HR Standard Deviation (bpm)'); plt.xticks(rotation=45, ha='right'); plt.grid(True); plt.legend(); plt.tight_layout()
        filename = f'reports/{display_activity_type}_3.png'
        plt.savefig(filename); plot_filenames.append(filename); plt.close()

        # Plot 4: Weekly Time in Zone 2
        zone_2_col = 'zone_time_Zone_2_60-70'
        if zone_2_col in activity_df.columns:
            activity_df['zone_2_time_minutes'] = activity_df[zone_2_col] / 60
            weekly_zone2_time = activity_df.resample('W-Mon', on='activity_start_date')['zone_2_time_minutes'].sum()
            if not weekly_zone2_time.empty:
                plt.figure(figsize=(11, 6)); weekly_zone2_time.plot(kind='bar', colormap='viridis'); plt.title(f'{display_activity_type} - Weekly Time in Zone 2'); plt.xlabel('Week'); plt.ylabel('Time in Zone 2 (minutes)'); plt.xticks(rotation=45, ha='right'); plt.tight_layout()
                filename = f'reports/{display_activity_type}_4.png'
                plt.savefig(filename); plot_filenames.append(filename); plt.close()

        # Plot 5: Per-Activity Heart Rate Zone Distribution
        zone_time_cols = sorted([c for c in activity_df.columns if 'zone_time' in c])
        zone_time_data = activity_df[['activity_display_date'] + zone_time_cols].set_index('activity_display_date')
        zone_dist_data = zone_time_data.div(zone_time_data.sum(axis=1), axis=0)
        zone_dist_data.columns = [c.replace('zone_time_', '').replace('_', ' ') for c in zone_dist_data.columns]
        if not zone_dist_data.empty:
            plt.figure(figsize=(12, 7)); zone_dist_data.plot(kind='bar', stacked=True, colormap='Spectral'); plt.title(f'{display_activity_type} - HR Zone Distribution'); plt.xlabel('Activity Date'); plt.ylabel('Percentage of Time'); plt.xticks(rotation=45, ha='right'); plt.legend(title='HR Zones', bbox_to_anchor=(1.02, 1), loc='upper left'); plt.tight_layout()
            filename = f'reports/{display_activity_type}_5.png'
            plt.savefig(filename); plot_filenames.append(filename); plt.close()

        # --- Add plots to this section of the PDF ---
        for i, f in enumerate(plot_filenames):
            if i % 2 == 0 and i > 0:
                pdf.add_page()
            pdf.image(f, w=190)
            pdf.ln(5)
            os.remove(f)

    pdf.output('reports/report.pdf', 'F')
    print("Successfully generated segmented report to reports/report.pdf")

if __name__ == '__main__':
    generate_report()