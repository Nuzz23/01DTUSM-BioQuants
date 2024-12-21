import pytest
from Assignment9 import Alignment

class TestCheckSequenceValidity:
    @pytest.mark.parametrize("input_string, expected", [
        # Happy path tests
        ("ACGT", True),
        ("ACGT-X", True),
        ("AAACCCGGGTTT", True),
        
        # Edge cases
        ("", False),
        ("-", True),
        ("X", True),
        
        # Error cases
        ("ACGTB", False),
        ("123", False),
        ("acgt", False)  # This is the reason to perform an upper case conversion
    ], ids=[
        "valid_standard_sequence",
        "valid_sequence_with_special_chars", 
        "valid_long_sequence",
        "empty_string",
        "single_dash",
        "single_x",
        "invalid_sequence_with_extra_char",
        "numeric_sequence", 
        "lowercase_sequence"
    ])
    def test_check_sequence_validity(self, input_string, expected):
        # Arrange
        test_obj = Alignment()
        
        # Act
        result = test_obj.checkSequenceValidity(input_string)
        
        # Assert
        assert result == expected
