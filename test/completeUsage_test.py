from Assignment9 import Alignment


class TestCompleteUsage:
    REF_SEQ ='GATCGTGGCTCTAGA'
    QUERIES = ['GATC', 'GGCT','CTAG']

    def test_read_sequence(self, tmp_path):
        test_file = tmp_path / "reference_sequences.txt"
        test_file.write_text(self.REF_SEQ)
        
        assert Alignment().readSequence(str(test_file)) == self.REF_SEQ

    def test_read_query(self, tmp_path):
        test_file = tmp_path / "query_sequences.txt"
        test_file.write_text('\n'.join(self.QUERIES))
        
        assert Alignment().readQueryData(str(test_file)) == self.QUERIES

    def test_output_alignment1(self):
        ris = Alignment().align_reads(referenceSequence=self.REF_SEQ, querySequence=self.QUERIES, outputFile=None)
        
        assert len(ris) == 3
        assert all(Alignment().score_alignment(item[0], item[1]) == item[3] for item in ris)
        assert ris[0][0] == 'GATC'

    def test_output_alignment2(self):
        temp = Alignment()
        temp.align_reads(referenceSequence=self.REF_SEQ, querySequence=self.QUERIES, outputFile=None)
        temp.setQuerySequence(temp.getQuerySequence()+['CTAX', 'CGTGT'])
        ris = temp.align_reads()
        
        assert len(ris) == 5
        assert all(Alignment().score_alignment(item[0], item[1]) == item[3] for item in ris)
        assert ris[0][0] == 'GATC'
        assert ris[3] == ['CTAG', 'CTAX', 10,2]
        assert ris[4] == ['CGTGG','CGTGT',3,3]