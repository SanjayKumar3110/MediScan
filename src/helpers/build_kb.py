import pandas as pd
import chromadb
from chromadb.utils import embedding_functions

# 1. Initialize Vector DB (Persistent)
chroma_client = chromadb.PersistentClient(path="./data/knowledge_base_db")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def build_specialty_mapper():
    # Load your CSV
    df = pd.read_csv("data/knowledge_base/symptoms_disease.csv") #
    
    collection = chroma_client.get_or_create_collection(name="specialty_mapper", embedding_function=sentence_transformer_ef)
    
    # Add to DB
    collection.add(
        documents=df['symptoms_list'].tolist(),     # What we search for ("chest pain")
        metadatas=df[['disease', 'specialist']].to_dict('records'), # The answer
        ids=[str(i) for i in range(len(df))]
    )
    print("✅ Specialty Mapper Built!")

def build_drug_encyclopedia():
    # Load your CSV
    df = pd.read_csv("data/knowledge_base/indian_medicines.csv").head(5000) # Start small
    
    collection = chroma_client.get_or_create_collection(name="drug_info", embedding_function=sentence_transformer_ef)
    
    # Combine relevant text for embedding
    df['embed_text'] = df['name'] + " - " + df['uses']
    
    collection.add(
        documents=df['embed_text'].tolist(),
        metadatas=df[['name', 'side_effects', 'manufacturer']].to_dict('records'),
        ids=[str(i) for i in range(len(df))]
    )
    print("✅ Drug DB Built!")

if __name__ == "__main__":
    build_specialty_mapper()
    build_drug_encyclopedia()