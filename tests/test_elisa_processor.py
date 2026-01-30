#!/usr/bin/env python3
"""
Unit tests for ELISA data processing pipeline
Author: Stephane Karim
Date: January 2026
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from elisa_processor import (
    calculate_average_od,
    calculate_corrected_od,
    read_elisa_data,
)


class TestAverageODCalculation:
    """Test suite for average OD calculations."""
    
    def test_average_calculation_basic(self):
        """Test basic average calculation with simple values."""
        df = pd.DataFrame({
            'Sample': ['Sample1', 'Sample2'],
            'OD1': [0.4, 0.6],
            'OD2': [0.6, 0.8]
        })
        
        result = calculate_average_od(df)
        
        assert 'AverageOD' in result.columns
        assert result['AverageOD'].tolist() == [0.5, 0.7]
    
    def test_average_calculation_decimals(self):
        """Test average calculation with decimal precision."""
        df = pd.DataFrame({
            'Sample': ['Sample1'],
            'OD1': [0.443],
            'OD2': [0.488]
        })
        
        result = calculate_average_od(df)
        
        expected = (0.443 + 0.488) / 2
        assert abs(result['AverageOD'].iloc[0] - expected) < 1e-10
    
    def test_average_calculation_zeros(self):
        """Test average calculation with zero values."""
        df = pd.DataFrame({
            'Sample': ['Blank'],
            'OD1': [0.0],
            'OD2': [0.0]
        })
        
        result = calculate_average_od(df)
        
        assert result['AverageOD'].iloc[0] == 0.0
    
    def test_average_calculation_identical_duplicates(self):
        """Test average when duplicates are identical."""
        df = pd.DataFrame({
            'Sample': ['Sample1'],
            'OD1': [0.5],
            'OD2': [0.5]
        })
        
        result = calculate_average_od(df)
        
        assert result['AverageOD'].iloc[0] == 0.5


class TestCorrectedODCalculation:
    """Test suite for corrected OD calculations."""
    
    def test_corrected_od_with_blank(self):
        """Test corrected OD calculation with a blank sample."""
        df = pd.DataFrame({
            'Sample': ['Sample1', 'BLANK'],
            'OD1': [0.5, 0.1],
            'OD2': [0.5, 0.1],
            'AverageOD': [0.5, 0.1]
        })
        
        result = calculate_corrected_od(df)
        
        assert 'CorrectedOD' in result.columns
        assert result.loc[0, 'CorrectedOD'] == 0.4  # 0.5 - 0.1
        assert result.loc[1, 'CorrectedOD'] == 0.0  # Blank should be 0
    
    def test_corrected_od_case_insensitive_blank(self):
        """Test that blank detection is case-insensitive."""
        df = pd.DataFrame({
            'Sample': ['Sample1', 'blank'],
            'OD1': [0.6, 0.2],
            'OD2': [0.6, 0.2],
            'AverageOD': [0.6, 0.2]
        })
        
        result = calculate_corrected_od(df)
        
        assert abs(result.loc[0, 'CorrectedOD'] - 0.4) < 1e-10  # 0.6 - 0.2
    
    def test_corrected_od_no_blank(self):
        """Test behavior when no blank is present."""
        df = pd.DataFrame({
            'Sample': ['Sample1', 'Sample2'],
            'OD1': [0.5, 0.6],
            'OD2': [0.5, 0.6],
            'AverageOD': [0.5, 0.6]
        })
        
        result = calculate_corrected_od(df)
        
        # Should equal AverageOD when no blank
        assert result['CorrectedOD'].tolist() == [0.5, 0.6]
    
    def test_negative_corrected_od(self):
        """Test that corrected OD can be negative (sample lower than blank)."""
        df = pd.DataFrame({
            'Sample': ['Sample1', 'BLANK'],
            'OD1': [0.1, 0.5],
            'OD2': [0.1, 0.5],
            'AverageOD': [0.1, 0.5]
        })
        
        result = calculate_corrected_od(df)
        
        assert result.loc[0, 'CorrectedOD'] == -0.4  # 0.1 - 0.5


class TestDataIntegrity:
    """Test suite for data loading and integrity checks."""
    
    def test_columns_preserved(self):
        """Test that original columns are preserved during processing."""
        df = pd.DataFrame({
            'Sample': ['Sample1', 'BLANK'],
            'OD1': [0.5, 0.1],
            'OD2': [0.5, 0.1]
        })
        
        df = calculate_average_od(df)
        df = calculate_corrected_od(df)
        
        assert 'Sample' in df.columns
        assert 'OD1' in df.columns
        assert 'OD2' in df.columns
        assert 'AverageOD' in df.columns
        assert 'CorrectedOD' in df.columns
    
    def test_row_count_preserved(self):
        """Test that number of rows is preserved during processing."""
        df = pd.DataFrame({
            'Sample': ['S1', 'S2', 'S3', 'BLANK'],
            'OD1': [0.4, 0.5, 0.6, 0.1],
            'OD2': [0.4, 0.5, 0.6, 0.1]
        })
        
        original_count = len(df)
        
        df = calculate_average_od(df)
        df = calculate_corrected_od(df)
        
        assert len(df) == original_count


class TestEdgeCases:
    """Test suite for edge cases and boundary conditions."""
    
    def test_single_sample(self):
        """Test processing with only one sample."""
        df = pd.DataFrame({
            'Sample': ['Sample1'],
            'OD1': [0.5],
            'OD2': [0.5]
        })
        
        df = calculate_average_od(df)
        df = calculate_corrected_od(df)
        
        assert len(df) == 1
        assert 'AverageOD' in df.columns
        assert 'CorrectedOD' in df.columns
    
    def test_very_large_values(self):
        """Test processing with very large OD values."""
        df = pd.DataFrame({
            'Sample': ['Sample1', 'BLANK'],
            'OD1': [100.0, 1.0],
            'OD2': [100.0, 1.0]
        })
        
        df = calculate_average_od(df)
        df = calculate_corrected_od(df)
        
        assert df.loc[0, 'CorrectedOD'] == 99.0
    
    def test_very_small_differences(self):
        """Test precision with very small differences."""
        df = pd.DataFrame({
            'Sample': ['Sample1', 'BLANK'],
            'OD1': [0.0001, 0.0000],
            'OD2': [0.0001, 0.0000]
        })
        
        df = calculate_average_od(df)
        df = calculate_corrected_od(df)
        
        assert abs(df.loc[0, 'CorrectedOD'] - 0.0001) < 1e-10


class TestRealWorldData:
    """Test suite using realistic ELISA data."""
    
    def test_typical_elisa_dataset(self):
        """Test with a typical ELISA dataset structure."""
        df = pd.DataFrame({
            'Sample': ['Sample1', 'Sample2', 'Sample3', 'BLANK'],
            'OD1': [0.443, 0.433, 0.343, 0.11],
            'OD2': [0.488, 0.43, 0.351, 0.135]
        })
        
        df = calculate_average_od(df)
        df = calculate_corrected_od(df)
        
        # Check blank average
        expected_blank = (0.11 + 0.135) / 2
        
        # Check first sample corrected OD
        sample1_avg = (0.443 + 0.488) / 2
        expected_corrected = sample1_avg - expected_blank
        
        assert abs(df.loc[0, 'CorrectedOD'] - expected_corrected) < 1e-10
        assert df.loc[3, 'CorrectedOD'] == 0.0  # Blank should be 0
    
    def test_coefficient_of_variation(self):
        """Test that duplicate precision can be calculated."""
        df = pd.DataFrame({
            'Sample': ['Sample1'],
            'OD1': [0.443],
            'OD2': [0.488]
        })
        
        df = calculate_average_od(df)
        
        # Calculate CV% = (std / mean) * 100
        mean = df['AverageOD'].iloc[0]
        std = np.std([df['OD1'].iloc[0], df['OD2'].iloc[0]])
        cv = (std / mean) * 100
        
        # CV should be reasonable for good duplicates (typically < 15%)
        assert cv < 15.0


def test_full_pipeline():
    """Integration test for the complete processing pipeline."""
    # Create sample data
    df = pd.DataFrame({
        'Sample': ['Sample1', 'Sample2', 'Sample3', 'BLANK'],
        'OD1': [0.443, 0.433, 0.343, 0.11],
        'OD2': [0.488, 0.43, 0.351, 0.135]
    })
    
    # Process through pipeline
    df = calculate_average_od(df)
    df = calculate_corrected_od(df)
    
    # Verify final structure
    expected_columns = ['Sample', 'OD1', 'OD2', 'AverageOD', 'CorrectedOD']
    assert all(col in df.columns for col in expected_columns)
    
    # Verify data integrity
    assert len(df) == 4
    assert df['Sample'].tolist() == ['Sample1', 'Sample2', 'Sample3', 'BLANK']
    
    # Verify blank correction applied
    assert df.loc[df['Sample'] == 'BLANK', 'CorrectedOD'].iloc[0] == 0.0


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
