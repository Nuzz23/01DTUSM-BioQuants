class Alignment():
    def __init__(self, pathReferenceSequence:str=None, pathQuerySequence:str=None, 
                    referenceSequence:str=None, querySequence:list[str]|set[str]=None):

        
                
        if (not pathReferenceSequence and not referenceSequence) or (not pathQuerySequence and not querySequence):
            raise ValueError('Incorrect inputs ')
        
        referenceSequence = referenceSequence or self.readSequence(path=pathReferenceSequence)
            
        if self.checkSequenceValidity(referenceSequence):
            self.__referenceSequence = referenceSequence.upper()
        else:
            raise ValueError('Incorrect reference sequence')
        
        querySequence = list(querySequence) if querySequence else self.readSequence(path=pathQuerySequence)
            
        for seq in querySequence:
            if not self.checkSequenceValidity(seq):
                raise ValueError('Incorrect query sequence')
            
        self.__querySequence = querySequence
    
    
    # DATA VALIDATION -------------------------------------------------------------------------
        
    def checkSequenceValidity(self, string:str)->bool:
        """checks whether a given sequence is valid or not (i.e contains correct characters)

        Args:
            string (str): the string to be checked

        Returns:
            result (bool): the result of the comparison
        """
        return set(string).difference({'A', 'C', 'G', 'T', '-', 'X'}).__len__() == 0
    
    
    ## DATA READING ---------------------------------------------------------------------------
    
    
    def readSequence(self, path:str)->str:
        """reads the reference sequence

        Args:
            path (str): the path to the txt file to be read.

        Returns:
            sequence (str): the sequence read 
        """
        
        with open(path, 'r', encoding='UTF-8') as fp:
            return ''.join(list(map(lambda line:line.strip().upper(), fp)))
        
        
    def readQueryData(path:str)->list[str]:
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
        
    def getQuerySequence(self)->list[str]:
        """returns the list of sequence to be queried

        Returns:
            queries (list[str]): the list of queries 
        """
        return list(self.__querySequence)
        
        
    ## SETTERS ------------------------------------------------------------------------------------
    def setReferenceSequence(self, referenceSequence:str)->None:
        """sets the new reference sequence to be used

        Args:
            referenceSequence (str): the new reference sequence

        Raises:
            ValueError: if the reference sequence is not correct
        """
        if self.checkSequenceValidity(referenceSequence.upper()):
            self.__referenceSequence = referenceSequence.upper()
        else:
            raise ValueError('Invalid reference sequence')
        
        
    def setQuerySequence(self, queries:list[str] | set[str])->None:
        """sets the new list of queries

        Args:
            queries (list[str] | set[str]): the list (or set) of queries to be used

        Raises:
            ValueError: if one of the query contains a strange character (i.e. not in A,C,G,T,-,X)
        """
        queries = list(map(lambda x:x.upper(), queries))
        
        for data in queries:
            if not self.checkSequenceValidity(data):
                raise ValueError(f'Invalid queries sequence, raised an error query : {data}')
            
        self.__referenceSequence = list(queries)