import pandas as pd
import numpy as np

def get_zone(hr, max_hr):
    if not pd.notna(hr):
        return None
    if hr < 0.6 * max_hr:
        return 'Zone 1 (50-60%)'
    elif hr < 0.725 * max_hr:
        return 'Zone 2 (60-72.5%)'
    elif hr < 0.8 * max_hr:
        return 'Zone 3 (72.5-80%)'
    elif hr < 0.9 * max_hr:
        return 'Zone 4 (80-90%)'
    else:
        return 'Zone 5 (90-100%)'

def calculate_cardiac_drift(first_half, second_half):
    hr_first_half_avg = first_half['heartrate'].mean()
    hr_second_half_avg = second_half['heartrate'].mean()
    speed_first_half_avg = first_half['velocity_smooth'].mean()
    speed_second_half_avg = second_half['velocity_smooth'].mean()

    if hr_first_half_avg > 0 and speed_first_half_avg > 0 and speed_second_half_avg > 0:
        drift_ratio = (hr_second_half_avg / hr_first_half_avg) / (speed_first_half_avg / speed_second_half_avg)
        return (drift_ratio - 1) * 100  # % drift
    return np.nan

def calculate_zone_metrics(activity_streams, max_hr):
    activity_streams['hr_zone'] = activity_streams['heartrate'].apply(get_zone, max_hr=max_hr)
    zone_time = activity_streams['hr_zone'].value_counts().to_dict()
    activity_streams['zone_shifted'] = activity_streams['hr_zone'].shift() != activity_streams['hr_zone']
    zone_transitions = activity_streams['zone_shifted'].sum()
    return zone_time, zone_transitions

def calculate_split_metrics(split_df):
    if split_df.empty:
        return {'avg_efficiency_factor': np.nan, 'hr_std_dev': np.nan}
    split_df_filtered = split_df[(split_df['heartrate'] > 0) & (split_df['velocity_smooth'] > 0)]
    if split_df_filtered.empty:
        return {'avg_efficiency_factor': np.nan, 'hr_std_dev': np.nan}
    split_df_filtered['efficiency_factor'] = split_df_filtered['velocity_smooth'] / (split_df_filtered['heartrate'] / 197)
    return {
        'avg_efficiency_factor': split_df_filtered['efficiency_factor'].mean(),
        'hr_std_dev': split_df_filtered['heartrate'].std()
    }

def calculate_metrics():
    """
    Calculates advanced performance metrics and includes activity type.
    """
    try:
        activities_df = pd.read_csv('data/activities.csv')
        streams_df = pd.read_csv('data/streams.csv')
    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure you have run the fetch scripts first.")
        return

    user_age = 23
    max_hr = 220 - user_age

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

        first_half = activity_streams.iloc[:len(activity_streams)//2]
        second_half = activity_streams.iloc[len(activity_streams)//2:]

        if first_half.empty or second_half.empty:
            continue

        cardiac_drift = calculate_cardiac_drift(first_half, second_half)
        zone_time, zone_transitions = calculate_zone_metrics(activity_streams, max_hr)
        first_half_metrics = calculate_split_metrics(first_half)
        second_half_metrics = calculate_split_metrics(second_half)

        metrics_data.append({
            'activity_id': activity_id,
            'activity_name': activity_details['name'],
            'activity_type': activity_details['type'],
            'activity_start_date': activity_details['start_date'],
            'is_long_run': activity_details['elapsed_time'] > 3600,
            'cardiac_drift': cardiac_drift,
            'zone_transitions': zone_transitions,
            **{f'zone_time_{k.replace(" ", "_").replace("(", "").replace(")", "").replace("%", "")}': v for k, v in zone_time.items()},
            **{f'first_half_{k}': v for k, v in first_half_metrics.items()},
            **{f'second_half_{k}': v for k, v in second_half_metrics.items()}
        })

    if metrics_data:
        metrics_df = pd.DataFrame(metrics_data)
        all_zone_keys = [
            ("Zone 1 (50-60%)", 0.50, 0.60),
            ("Zone 2 (60-72.5%)", 0.60, 0.725),
            ("Zone 3 (72.5-80%)", 0.725, 0.80),
            ("Zone 4 (80-90%)", 0.80, 0.90),
            ("Zone 5 (90-100%)", 0.90, 1.00)
        ]
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