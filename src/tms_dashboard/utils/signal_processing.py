import numpy as np


def apply_baseline(baseline_start_ms, baseline_end_ms, signal_start_ms, signal_end_ms, data, sampling_rate):
    """
    Applies a correction on a signal baseline.
    
    Args:
        baseline_start_ms: Baseline interval start in milliseconds (ex: -50)
        baseline_end_ms: Baseline interval end in milliseconds, exclusive (ex: -10)
        signal_start_ms: Start of the whole signal in milliseconds (ex: -50)
        signal_end_ms: End of the whole signal in milliseconds (ex: 40)
        data: Array containing signal data
        sampling_rate: Sampling rate in Hz
        
    Returns:
        Array with corrected baseline
    """
    signal = np.asarray(data, dtype=float)
    if signal.ndim != 1 or signal.size == 0:
        raise ValueError('Baseline correction requires a non-empty one-dimensional signal.')
    if not np.isfinite(sampling_rate) or sampling_rate <= 0:
        raise ValueError('Sampling rate must be positive and finite.')
    if not signal_start_ms <= baseline_start_ms < baseline_end_ms <= signal_end_ms:
        raise ValueError(
            f'Baseline [{baseline_start_ms}, {baseline_end_ms}) ms must fit '
            f'inside the signal window [{signal_start_ms}, {signal_end_ms}) ms.'
        )

    baseline_start_idx = int(round((baseline_start_ms - signal_start_ms) * sampling_rate / 1000))
    baseline_end_idx = int(round((baseline_end_ms - signal_start_ms) * sampling_rate / 1000))
    if not 0 <= baseline_start_idx < baseline_end_idx <= signal.size:
        raise ValueError('The signal does not contain all samples required for the baseline interval.')

    mean_baseline = np.mean(signal[baseline_start_idx:baseline_end_idx])
    return signal - mean_baseline


def set_apply_baseline_all(baseline_start_ms, baseline_end_ms, signal_start_ms, signal_end_ms, data_windows, sampling_rate):
    """
    Applies baseline in all data windows.
    
    Args:
        baseline_start_ms: Baseline interval start in milliseconds
        baseline_end_ms: Baseline interval end in milliseconds
        signal_start_ms: Start of the whole signal in milliseconds
        signal_end_ms: End of the whole signal in milliseconds
        data_windows: Arrays list containing data windows
        sampling_rate: Sampling rate in Hz
        
    Returns:
        Arrays list containing baseline-corrected data windows
    """
    processed_data = []
    for window in data_windows:
        corrected = apply_baseline(
            baseline_start_ms, 
            baseline_end_ms, 
            signal_start_ms, 
            signal_end_ms, 
            window, 
            sampling_rate
        )
        processed_data.append(corrected)
    return processed_data

def new_indexes_fast_tol(A, B, decimals=5):
    """
    Returns the indexes B whose temporal series
    do not exist in (with numerical tolerance).
    """
    A = np.asarray(A)
    B = np.asarray(B)

    # Quantization (stable and fast)
    Aq = np.round(A, decimals=decimals)
    Bq = np.round(B, decimals=decimals)

    # Hash per line
    set_A = {tuple(row) for row in Aq}

    # New indexes
    return [i for i, row in enumerate(Bq) if tuple(row) not in set_A]

def p2p_from_time(signal, fs, tmin_ms, start_ms=10):
    signal = np.asarray(signal)
    start_idx = int(round((start_ms - tmin_ms) * fs / 1000))
    cropped = signal[start_idx:]
    return round(np.ptp(cropped),2)
