import pytest
from Assignment9 import Alignment

class TestFindBestAlignment:
    @pytest.mark.parametrize("reference, query, expected_pos, expected_score", [
        # Happy path tests
        ("ACGTACGTACGT", "ACGT", 0, 4),
        ("XTATATATATAT", "ATAT", 2, 4),
        ("GCATGCATGCAT", "ATGX", 2, 2),
        
        # Edge cases
        ("AAAAA", "AAA", 0, 3)
    ], ids=[
        "standard_best_alignment",
        "repeated_pattern_alignment",
        "partial_match_alignment", 
        "multiple_best_positions",
    ])
    def test_find_best_alignment_valid_inputs(self, reference, query, expected_pos, expected_score):
        # Act
        pos, score = Alignment().find_best_alignment(reference, query)
        
        # Assert
        assert pos == expected_pos
        assert score == expected_score

    def test_find_best_alignment_invalid_length(self):        
        # Act & Assert
        with pytest.raises(ValueError, match='reference sequence length should be higher than the query sequence length'):
            Alignment().find_best_alignment("SHORT", "LONGER_QUERY")
            
        with pytest.raises(ValueError, match='reference sequence length should be higher than the query sequence length'):
            Alignment().find_best_alignment("EQUAL", "EQUAL")

    def test_find_best_alignment_custom_scoring(self):
        def custom_scoring(self, ref_sub, query):
            return len([c for c in ref_sub if c in query])
        
        # Act
        pos, score = Alignment().find_best_alignment("ACGTACGTACGT", "ACGX", custom_scoring)
        
        # Assert
        assert pos == 0
        assert score == 3
