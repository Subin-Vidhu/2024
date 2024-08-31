import pandas as pd
import chromadb
import uuid
import os

class Portfolio:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        self.file_path = os.path.join(current_dir, "resource", "my_portfolio.csv")
        self.data = pd.read_csv(self.file_path)
        vectorstore_path = os.path.join(parent_dir, "vectorstore")
        self.chroma_client = chromadb.PersistentClient(vectorstore_path)
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
