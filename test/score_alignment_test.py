import pytest
from Assignment9 import Alignment


class TestScoreAlignment:
    @pytest.mark.parametrize("seq1, seq2, expected", [
        # Happy path tests
        ("ACGT", "ACGT", 4),
        ("ACGT", "ACTT", 2),
        ("AAAA", "TTTT", -4),
        
        # Edge cases
        ("A", "A", 1),
        
        # Mixed match/mismatch
        ("ACGT", "AGCT", 0),
        ("ATCG", "TAGC", -4)
    ], ids=[
        "perfect_match",
        "partial_match",
        "complete_mismatch",
        "single_character_match",
        "mixed_match_first_half",
        "balanced_match_mismatch"
    ])
    def test_score_alignment_valid_inputs(self, seq1, seq2, expected):
        # Assert
        assert Alignment().score_alignment(seq1, seq2) == expected

    def test_score_alignment_unequal_lengths(self):
        # Act & Assert
        with pytest.raises(ValueError, match='Lengths of the two sequences should match or the two sequence should not be empty'):
            Alignment().score_alignment("ACGT", "ACG")

    def test_score_alignment_empty_string(self):
        test_obj = Alignment()
        
        # Act & Assert
        with pytest.raises(ValueError, match='Lengths of the two sequences should match or the two sequence should not be empty'):
            test_obj.score_alignment("ACT", "")
            
        with pytest.raises(ValueError, match='Lengths of the two sequences should match or the two sequence should not be empty'):
            test_obj.score_alignment("", "AC")