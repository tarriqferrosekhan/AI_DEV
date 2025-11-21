from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import os
os.system('cls')

class Key:
    class EmbeddingAlgorithms:
        Word2Vec="Word2Vec"

class EmbeddingManager:
    def __init__(self):
        self.current_directory = os.getcwd()
        self.folder_name = "DataSource"
        self.absolute_folder_path = ""
        self.directory_path = "" 
        self.txt_files = ""
        self.lines=[]
        self.tokens=None
        self.Vocabulary=None
        self.model=None
        self.CurrentEmbeddingAlgorithm=""
        self.WordVectors=None
        self.init()

    def init(self):
        self.absolute_folder_path = os.path.join(self.current_directory, self.folder_name)
        self.directory_path = Path(self.absolute_folder_path)  # Replace with your target directory
        self.txt_files = list(self.directory_path.glob('*.txt'))

    def importDataSources(self):
        try:
            if len(self.lines)>0:
                return
            for txt_file in self.txt_files:
                with open(txt_file, 'r') as file:
                    _content=file.read()
                    self.lines.extend(_content.splitlines())
            print("imported...")
            print(self.lines)
        except Exception as e:
            print(e)
    
    def GetWord2VecVocab(self):
        _vocab=[]
        if self.model!=None:
            _vocab=list(self.model.wv.index_to_key)
        return _vocab
    
    def GetWord2VecModel(self,_tokens):
        _model=None
        try:
            _model=Word2Vec(sentences=_tokens,vector_size=300,window=2,min_count=1,workers=4,sg=1)
        except Exception as e:
            print(e)
        return _model
    
    def GetTokens(self):
        _tokens=None
        try:
            if len(self.lines)==0:
                self.importDataSources()
            _tokens=[line.lower().split() for line in self.lines]
        except Exception as e:
            print(e)
        return _tokens
    
    def GetWord2Vec_Vectors(self,_model,_vocab):
        _Word_Vectors=None
        try:
            _Word_Vectors=np.array([_model.wv[word] for word in _vocab])
        except Exception as e:
            print(e)
        return _Word_Vectors
 
    def GetEmbeddingModel(self,embedding_method="Word2Vec"):
        _model=None
        try:
            self.tokens=self.GetTokens()
            if embedding_method==Key.EmbeddingAlgorithms.Word2Vec:
                self.CurrentEmbeddingAlgorithm=Key.EmbeddingAlgorithms.Word2Vec
                _model=self.GetWord2VecModel(self.tokens)
                if _model!=None:
                    self.model=self.GetWord2VecModel(self.tokens)
                    self.Vocabulary=self.GetWord2VecVocab()
                    self.WordVectors=self.GetWord2Vec_Vectors(self.model,self.Vocabulary)
        except Exception as e:
            print(e)
        return _model
    
    def GetSimilarWords(self,_Word,_topn=3,_positive=[],_negative=[]):
        similar_words=None
        try:
            if self.model==None:
                return
            if self.CurrentEmbeddingAlgorithm==Key.EmbeddingAlgorithms.Word2Vec:
                similar_words=self.model.wv.most_similar(_Word,topn=_topn)
        except Exception as e:
            print(e)
        return similar_words

_embed=EmbeddingManager()
_model=_embed.GetEmbeddingModel()
print(_model)
print(_embed.tokens)
print(_embed.GetSimilarWords("cat"))
print("Word vectors")
print(_embed.WordVectors)






    
