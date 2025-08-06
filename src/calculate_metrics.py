
import pandas as pd
import numpy as np

def calculate_metrics():
    """
    Calculates advanced performance metrics from the raw activity and stream data.
    """
    try:
        activities_df = pd.read_csv('data/activities.csv')
        streams_df = pd.read_csv('data/streams.csv')
    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure you have run the fetch scripts first.")
        return

    # User-defined settings
    user_age = 23
    max_hr = 220 - user_age

    def get_zone(hr):
        if not pd.notna(hr):
            return None
        if hr < 0.6 * max_hr:
            return 'Zone 1 (50-60%)'
        elif hr < 0.7 * max_hr:
            return 'Zone 2 (60-70%)'
        elif hr < 0.8 * max_hr:
            return 'Zone 3 (70-80%)'
        elif hr < 0.9 * max_hr:
            return 'Zone 4 (80-90%)'
        else:
            return 'Zone 5 (90-100%)'

    activities_with_hr = streams_df[streams_df['heartrate'].notna()]['activity_id'].unique()
    
    metrics_data = []

    for activity_id in activities_with_hr:
        print(f"Calculating metrics for activity {activity_id}")
        
        activity_streams = streams_df[streams_df['activity_id'] == activity_id].copy()
        activity_details = activities_df[activities_df['id'] == activity_id].iloc[0]

        activity_streams = activity_streams[activity_streams['moving']]
        activity_streams = activity_streams[activity_streams['heartrate'] > 0]

        if activity_streams.empty:
            continue

        # --- Run Splitting ---
        first_half = activity_streams.iloc[:len(activity_streams)//2]
        second_half = activity_streams.iloc[len(activity_streams)//2:]

        if first_half.empty or second_half.empty:
            continue

        # --- Metric Calculations ---
        # Cardiac Drift
        hr_first_half_avg = first_half['heartrate'].mean()
        hr_second_half_avg = second_half['heartrate'].mean()
        # Use velocity_smooth, convert to pace (s/m)
        pace_first_half_avg = (1 / first_half['velocity_smooth'].mean()) if first_half['velocity_smooth'].mean() > 0 else 0
        pace_second_half_avg = (1 / second_half['velocity_smooth'].mean()) if second_half['velocity_smooth'].mean() > 0 else 0

        if hr_first_half_avg > 0 and pace_first_half_avg > 0 and pace_second_half_avg > 0:
            cardiac_drift = (hr_second_half_avg / hr_first_half_avg) / (pace_first_half_avg / pace_second_half_avg) # Inverted pace ratio for correct drift
        else:
            cardiac_drift = np.nan

        # Heart Rate Zone Analysis
        activity_streams['hr_zone'] = activity_streams['heartrate'].apply(get_zone)
        zone_distribution = activity_streams['hr_zone'].value_counts(normalize=True).to_dict()

        # Zone Transitions
        activity_streams['zone_shifted'] = activity_streams['hr_zone'].shift() != activity_streams['hr_zone']
        zone_transitions = activity_streams['zone_shifted'].sum()

        # Split-based metrics function
        def calculate_split_metrics(split_df):
            if split_df.empty:
                return {'avg_speed_hr_efficiency': np.nan, 'hr_std_dev': np.nan}
            
            split_df_filtered = split_df[(split_df['heartrate'] > 0) & (split_df['velocity_smooth'] > 0)]

            if split_df_filtered.empty:
                return {'avg_speed_hr_efficiency': np.nan, 'hr_std_dev': np.nan}

            split_df_filtered['speed_hr_efficiency'] = split_df_filtered['velocity_smooth'] / split_df_filtered['heartrate']
            return {
                'avg_speed_hr_efficiency': split_df_filtered['speed_hr_efficiency'].mean(),
                'hr_std_dev': split_df_filtered['heartrate'].std()
            }

        first_half_metrics = calculate_split_metrics(first_half)
        second_half_metrics = calculate_split_metrics(second_half)

        metrics_data.append({
            'activity_id': activity_id,
            'activity_name': activity_details['name'],
            'activity_start_date': activity_details['start_date'],
            'cardiac_drift': cardiac_drift,
            'zone_transitions': zone_transitions,
            **{f'zone_{k.replace(" ", "_").replace("(", "").replace(")", "").replace("%", "")}_dist': v for k, v in zone_distribution.items()},
            **{f'first_half_{k}': v for k, v in first_half_metrics.items()},
            **{f'second_half_{k}': v for k, v in second_half_metrics.items()}
        })

    if metrics_data:
        metrics_df = pd.DataFrame(metrics_data)
        # Fill NaN for missing zones to ensure consistent columns
        all_zone_keys = [f'zone_Zone_{i}_{p1}-{p2}_dist' for i, (p1, p2) in enumerate([(50,60),(60,70),(70,80),(80,90),(90,100)], 1)]
        for key in all_zone_keys:
            if key not in metrics_df.columns:
                metrics_df[key] = 0
        metrics_df.fillna(0, inplace=True)
        metrics_df.to_csv('data/metrics.csv', index=False)
        print("Successfully calculated and saved advanced metrics to data/metrics.csv")
    else:
        print("No activities with heartrate data found to calculate metrics.")

if __name__ == '__main__':
    calculate_metrics()
