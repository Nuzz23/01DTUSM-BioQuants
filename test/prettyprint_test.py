import pytest
import tempfile
import os
from Assignment9 import Alignment


class TestPrettyPrint:
    @pytest.mark.parametrize("results, output_path, expected_output", [
        # Happy path tests
        (
            [['ACGT', 'ACG', 0, 3]], 
            True, 
            "Reference sequence : None\n\nPortion of the reference sequence : ACGT\nSequence queried : ACG\nPosition for the best alignment in the reference sequence : 0\nbest scoring obtained : 3\n\n\n"
        ),
        (
            [['ACGT', 'ACG', 0, 3], ['TGCA', 'GC', 1, 2]], 
            True, 
            "Reference sequence : None\n\nPortion of the reference sequence : ACGT\nSequence queried : ACG\nPosition for the best alignment in the reference sequence : 0\nbest scoring obtained : 3\n\n\nPortion of the reference sequence : TGCA\nSequence queried : GC\nPosition for the best alignment in the reference sequence : 1\nbest scoring obtained : 2\n\n\n"
        )
    ], ids=[
        "single_result_stdout",
        "multiple_results_stdout"
    ])
    
    def test_pretty_print_stdout(self, results, output_path, expected_output, capsys):
        test_obj = Alignment()
        test_obj.__referenceSequence = None
        
        test_obj.prettyPrint(results, output_path)
    
        assert capsys.readouterr().out == expected_output

    def test_pretty_print_file(self):
        test_obj = Alignment()
        test_obj.__referenceSequence = None
        results = [['ACGT', 'ACG', 0, 3]]
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            test_obj.prettyPrint(results, temp_file.name)
            temp_file.close()
            
            with open(temp_file.name, 'r') as f:
                content = f.read()
            
            os.unlink(temp_file.name)
        
        expected_output = "Reference sequence : None\n\nPortion of the reference sequence : ACGT\nSequence queried : ACG\nPosition for the best alignment in the reference sequence : 0\nbest scoring obtained : 3\n\n\n"
        assert content == expected_output

    @pytest.mark.parametrize("output_path", [
        '',
        None,
        False
    ], ids=[
        "empty_string",
        "none_value",
        "false_value"
    ])
    
    def test_pretty_print_output(self, output_path):
        # Assert
        assert Alignment().prettyPrint([['ACG', 'ACG', 0, 3]], output_path) is not None
