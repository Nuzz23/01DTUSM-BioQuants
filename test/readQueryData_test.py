import pytest
import os
from Assignment9 import Alignment

class TestReadQueryData:
    @pytest.fixture
    def alignment(self):
        return Alignment()

    @pytest.mark.parametrize("file_content,expected", [
        # Happy path tests
        ("ATCG\nGCTA\nTAGC", ["ATCG", "GCTA", "TAGC"]),  # Multiple sequences
        ("ATCG", ["ATCG"]),  # Single sequence
        ("  ATCG  \n  GCTAX  ", ["ATCG", "GCTAX"])  # Sequences with whitespace and missing characters
    ], ids=["multiple_sequences", "single_sequence", "whitespace_sequences"])
    
    def test_read_query_data_success(self, alignment, tmp_path, file_content, expected):
        # Arrange
        test_file = tmp_path / "query_sequences.txt"
        test_file.write_text(file_content)

        # Act
        result = alignment.readQueryData(str(test_file))

        # Assert
        assert result == expected

    def test_read_query_data_empty_file(self, alignment, tmp_path):
        # Arrange
        test_file = tmp_path / "empty_file.txt"
        test_file.write_text("")

        # Act
        result = alignment.readQueryData(str(test_file))

        # Assert
        assert result == []

    def test_read_query_data_nonexistent_file(self, alignment):
        # Arrange
        nonexistent_path = "/path/to/nonexistent/file.txt"

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            alignment.readQueryData(nonexistent_path)
