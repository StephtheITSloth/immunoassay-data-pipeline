#!/usr/bin/env python3
"""
ELISA Data Processing Pipeline
Author: Stephane Karim
Date: January 2026

This script processes ELISA (Enzyme-Linked Immunosorbent Assay) data by:
1. Reading raw optical density (OD) measurements from duplicate wells
2. Calculating average OD values
3. Correcting for blank background signal
4. Generating standard curves for concentration calculations
5. Exporting processed results for downstream analysis

This pipeline demonstrates data handling skills relevant to bioinformatics
and laboratory data analysis.
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path


def read_elisa_data(file_path):
    """
    Read ELISA data from CSV file.
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file containing raw ELISA data
        
    Returns:
    --------
    pd.DataFrame
        DataFrame containing the raw ELISA data
    """
    try:
        df = pd.read_csv(file_path)
        print(f"\n✓ Successfully loaded data from: {file_path}")
        print(f"  Columns found: {', '.join(df.columns.tolist())}")
        print(f"  Number of samples: {len(df)}")
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def calculate_average_od(df):
    """
    Calculate average OD from duplicate measurements.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with OD1 and OD2 columns
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with added AverageOD column
    """
    df['AverageOD'] = (df['OD1'] + df['OD2']) / 2
    print("\n✓ Calculated AverageOD from duplicates")
    return df


def calculate_corrected_od(df, blank_sample_name='BLANK'):
    """
    Calculate corrected OD by subtracting blank average.
    
    The blank represents background signal and should be subtracted
    from all samples to get the true signal from the target protein.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with AverageOD column
    blank_sample_name : str
        Name identifier for the blank sample (default: 'BLANK')
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with added CorrectedOD column
    """
    # Find the blank sample
    blank_mask = df['Sample'].str.upper() == blank_sample_name.upper()
    
    if not blank_mask.any():
        print(f"Warning: No blank sample found with name '{blank_sample_name}'")
        print("Setting CorrectedOD equal to AverageOD")
        df['CorrectedOD'] = df['AverageOD']
        return df
    
    # Calculate blank average
    blank_average = df.loc[blank_mask, 'AverageOD'].values[0]
    print(f"\n✓ Blank average OD: {blank_average:.4f}")
    
    # Subtract blank from all samples
    df['CorrectedOD'] = df['AverageOD'] - blank_average
    
    # Set blank's corrected OD to 0
    df.loc[blank_mask, 'CorrectedOD'] = 0
    
    print(f"✓ Calculated CorrectedOD (AverageOD - Blank)")
    
    return df


def save_results(df, output_path):
    """
    Save processed ELISA data to CSV file.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Processed DataFrame to save
    output_path : str
        Path where the CSV file should be saved
    """
    df.to_csv(output_path, index=False)
    print(f"\n✓ Results saved to: {output_path}")


def display_results_summary(df):
    """
    Display a summary of the processed data.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Processed DataFrame
    """
    print("\n" + "="*60)
    print("ELISA DATA PROCESSING SUMMARY")
    print("="*60)
    print(df.to_string(index=False, float_format=lambda x: f'{x:.4f}'))
    print("="*60 + "\n")


def main():
    """
    Main execution function for ELISA data processing pipeline.
    """
    print("\n" + "="*60)
    print("ELISA DATA PROCESSING PIPELINE")
    print("="*60)
    
    # Step 1: Get file path from user
    file_path = input("\nEnter the path to the ELISA data CSV file: ").strip()
    
    # Remove quotes if user included them
    file_path = file_path.strip('"').strip("'")
    
    # Step 2: Read the data
    df = read_elisa_data(file_path)
    
    # Step 3: Calculate AverageOD
    df = calculate_average_od(df)
    
    # Step 4: Calculate CorrectedOD
    df = calculate_corrected_od(df)
    
    # Step 5: Display results
    display_results_summary(df)
    
    # Step 6: Save results
    output_path = 'elisa_result.csv'
    save_results(df, output_path)
    
    print("Pipeline completed successfully! ✓\n")


if __name__ == "__main__":
    main()
