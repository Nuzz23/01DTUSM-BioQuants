import sys
from typing import List


class Alignment():    
    def __init__(self):
        """Initialize an empty Alignment object with no sequences.
        
        Creates an Alignment instance with query and reference sequences set to None, 
        preparing the object for subsequent sequence loading or assignment.
        """

        self.__querySequence = None
        self.__referenceSequence = None
        
            
    ## SCORE ALIGNMENT FUNCTION ----------------------------------------------------------------------------------
    
    def score_alignment(self, seq1:str, seq2:str)->int:
        """Evaluates the alignment score of two string

        Args:
            seq1 (str): the first sequence
            seq2 (str): the second sequence

        Raises:
            ValueError: if the length of the two sequence is not equal

        Returns:
            score (int): the score alignment obtained
        """
        
        if len(seq1) != len(seq2) or not len(seq1) or not len(seq2):
            raise ValueError('Lengths of the two sequences should match or the two sequence should not be empty')
        
        return sum(1 if seq1[i] == seq2[i] and seq1[i] not in {'X', '-'} else -1 for i in range(len(seq1)))
    
    
    ## ALIGNMENT READS
    def align_reads(self, referenceSequence:str=None, querySequence:List[str]=None,
                    pathReferenceSequence:str=None, pathQuerySequence:str=None,
                    alignmentFunction=score_alignment, outputFile:str = True
                    ) -> List[List[str]]:
        """Align query sequences against a reference sequence using a specified alignment function.

        Performs sequence alignment by finding the best matching positions of query sequences within a reference sequence. 
        Supports flexible input methods including direct sequences, file paths, or previously set sequences.

        Args:
            referenceSequence (str): Optional direct reference sequence.
            pathReferenceSequence (str): Optional path to the reference sequence file.
            querySequence (str): Optional direct query sequences as a list or set.
            pathQuerySequence (str): Optional path to the query sequence file.
            alignmentFunction (Function): Function used to score alignments, defaults to score_alignment.
            outputFile (None|bool|str): Controls where the results are going to be outputted, if a non empty string is given it's interpreted as
                the path to a file where to print the data. If a True boolean is given, the prints occurs on screen (stdout). 
                If anything else is given, no print occurs. 

        Returns:
            results (list[list[str, str, int, int]]): A list of alignment results, 
            each containing [matched reference segment, query sequence, position in the reference sequence, score].

        Raises:
            ValueError: If no valid reference or query sequences are provided or sequences are invalid.
        """
        
        if not (referenceSequence or pathReferenceSequence or self.__referenceSequence):
            raise ValueError('Before using align read you should either set reference sequence via setter or give a reference sequence'+
                            'as a string via referenceSequence param or a path to a file containing a reference sequence via the path param')
            
        if not (querySequence or pathQuerySequence or self.__querySequence):
            raise ValueError('Before using align read you should either set query sequence via setter or give a query sequence'+
                            'as a string via querySequence param or a path to a file containing a query sequence via the path param')
                
        
        if referenceSequence or pathReferenceSequence:
            
            referenceSequence = referenceSequence or self.readSequence(pathReferenceSequence)
            referenceSequence = referenceSequence.strip().upper()
            
            if not self.checkSequenceValidity(referenceSequence):
                raise ValueError('Incorrect reference sequence passed ')
        else:
            referenceSequence = self.__referenceSequence
        
        if querySequence or pathQuerySequence:        
            querySequence = list(querySequence) if querySequence else self.readQueryData(path=pathQuerySequence)
            
            querySequence = list(map(lambda x:x.strip().upper(), querySequence))
            
            for seq in querySequence:
                if not self.checkSequenceValidity(seq):
                    raise ValueError('Incorrect query sequence')
                
            self.__querySequence = querySequence
            
            
        self.__referenceSequence = referenceSequence.upper()
        
        alignment = []

        for data in self.__querySequence:
            pos, score = self.find_best_alignment(self.__referenceSequence, data, scoringFunction=alignmentFunction)
            alignment.append([self.__referenceSequence[pos:pos+len(data)], data, pos, score])
            
            
        self.prettyPrint(alignment, outputFilePath=outputFile)
        
        return alignment
    

    ## BEST ALIGNMENT FUNCTION ---------------------------------------------------------------------------

    def find_best_alignment(self, reference:str, query:str, scoringFunction=score_alignment)->List[int]:
        """evaluates the best possible alignment for a query sequence into a sequence

        Args:
            reference (str): the reference sequence 
            query (str): the sub sequence to be aligned to the reference sequence
            scoringFunction (function, optional): the function to be used to determine the score, 
            the function must accept two string as input (in the order reference, subsequence) and must return an 
            integer or float.  Defaults to score_alignment.

        Raises:
            ValueError: if the reference sequence has a lower or equal length to the query sequence

        Returns:
            position (int): the starting position in the reference sequence for which the best alignment score was obtained 
            best score (int): the best alignment score obtained by the sequence  
        """
        
        if len(reference) <= len(query):
            raise ValueError('reference sequence length should be higher than the query sequence length')
        
        try:
            maximumScore = float('-inf')
        except TypeError:
            maximumScore = -999999999
        
        for i in range(len(reference)-len(query), -1, -1):
            score = scoringFunction(self, reference[i:i+len(query)], query)
            if score >= maximumScore:
                maximumScore = score
                pos = i

        return pos, maximumScore


    ## PRETTY PRINT OF THE RESULTS ------------------------------------------------------------------------

    def prettyPrint(self, results:List[List[str]], outputFilePath:str=True)->List[List[str]]:
        """performs the print of the align_reads function in a prettier way

        Args:
            results (list[list[str, str, int, int]]): the result of the align_reads function
            outputFile (None|bool|str): Controls where the results are going to be outputted, if a non empty string is given it's interpreted as
                the path to a file where to print the data. If a True boolean is given, the prints occurs on screen (stdout). 
                If anything else is given, no print occurs. Defaults to True.
        
        Returns: 
            The results of the align_read function (i.e. the parameter results)    
        """
        
        if isinstance(outputFilePath, bool) and outputFilePath:
            outputFilePath = sys.stdout
        elif isinstance(outputFilePath, str) and outputFilePath.strip() != '':
            outputFilePath = open(outputFilePath, 'w', encoding='UTF-8')
        else:
            return results

        
        print(f"Reference sequence : {self.__referenceSequence}", file=outputFilePath, end='\n'*2)
            
        for data in results:
            print(f"Portion of the reference sequence : {data[0]}", file=outputFilePath)
            print(f"Sequence queried : {data[1]}", file=outputFilePath)
            print(f"Position for the best alignment in the reference sequence : {data[2]}", file=outputFilePath)
            print(f"best scoring obtained : {data[3]}", file=outputFilePath, end='\n'*3)
            
        if outputFilePath != sys.stdout:
            outputFilePath.close()
        
        return results


    # DATA VALIDATION -------------------------------------------------------------------------
        
    def checkSequenceValidity(self, string:str)->bool:
        """checks whether a given sequence is valid or not (i.e contains correct characters)

        Args:
            string (str): the string to be checked

        Returns:
            result (bool): the result of the comparison
        """
        return all(item in {'A', 'C', 'G', 'T', '-', 'X'} for item in string) and string.strip() != ''
    
    
    ## DATA READING ---------------------------------------------------------------------------
    
    
    def readSequence(self, path:str)->str:
        """reads the reference sequence

        Args:
            path (str): the path to the txt file to be read.

        Returns:
            sequence (str): the sequence read 
        """
        
        with open(path, 'r', encoding='UTF-8') as fp:
            return ''.join(line.strip().upper() for line in  fp)
        
        
    def readQueryData(self, path:str)->List[str]:
        """reads the query data to be aligned

        Args:
            path (str): The path to the file containing the data to be aligned.

        Returns:
            sequences (list[str]): the list of sequences to be matched 
        """
        
        with open(path, 'r', encoding='UTF-8') as fp:
            return list(map(lambda line:line.strip().upper(), fp))
        
        
    ## GETTERS ------------------------------------------------------------------------------------ 
    def getReferenceSequence(self)->str:
        """returns the reference sequence 

        Returns:
            reference sequence (str): the reference sequence
        """
        return self.__referenceSequence
    
        
    def getQuerySequence(self)->List[str]:
        """returns the list of sequence to be queried

        Returns:
            queries (list[str]): the list of queries 
        """
        return list(self.__querySequence) if self.__querySequence else None
        
        
    ## SETTERS ------------------------------------------------------------------------------------
    def setReferenceSequence(self, referenceSequence:str)->None:
        """sets the new reference sequence to be used

        Args:
            referenceSequence (str): the new reference sequence

        Raises:
            ValueError: if the reference sequence is not correct
        """
        referenceSequence = referenceSequence.strip().upper()
        if self.checkSequenceValidity(referenceSequence):
            self.__referenceSequence = referenceSequence
        else:
            raise ValueError('Invalid reference sequence')
        
        
    def setQuerySequence(self, queries:List[str])->None:
        """sets the new list of queries

        Args:
            queries (list[str] | set[str]): the list (or set) of queries to be used

        Raises:
            ValueError: if one of the query contains a strange character (i.e. not in A,C,G,T,-,X)
        """
        queries = list(map(lambda x:x.strip().upper(), queries))
        
        for data in queries:
            if not self.checkSequenceValidity(data):
                raise ValueError(f'Invalid queries sequence, raised an error query : {data}')
            
        self.__querySequence = list(queries)