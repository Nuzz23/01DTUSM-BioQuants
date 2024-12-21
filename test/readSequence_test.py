import pytest
import os
from Assignment9 import Alignment

class TestReadSequence:
    @pytest.fixture
    def alignment(self):
        return Alignment()

    @pytest.mark.parametrize("file_content,expected", [
        # Happy path tests
        ("ATCG", "ATCG"),  # Single line sequence
        ("atcg", "ATCG"),  # Lowercase conversion
        ("  ATCG  ", "ATCG"),  # Whitespace handling
        ("ATCG\nGCTA", "ATCGGCTA"),  # Multiple lines
        ("  ATCG  \n  GCTA  ", "ATCGGCTA"),  # Multiple lines with whitespace
        (' ATCGC-  \n XGTA', 'ATCGC-XGTA')
    ], ids=["single_line", "lowercase_conversion", "whitespace_trim", "multiple_lines", "multiple_lines_whitespace", 'non_standard_characters'])
    
    def test_read_sequence_success(self, alignment, tmp_path, file_content, expected):
        # Arrange
        test_file = tmp_path / "reference_sequence.txt"
        test_file.write_text(file_content)

        # Act
        result = alignment.readSequence(str(test_file))

        # Assert
        assert result == expected

    def test_read_sequence_empty_file(self, alignment, tmp_path):
        # Arrange
        test_file = tmp_path / "empty_file.txt"
        test_file.write_text("")

        # Act
        result = alignment.readSequence(str(test_file))

        # Assert
        assert result == ""

    def test_read_sequence_nonexistent_file(self, alignment):
        # Arrange
        nonexistent_path = "/path/to/nonexistent/file.txt"

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            alignment.readSequence(nonexistent_path)

