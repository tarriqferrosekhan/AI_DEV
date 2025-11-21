import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from EmbeddingManager import EmbeddingManager
from EmbeddingManager import Key
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

class EmbeddingVisualizer:
    def __init__(self):
        self.EmbeddingManager=EmbeddingManager()
        self.model=self.EmbeddingManager.GetEmbeddingModel()
        self.EmbeddingMethod=""
    
    def Visualize_TSNE_2D(self):
        vocab=list(self.EmbeddingManager.Vocabulary)
        vocab_vectors=self.EmbeddingManager.WordVectors
        tsne=TSNE(n_components=2,random_state=42,perplexity=2)
        reduced_result_vectors=tsne.fit_transform(vocab_vectors)
        plt.figure(figsize=(12,8))
        plt.scatter(reduced_result_vectors[:,0],reduced_result_vectors[:,1],marker='o')
        for i,word in enumerate(vocab):
            plt.annotate(word,(reduced_result_vectors[i,0],reduced_result_vectors[i,1]),fontsize=9,alpha=0.7)
        plt.title("Two Dimensional TSNE")
        plt.xlabel("Dimension 1")
        plt.ylabel("Dimension 2")
        plt.show()

    def Visualize_TSNE_3D(self):
        vocab=list(self.EmbeddingManager.Vocabulary)
        vocab_vectors=self.EmbeddingManager.WordVectors
        tsne=TSNE(n_components=3,random_state=42,perplexity=2)
        reduced_result_vectors=tsne.fit_transform(vocab_vectors)
        fig=plt.figure(figsize=(12,8))
        ax=fig.add_subplot(111,projection='3d')
        ax.scatter(reduced_result_vectors[:,0],reduced_result_vectors[:,1],reduced_result_vectors[:,2],marker='o')
        for i,word in enumerate(vocab):
            ax.text(reduced_result_vectors[i,0],reduced_result_vectors[i,1],reduced_result_vectors[i,2],word,fontsize=9)

        ax.set_title("3 Dimensional TSNE")
        ax.set_xlabel("Dimension 1")
        ax.set_ylabel("Dimension 2")
        plt.show()

    def Visualize_PCA_2D(self):
        vocab=list(self.EmbeddingManager.Vocabulary)
        vocab_vectors=self.EmbeddingManager.WordVectors
        pca=PCA(n_components=2)
        reduced_result_vectors=pca.fit_transform(vocab_vectors)
        fig=plt.figure(figsize=(12,8))
        plt.scatter(reduced_result_vectors[:,0],reduced_result_vectors[:,1])
        for i,word in enumerate(vocab):
            plt.text(reduced_result_vectors[i,0],reduced_result_vectors[i,1],word)

        plt.title("Two Dimensional PCA")
        plt.show()


EmbeddingVisualizer().Visualize_TSNE_3D()