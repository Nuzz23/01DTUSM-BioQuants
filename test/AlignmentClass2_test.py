import pytest
import tempfile
import os
from Assignment9 import Alignment

class TestAlignmentAdditionalTests:
    def test_pretty_print_stdout(self, capsys):
        # Arrange
        alignment = Alignment()
        alignment.setReferenceSequence("ACGTACGTACGT")
        results = [["ACGT", "ACGT", 8, 4]]
        
        # Act
        alignment.prettyPrint(results)
        captured = capsys.readouterr()
        
        # Assert
        assert "Reference sequence : ACGTACGTACGT" in captured.out
        assert "Portion of the reference sequence : ACGT" in captured.out
        assert "Sequence queried : ACGT" in captured.out
        assert "Position for the best alignment in the reference sequence : 8" in captured.out
        assert "best scoring obtained : 4" in captured.out

    def test_pretty_print_file(self):
        # Arrange
        alignment = Alignment()
        alignment.setReferenceSequence("ACGTACGTACGT")
        results = [["ACGT", "ACGT", 0, 4]]
        
        # Act
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            alignment.prettyPrint(results, temp_file.name)
            temp_file.close()
            
            with open(temp_file.name, 'r') as f:
                content = f.read()
            
            os.unlink(temp_file.name)
        
        # Assert
        assert "Reference sequence : ACGTACGTACGT" in content
        assert "Portion of the reference sequence : ACGT" in content
        assert "Sequence queried : ACGT" in content
        assert "Position for the best alignment in the reference sequence : 0" in content
        assert "best scoring obtained : 4" in content

    def test_align_reads_custom_scoring_function(self):
        # Arrange
        alignment = Alignment()
        alignment.setReferenceSequence("ACGXACGXACGX")
        
        def custom_scoring(self, ref_sub, query):
            return len([c for c in ref_sub if c in query])
        
        # Assert
        assert alignment.align_reads(querySequence=["ACGT"], alignmentFunction=custom_scoring, outputFile=False) == [["ACGX", "ACGT", 0, 3]]

    def test_align_reads_multiple_queries(self):
        # Arrange
        alignment = Alignment()
        alignment.setReferenceSequence("ACGTACGTACGT")
        
        # Act
        results = alignment.align_reads(querySequence=["ACGT", "TGCA"], outputFile=False)
        
        # Assert
        assert len(results) == 2
        assert results[0] == ["ACGT", "ACGT", 0, 4]
        assert results[1] == ["CGTA", "TGCA", 1, 0]

    def test_align_reads_file_input(self):
        # Arrange
        alignment = Alignment()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as ref_file, \
             tempfile.NamedTemporaryFile(mode='w', delete=False) as query_file:
            ref_file.write("ACGTACGTACGT")
            ref_file.close()
            
            query_file.write("ACGT\nTGCA")
            query_file.close()
        
        # Act
        try:
            results = alignment.align_reads(
                pathReferenceSequence=ref_file.name, 
                pathQuerySequence=query_file.name, 
                outputFile=False
            )
        finally:
            os.unlink(ref_file.name)
            os.unlink(query_file.name)
        
        # Assert
        assert len(results) == 2
        assert results[0] == ["ACGT", "ACGT", 0, 4]
        assert results[1] == ["CGTA", "TGCA", 1, 0]

    def test_align_reads_setter_methods(self):
        # Arrange
        alignment = Alignment()
        alignment.setReferenceSequence("ACGTACGTACGT")
        alignment.setQuerySequence(["ACGT", "TGCA"])
        
        # Act
        results = alignment.align_reads(outputFile=False)
        
        # Assert
        assert len(results) == 2
        assert results[0] == ["ACGT", "ACGT", 0, 4]
        assert results[1] == ["CGTA", "TGCA", 1, 0]

    def test_align_reads_error_handling(self):
        # Arrange
        alignment = Alignment()
        
        # Act & Assert
        with pytest.raises(ValueError, match='Before using align read you should either set reference sequence'):
            alignment.align_reads(querySequence=["ACGT"])
        
        with pytest.raises(ValueError, match='Before using align read you should either set query sequence'):
            alignment.align_reads(referenceSequence="ACGTACGTACGT")
        
        with pytest.raises(ValueError, match='Incorrect reference sequence passed'):
            alignment.align_reads(referenceSequence="123", querySequence=["ACGT"])
        
        with pytest.raises(ValueError, match='Incorrect query sequence'):
            alignment.align_reads(referenceSequence="ACGTACGTACGT", querySequence=["123"])
