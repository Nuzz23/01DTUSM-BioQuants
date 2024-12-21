import pytest
import tempfile
import os
from Assignment9 import Alignment

class TestAlignment:
    def test_initialization(self):
        # Arrange & Act
        alignment = Alignment()
        
        # Assert
        assert alignment.getReferenceSequence() is None
        assert alignment.getQuerySequence() is None

    @pytest.mark.parametrize("seq1, seq2, expected", [
        # Happy path tests
        ("ACGT", "ACGT", 4),
        ("ACGT", "AGCT", 0),
        ("ACGT", "AXGT", 2),
        
        # Edge cases
        ("A-GT", "ACGT", 2),
        ("AX-T", "ACGT", 0)
    ], ids=[
        "perfect_match",
        "partial_match",
        "match_with_x",
        "match_with_dash",
        "match_with_x_and_dash"
    ])
    def test_score_alignment(self, seq1, seq2, expected):
        # Assert
        assert Alignment().score_alignment(seq1, seq2) == expected

    def test_score_alignment_unequal_lengths(self):
        # Act & Assert
        with pytest.raises(ValueError, match='Lengths of the two sequences should match or the two sequence should not be empty'):
            Alignment().score_alignment("ACGT", "ACG")

    @pytest.mark.parametrize("reference, query, expected_pos, expected_score", [
        # Happy path tests
        ("ACGTACGTACGT", "ACGT", 0, 4),
        ("AT-TATATATAT", "ATAT", 4, 4)
    ], ids=[
        "standard_best_alignment",
        "repeated_pattern_alignment"
    ])
    def test_find_best_alignment(self, reference, query, expected_pos, expected_score):
        # Act
        pos, score = Alignment().find_best_alignment(reference, query)
        
        # Assert
        assert pos == expected_pos
        assert score == expected_score

    def test_find_best_alignment_invalid_length(self):
        with pytest.raises(ValueError, match='reference sequence length should be higher than the query sequence length'):
            Alignment().find_best_alignment("SHORT", "LONGER_QUERY")

    @pytest.mark.parametrize("sequence, is_valid", [
        # Happy path tests
        ("ACGT", True),
        ("AAACCCGGGTTT", True),
        ("A-C-G-T", True),
        ("AXXXT", True),
        
        # Error cases
        ("", False),
        ("123", False),
        ("acgt", False)
    ], ids=[
        "valid_standard_sequence",
        "valid_long_sequence", 
        "valid_sequence_with_dashes",
        "valid_sequence_with_x",
        "empty_string",
        "numeric_sequence", 
        "lowercase_sequence"
    ])
    def test_check_sequence_validity(self, sequence, is_valid):
        assert Alignment().checkSequenceValidity(sequence) == is_valid

    def test_read_sequence(self):
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write("ACGT\nTGCA")
            temp_file.close()
        
        # Act
        try:
            sequence = Alignment().readSequence(temp_file.name)
        finally:
            os.unlink(temp_file.name)
        
        # Assert
        assert sequence == "ACGTTGCA"

    def test_read_query_data(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write("ACGT\nTGCA")
            temp_file.close()
        
        # Act
        try:
            queries = Alignment().readQueryData(temp_file.name)
        finally:
            os.unlink(temp_file.name)
        
        # Assert
        assert queries == ["ACGT", "TGCA"]

    def test_setters_and_getters(self):
        # Arrange
        alignment = Alignment()
        
        # Act
        alignment.setReferenceSequence("ACGT")
        alignment.setQuerySequence(["TGCA", "GCTA"])
        
        # Assert
        assert alignment.getReferenceSequence() == "ACGT"
        assert alignment.getQuerySequence() == ["TGCA", "GCTA"]

    def test_setters_invalid_input(self):
        # Arrange
        alignment = Alignment()
        
        # Act & Assert
        with pytest.raises(ValueError, match='Invalid reference sequence'):
            alignment.setReferenceSequence("123")
        
        with pytest.raises(ValueError, match='Invalid queries sequence'):
            alignment.setQuerySequence(["123"])


