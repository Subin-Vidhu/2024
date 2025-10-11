# FDA Compliance Enhancement Functions
import numpy as np
from scipy import stats
import warnings

def calculate_confidence_intervals(data, confidence=0.95):
    """
    Calculate confidence intervals for FDA compliance.
    
    References:
    - FDA AI/ML SaMD Guidance (2021)
    - Bossuyt et al. STARD 2015 guidelines
    """
    if len(data) < 2:
        return {'mean': np.nan, 'lower_ci': np.nan, 'upper_ci': np.nan}
    
    mean_val = np.mean(data)
    sem = stats.sem(data)  # Standard error of mean
    
    # Calculate confidence interval
    alpha = 1 - confidence
    dof = len(data) - 1
    t_critical = stats.t.ppf(1 - alpha/2, dof)
    
    margin_error = t_critical * sem
    
    return {
        'mean': mean_val,
        'lower_ci': mean_val - margin_error,
        'upper_ci': mean_val + margin_error,
        'sem': sem,
        't_critical': t_critical
    }

def enhanced_dice_coefficient(y_true, y_pred, epsilon=1e-6):
    """
    FDA-compliant Dice coefficient with enhanced validation.
    
    References:
    - Zou et al. (2004) Academic Radiology
    - Taha & Hanbury (2015) BMC Medical Imaging
    """
    # Input validation
    if y_true.shape != y_pred.shape:
        raise ValueError("Ground truth and prediction must have identical shapes")
    
    # Convert to binary masks
    y_true_bin = y_true.astype(np.bool_)
    y_pred_bin = y_pred.astype(np.bool_)
    
    # Calculate components
    intersection = np.sum(y_true_bin & y_pred_bin)
    sum_true = np.sum(y_true_bin)
    sum_pred = np.sum(y_pred_bin)
    
    # Handle edge cases per FDA requirements
    if sum_true == 0 and sum_pred == 0:
        return 1.0  # Perfect agreement on empty
    elif sum_true == 0 or sum_pred == 0:
        return 0.0  # No overlap possible
    
    # Standard Dice formula with numerical stability
    dice = (2.0 * intersection + epsilon) / (sum_true + sum_pred + epsilon)
    
    return np.clip(dice, 0.0, 1.0)  # Ensure valid range

def robust_volume_percentage_diff(true_volume, pred_volume, min_volume_threshold=0.1):
    """
    FDA-compliant volume percentage difference calculation.
    
    Parameters:
    -----------
    true_volume, pred_volume : float
        Volumes in cm³
    min_volume_threshold : float
        Minimum volume to calculate percentage (prevents division by tiny numbers)
    
    References:
    - Kessler et al. (2015) Statistical Methods in Medical Research
    """
    # Validate inputs
    if true_volume < 0 or pred_volume < 0:
        warnings.warn("Negative volumes detected - check segmentation")
        return np.nan
    
    # Handle edge cases
    if true_volume < min_volume_threshold:
        if pred_volume < min_volume_threshold:
            return 0.0  # Both negligible
        else:
            return np.inf  # Significant prediction on negligible truth
    
    # Standard relative difference
    rel_diff = ((pred_volume - true_volume) / true_volume) * 100
    
    return rel_diff

def validate_statistical_power(n_cases, effect_size=0.1, alpha=0.05, power=0.8):
    """
    Validate if sample size meets FDA statistical power requirements.
    
    References:
    - FDA Statistical Guidance (2019)
    - Cohen's effect size conventions
    """
    from scipy.stats import norm
    
    # Calculate achieved power
    z_alpha = norm.ppf(1 - alpha/2)
    z_beta = norm.ppf(power)
    
    # Required sample size for given effect size
    required_n = ((z_alpha + z_beta) / effect_size) ** 2
    
    achieved_power = norm.cdf(effect_size * np.sqrt(n_cases) - z_alpha)
    
    return {
        'n_cases': n_cases,
        'required_n': int(np.ceil(required_n)),
        'achieved_power': achieved_power,
        'adequate_power': achieved_power >= power,
        'effect_size': effect_size
    }

def calculate_clinical_agreement_metrics(dice_scores, volume_diffs, dice_threshold=0.85, volume_threshold=10.0):
    """
    Calculate clinical agreement metrics per FDA requirements.
    
    References:
    - FDA Computer-Assisted Detection Guidance (2019)
    - Bland & Altman (1986) for agreement analysis
    """
    results = {}
    
    # Dice agreement
    if len(dice_scores) > 0:
        high_dice = np.sum(dice_scores >= dice_threshold)
        results['dice_agreement_rate'] = high_dice / len(dice_scores)
        results['dice_agreement_count'] = high_dice
        results['dice_total'] = len(dice_scores)
        
        # Calculate confidence interval for agreement rate
        ci = calculate_confidence_intervals(dice_scores >= dice_threshold)
        results['dice_agreement_ci'] = ci
    
    # Volume agreement
    if len(volume_diffs) > 0:
        good_volume = np.sum(np.abs(volume_diffs) <= volume_threshold)
        results['volume_agreement_rate'] = good_volume / len(volume_diffs)
        results['volume_agreement_count'] = good_volume
        results['volume_total'] = len(volume_diffs)
        
        # Calculate confidence interval for volume agreement
        ci = calculate_confidence_intervals(np.abs(volume_diffs) <= volume_threshold)
        results['volume_agreement_ci'] = ci
    
    return results

# Example usage for FDA validation report
def generate_fda_validation_report(dice_left, dice_right, vol_diff_left, vol_diff_right):
    """
    Generate FDA-compliant validation report.
    """
    report = {
        'timestamp': pd.Timestamp.now(),
        'validation_standard': 'FDA AI/ML SaMD Guidance 2021',
        'statistical_methods': 'Zou et al. (2004), Bland & Altman (1986)'
    }
    
    # Statistical validation
    for kidney, dice_scores in [('Left', dice_left), ('Right', dice_right)]:
        if len(dice_scores) > 0:
            ci = calculate_confidence_intervals(dice_scores)
            report[f'{kidney}_Dice_CI'] = ci
            
            # Clinical threshold analysis
            agreement = calculate_clinical_agreement_metrics(dice_scores, [])
            report[f'{kidney}_Clinical_Agreement'] = agreement
    
    # Volume analysis
    for kidney, vol_diffs in [('Left', vol_diff_left), ('Right', vol_diff_right)]:
        if len(vol_diffs) > 0:
            ci = calculate_confidence_intervals(vol_diffs)
            report[f'{kidney}_Volume_CI'] = ci
            
            # Clinical threshold analysis
            agreement = calculate_clinical_agreement_metrics([], vol_diffs)
            report[f'{kidney}_Volume_Agreement'] = agreement
    
    # Statistical power validation
    n_cases = len(dice_left) if len(dice_left) > 0 else len(dice_right)
    power_analysis = validate_statistical_power(n_cases)
    report['Statistical_Power'] = power_analysis
    
    return report
