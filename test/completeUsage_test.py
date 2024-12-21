from Assignment9 import Alignment


class TestCompleteUsage:
    REFERENCE_SEQUENCE_INPUT_PATH = 'referenceSequence.txt'
    QUERY_DATA_INPUT_PATH =  'queryData.txt'
    REF_SEQ ='GATCGTGGCTCTAGA'
    QUERIES = ['GATC', 'GGCT','CTAG']

    def test_read_sequence(self):
        # The file contains GATCGTGGCTCTAGA
        assert Alignment().readSequence(self.REFERENCE_SEQUENCE_INPUT_PATH) == 'GATCGTGGCTCTAGA'

    def test_read_query(self):
        # The file contains
        assert Alignment().readQueryData(self.QUERY_DATA_INPUT_PATH) == ['GATC', 'GGCT','CTAG']

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