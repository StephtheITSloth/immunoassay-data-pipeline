#!/usr/bin/env python3
"""
Advanced ELISA Analysis with Standard Curve
Author: Stephane Karim
Date: January 2026

This script extends the basic ELISA processing by:
1. Processing standard curve data
2. Fitting a four-parameter logistic (4PL) regression model
3. Calculating protein concentrations from OD values
4. Generating publication-quality visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pathlib import Path
import sys


class ELISAAnalyzer:
    """
    Complete ELISA data analysis including standard curve fitting
    and concentration calculations.
    """
    
    def __init__(self):
        self.elisa_data = None
        self.standard_data = None
        self.blank_od = None
        self.curve_params = None
        
    def load_data(self, elisa_path, standard_path):
        """Load both ELISA sample data and standard curve data."""
        try:
            self.elisa_data = pd.read_csv(elisa_path)
            self.standard_data = pd.read_csv(standard_path)
            print(f"✓ Loaded ELISA data: {len(self.elisa_data)} samples")
            print(f"✓ Loaded standard data: {len(self.standard_data)} standards")
        except Exception as e:
            print(f"Error loading data: {e}")
            sys.exit(1)
    
    def process_elisa_data(self):
        """Process ELISA data: calculate averages and correct for blank."""
        # Calculate average OD
        self.elisa_data['AverageOD'] = (
            self.elisa_data['OD1'] + self.elisa_data['OD2']
        ) / 2
        
        # Find and store blank value
        blank_mask = self.elisa_data['Sample'].str.upper() == 'BLANK'
        if blank_mask.any():
            self.blank_od = self.elisa_data.loc[blank_mask, 'AverageOD'].values[0]
            self.elisa_data['CorrectedOD'] = self.elisa_data['AverageOD'] - self.blank_od
            self.elisa_data.loc[blank_mask, 'CorrectedOD'] = 0
            print(f"✓ Blank OD: {self.blank_od:.4f}")
        else:
            print("Warning: No blank found")
            self.blank_od = 0
            self.elisa_data['CorrectedOD'] = self.elisa_data['AverageOD']
    
    def process_standard_data(self):
        """Process standard curve data."""
        self.standard_data['AverageOD'] = (
            self.standard_data['OD1'] + self.standard_data['OD2']
        ) / 2
        self.standard_data['CorrectedOD'] = self.standard_data['AverageOD'] - self.blank_od
        print("✓ Processed standard curve data")
    
    @staticmethod
    def four_parameter_logistic(x, A, B, C, D):
        """
        Four-parameter logistic (4PL) function for ELISA standard curves.
        
        Parameters:
        -----------
        x : array-like
            Concentration values
        A : float
            Minimum asymptote (minimum response)
        B : float
            Hill's slope (steepness of curve)
        C : float
            Inflection point (EC50)
        D : float
            Maximum asymptote (maximum response)
        
        Returns:
        --------
        array-like
            OD values predicted by the 4PL model
        """
        return D + (A - D) / (1 + (x / C) ** B)
    
    def fit_standard_curve(self):
        """
        Fit a 4-parameter logistic curve to standard data.
        """
        x = self.standard_data['Concentration (ng/ml)'].values
        y = self.standard_data['CorrectedOD'].values
        
        # Initial parameter guesses
        A = np.min(y)  # Min OD
        D = np.max(y)  # Max OD
        C = np.median(x)  # EC50 approximation
        B = 1.0  # Hill slope
        
        try:
            # Fit the curve
            self.curve_params, _ = curve_fit(
                self.four_parameter_logistic,
                x, y,
                p0=[A, B, C, D],
                maxfev=10000
            )
            
            # Calculate R²
            y_pred = self.four_parameter_logistic(x, *self.curve_params)
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)
            
            print(f"✓ Standard curve fitted successfully")
            print(f"  R² = {r_squared:.4f}")
            print(f"  Parameters: A={self.curve_params[0]:.4f}, "
                  f"B={self.curve_params[1]:.4f}, "
                  f"C={self.curve_params[2]:.4f}, "
                  f"D={self.curve_params[3]:.4f}")
            
            return r_squared
            
        except Exception as e:
            print(f"Error fitting curve: {e}")
            return None
    
    def calculate_concentrations(self):
        """
        Calculate protein concentrations from OD values using the standard curve.
        Uses inverse of 4PL function.
        """
        if self.curve_params is None:
            print("Error: Standard curve not fitted yet")
            return
        
        A, B, C, D = self.curve_params
        
        concentrations = []
        for _, row in self.elisa_data.iterrows():
            od = row['CorrectedOD']
            
            # Skip blank
            if row['Sample'].upper() == 'BLANK':
                concentrations.append(0)
                continue
            
            # Inverse 4PL to get concentration from OD
            # od = D + (A - D) / (1 + (x / C)^B)
            # Solving for x (concentration)
            try:
                if od >= D:
                    # OD at or above maximum - saturated
                    conc = np.nan
                elif od <= A:
                    # OD at or below minimum - below detection
                    conc = np.nan
                else:
                    # Calculate concentration
                    conc = C * ((D - A) / (od - A) - 1) ** (1 / B)
                concentrations.append(conc)
            except:
                concentrations.append(np.nan)
        
        self.elisa_data['Concentration (ng/ml)'] = concentrations
        print("✓ Calculated protein concentrations")
    
    def plot_results(self, output_path='elisa_analysis.png'):
        """
        Generate publication-quality plots of the analysis.
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Plot 1: Standard Curve
        x_std = self.standard_data['Concentration (ng/ml)'].values
        y_std = self.standard_data['CorrectedOD'].values
        
        # Generate smooth curve for plotting
        x_smooth = np.logspace(np.log10(x_std.min()), np.log10(x_std.max()), 100)
        y_smooth = self.four_parameter_logistic(x_smooth, *self.curve_params)
        
        ax1.scatter(x_std, y_std, s=100, alpha=0.7, color='navy', 
                   label='Standards', zorder=5)
        ax1.plot(x_smooth, y_smooth, 'r-', linewidth=2, 
                label='4PL Fit', alpha=0.8)
        ax1.set_xlabel('Concentration (ng/ml)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Corrected OD (450 nm)', fontsize=12, fontweight='bold')
        ax1.set_title('ELISA Standard Curve', fontsize=14, fontweight='bold')
        ax1.set_xscale('log')
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.legend(fontsize=10)
        
        # Plot 2: Sample Concentrations
        samples = self.elisa_data[
            self.elisa_data['Sample'].str.upper() != 'BLANK'
        ].copy()
        
        # Remove NaN values for plotting
        samples_valid = samples[samples['Concentration (ng/ml)'].notna()]
        
        if len(samples_valid) > 0:
            x_pos = np.arange(len(samples_valid))
            ax2.bar(x_pos, samples_valid['Concentration (ng/ml)'], 
                   color='steelblue', alpha=0.7, edgecolor='navy', linewidth=1.5)
            ax2.set_xlabel('Sample', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Concentration (ng/ml)', fontsize=12, fontweight='bold')
            ax2.set_title('Sample Protein Concentrations', fontsize=14, fontweight='bold')
            ax2.set_xticks(x_pos)
            ax2.set_xticklabels(samples_valid['Sample'], rotation=45, ha='right')
            ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ Plots saved to: {output_path}")
        plt.close()
    
    def generate_report(self, output_path='elisa_report.txt'):
        """Generate a text report of the analysis."""
        with open(output_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write("ELISA ANALYSIS REPORT\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Blank OD: {self.blank_od:.4f}\n\n")
            
            f.write("Standard Curve Parameters (4PL Model):\n")
            f.write(f"  A (min asymptote): {self.curve_params[0]:.4f}\n")
            f.write(f"  B (Hill slope): {self.curve_params[1]:.4f}\n")
            f.write(f"  C (EC50): {self.curve_params[2]:.4f}\n")
            f.write(f"  D (max asymptote): {self.curve_params[3]:.4f}\n\n")
            
            f.write("Sample Results:\n")
            f.write("-"*70 + "\n")
            
            for _, row in self.elisa_data.iterrows():
                if row['Sample'].upper() != 'BLANK':
                    f.write(f"{row['Sample']}: ")
                    f.write(f"OD = {row['CorrectedOD']:.4f}, ")
                    if pd.notna(row['Concentration (ng/ml)']):
                        f.write(f"Conc = {row['Concentration (ng/ml)']:.2f} ng/ml\n")
                    else:
                        f.write("Conc = Out of range\n")
            
            f.write("="*70 + "\n")
        
        print(f"✓ Report saved to: {output_path}")
    
    def save_processed_data(self, output_path='elisa_result.csv'):
        """Save the processed data to CSV."""
        self.elisa_data.to_csv(output_path, index=False)
        print(f"✓ Processed data saved to: {output_path}")


def main():
    """Main execution function."""
    print("\n" + "="*70)
    print("ADVANCED ELISA ANALYSIS PIPELINE")
    print("="*70 + "\n")
    
    # Initialize analyzer
    analyzer = ELISAAnalyzer()
    
    # Get file paths
    elisa_path = input("Enter path to ELISA data CSV: ").strip().strip('"').strip("'")
    standard_path = input("Enter path to standard values CSV: ").strip().strip('"').strip("'")
    
    # Load and process data
    print("\n" + "-"*70)
    analyzer.load_data(elisa_path, standard_path)
    
    print("\nProcessing data...")
    print("-"*70)
    analyzer.process_elisa_data()
    analyzer.process_standard_data()
    
    print("\nFitting standard curve...")
    print("-"*70)
    analyzer.fit_standard_curve()
    
    print("\nCalculating concentrations...")
    print("-"*70)
    analyzer.calculate_concentrations()
    
    print("\nGenerating outputs...")
    print("-"*70)
    analyzer.save_processed_data()
    analyzer.plot_results()
    analyzer.generate_report()
    
    print("\n" + "="*70)
    print("Analysis complete! ✓")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
