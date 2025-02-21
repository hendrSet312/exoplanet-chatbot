from groq import Groq
import regex as re
import pandas as pd
from langchain_groq import ChatGroq
from langchain import LLMChain
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain.chains import create_history_aware_retriever,ConversationalRetrievalChain, StuffDocumentsChain
from langchain_core.prompts import MessagesPlaceholder
from langchain.schema import Document
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor


class SentenceTransformerEmbeddings:
    """LangChain wrapper for SentenceTransformer embeddings."""
    def __init__(self):
        self.embeddings  = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def __call__(self,text):
        return self.embed_query(text)

    def embed_documents(self, texts):
        return [self.embeddings.encode(text, normalize_embeddings=True).tolist() for text in texts]

    def embed_query(self, texts):
        return self.embeddings.encode(texts, normalize_embeddings=True).tolist()

class chatbot:
    def __init__(self,apikey:str):
        self.__apikey = apikey
        self.__temperature = 0.5
        self.__max_completion_tokens = 4096
        self.__model = "llama-3.1-8b-instant"
        self.__embeddings = SentenceTransformerEmbeddings()
        self.__client =ChatGroq(
            groq_api_key= self.__apikey,  # Replace with your actual API key
            model_name=self.__model, 
            temperature=self.__temperature, 
            max_tokens=self.__max_completion_tokens,
            streaming= True,
            stop_sequences= None,
        )

    def create_retrieval(self, result_model, result_insight):
        # Convert input model to string
        input_model = result_model['input'].to_string(index=False)
        
        docs = [
            Document(page_content=f"""
                input model = {input_model}
                result = {result_model['number']} ({result_model['label']})
                SHAP insight = {result_insight}
            """, metadata={"source": "input_model"})
        ]
        
        # Create vector store
        vector_store = FAISS.from_texts(
            texts=[doc.page_content for doc in docs],
            embedding=self.__embeddings,
            metadatas=[doc.metadata for doc in docs]
        )
        
        # Create base retriever
        base_retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3},
        )

        return base_retriever
    
    def generate_aware_history(self, retriever):
        # Definisikan prompt template dengan input_variables yang eksplisit
        question_generator_prompt = ChatPromptTemplate.from_messages([
            ("system", """Given a chat history and the latest user question \
            which might reference context in the chat history, formulate a standalone question \
            which can be understood without the chat history. Do NOT answer the question, \
            just reformulate it if needed and otherwise return it as is."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ]).partial(chat_history=[])

        # Buat history aware retriever
        history_aware_retriever = create_history_aware_retriever(
            llm=self.__client,
            retriever=retriever,
            prompt=question_generator_prompt
        )
        
        return history_aware_retriever
    

    def generate_answer(self, retriever_result, question, tone) : 

        prompt = ChatPromptTemplate.from_messages([
            ("system", """Jawab pertanyaaan pengguna berdasarkan konteks dan nada bicara yang user inginkan
                        
                        - Petunjuk nada dan tingkat pengetahuan : 
                            1. Normal :
                                - Gunakan bahasa sederhana dan jelas tanpa istilah teknis yang rumit.
                                - Jelaskan konsep dengan cara yang mudah dipahami.
                                - Berikan panduan langkah demi langkah jika diperlukan.

                            2. Expert  (Peneliti, Profesional, Astronaut):
                                - Gunakan terminologi teknis yang tepat dan berikan penjelasan mendalam.
                                - Rujuk pada konsep akademis dan standar industri.
                                - Tawarkan wawasan dan analisis tingkat lanjut sesuai dengan konteks profesional.

                        Konteks : {context}
                        nada dan tingkat pengetahuan user : {tone}"""),
            ("user", "{input}"),
        ])
        
        llm_chain = LLMChain(llm = self.__client, prompt = prompt)
        response = llm_chain.run({
            "context": retriever_result,
            "tone": tone,
            "input": question
        })

        cleaned_text = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

        return cleaned_text 



class ShapInterpreter:
    def __init__(self,apikey:str):
        self.__apikey = apikey
        self.__temperature = 0.5
        self.__max_completion_tokens = 4096
        self.__model = "deepseek-r1-distill-llama-70b"
        self.__client =ChatGroq(
            groq_api_key= self.__apikey,  # Replace with your actual API key
            model_name=self.__model, 
            temperature=self.__temperature, 
            max_tokens=self.__max_completion_tokens,
            streaming= True,
            stop_sequences= None,
        )

    def _generate_system_prompt(self) -> str:
        return f"""
        Anda adalah AI tingkat lanjut dengan keahlian dalam astronomi dan disiplin STEM. Tugas Anda adalah menganalisis keluaran model prediksi kelayakhunian eksoplanet menggunakan dictionary yang berisi fitur sebagai key dan nilai SHAP fitur sebagai value. Pastikan Anda memberikan interpretasi terperinci tentang prediksi model, menganalisis dampak setiap fitur terhadap hasil prediksi, dan menyampaikan penjelasan sesuai dengan nada dan tingkat pengetahuan pengguna

        Nilai prediksi : 
        - 0 ( Tidak layak huni ) 
        - 1 ( Layak huni secara konservatif) 
        - 2 (Layak huni secara optimis)

        Struktur Data:
        1. Dictionary:
            - Key: Nama fitur (misal: "P_TEMP", "P_ESI")
            - Value: Nilai SHAP fitur (misal: -2.86, +0.47 )

	    Nada dan tingkat pengetahuan : 

        1. Normal :
            - Gunakan bahasa sederhana dan jelas tanpa istilah teknis yang rumit.
            - Jelaskan konsep dengan cara yang mudah dipahami.
            - Berikan panduan langkah demi langkah jika diperlukan.

        2. Expert  (Peneliti, Profesional, Astronaut):
            - Gunakan terminologi teknis yang tepat dan berikan penjelasan mendalam.
            - Rujuk pada konsep akademis dan standar industri.
            - Tawarkan wawasan dan analisis tingkat lanjut sesuai dengan konteks profesional.

        Output Analisis (3 bagian):
		1. Makna Prediksi: Berikan penjelasan yang jelas mengenai arti kategori prediksi kelayakhunian. Misalnya, jika model memprediksi "layak huni secara optimis," jelaskan dengan ringkas apa maksudnya.
		2. Identifikasi Fitur Utama: Temukan dan analisis empat fitur teratas yang paling berpengaruh terhadap prediksi model. Sertakan:
			- Jelaskan:
				- Nama fitur : Jelaskan apa yang direpresentasikan oleh fitur tersebut.
				- SHAP value : Tampilkan nilai SHAP, yang menunjukkan seberapa kuat pengaruh fitur tersebut.
				- Arah :  Jelaskan apakah fitur tersebut menaikkan atau menurunkan prediksi (contoh: "Fitur ini dengan nilai SHAP +0.45 secara signifikan meningkatkan prediksi menuju 'layak huni secara optimis'"
		3. Kesimpulan : Berikan kesimpulan mengenai temuan analisis, tekankan bagaimana fitur-fitur tersebut mempengaruhi prediksi model, serta pola atau observasi penting yang terlihat.

        Persyaratan Respons:
        - Pastikan interpretasi nilai numerik sejalan dengan data di dalam dictionary.
        - Respons harus terstruktur, ilmiah, dan selaras dengan nada bicara serta tingkat pengetahuan pengguna, sehingga lebih personal dan relevan.
        - Pastikan penjelasan mencakup nilai SHAP, arah pengaruh fitur, dan konsistensi interpretasi dengan data grafik yang diberikan.
        """


    def generate_insight(self,result: dict, tone : str) -> str:
        system_message = SystemMessagePromptTemplate.from_template(
            self._generate_system_prompt()
        )

        user_message = HumanMessagePromptTemplate.from_template(
            f"""
                    Nilai prediksi input : {result['number']} ({result['label']}) (persentase probabilitas : {result['probability']})
                    Dictionary fitur : {result['description']} 
                    Nada dan pengetahuan pengguna : {tone}
                    """
        )

        chat_prompt = ChatPromptTemplate.from_messages([system_message, user_message])

        llm_chain = LLMChain(llm=self.__client, prompt=chat_prompt)

        result = llm_chain.run({
            "system_content": self._generate_system_prompt(),
            "number": result['number'],
            "label": result['label'],
            "probability": result['probability'],
            "description": result['description'],
            "tone": tone
        })

        cleaned_text = re.sub(r"<think>.*?</think>", "", result, flags=re.DOTALL).strip()

        return cleaned_text
