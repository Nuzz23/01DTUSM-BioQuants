import pytest
import tempfile
import os
from Assignment9 import Alignment

class TestAlignReads:
    @pytest.mark.parametrize("reference, query, expected_results", [
        # Happy path tests
        ("ACGTACGTACGT", ["ACGT"], [["ACGT", "ACGT", 0, 4]]),
        ("AT-TATATATAT", ["ATAT"], [["ATAT", "ATAT", 4, 4]]),
        ("GCATG-ATGXAT", ["ATGC"], [["ATG-", "ATGC", 2, 2]])
    ], ids=[
        "single_query_standard_alignment",
        "repeated_pattern_alignment",
        "partial_match_alignment"
    ])
    def test_align_reads_direct_input(self, reference, query, expected_results):
        # Assert
        assert Alignment().align_reads(referenceSequence=reference, querySequence=query, outputFile=False) == expected_results

    def test_align_reads_file_input(self):
        # Arrange
        
        test_obj = Alignment()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as ref_file, \
             tempfile.NamedTemporaryFile(mode='w', delete=False) as query_file:
            ref_file.write("-CGTACGTACGT")
            ref_file.close()
            
            query_file.write("ACGT")
            query_file.close()
        
        # Act
        try:
            results = test_obj.align_reads(
                pathReferenceSequence=ref_file.name, 
                pathQuerySequence=query_file.name, 
                outputFile=False
            )
        finally:
            os.unlink(ref_file.name)
            os.unlink(query_file.name)
        
        # Assert
        assert results == [["ACGT", "ACGT", 4, 4]]

    def test_align_reads_no_reference_sequence(self):        
        # Act & Assert
        with pytest.raises(ValueError, match='Before using align read you should either set reference sequence'):
            Alignment().align_reads(querySequence=["ACGT"])

    def test_align_reads_no_query_sequence(self):        
        # Act & Assert
        with pytest.raises(ValueError, match='Before using align read you should either set query sequence'):
            Alignment().align_reads(referenceSequence="ACGTACGTACGT")

    def test_align_reads_invalid_reference_sequence(self):
        # Act & Assert
        with pytest.raises(ValueError, match='Incorrect reference sequence passed'):
            Alignment().align_reads(referenceSequence="123", querySequence=["ACGT"])

    def test_align_reads_invalid_query_sequence(self):
        # Act & Assert
        with pytest.raises(ValueError, match='Incorrect query sequence'):
            Alignment().align_reads(referenceSequence="ACGTACGTACGT", querySequence=["123"])
