import os
import openai
import pandas as pd
import csv
from llama_index.core import VectorStoreIndex,Document,SummaryIndex
from llama_index.llms.openai import OpenAI
from llama_index.core.prompts import PromptTemplate
from llama_index.core import Settings
from Utils import Utils
from AppConfig import AppConfig
from AppMessage import AppMessage,MessageType

class BooksRAG:
	def __init__(self):
		self.base_path = os.getcwd()+"\\"
		self.path_books=self.base_path
		self.path_api_key=self.base_path
		self.appconfigfileName=self.base_path+"appConfig.json"
		self.appconfig:AppConfig=None
		self.important_columns = ['Genre', 'Publication Year', 'Page Count', 'Price (INR)']
		self.RecommendedAttributes="'Genre', 'Publication Year', 'Page Count', 'Price (INR)'"
		self.DataSource=pd.DataFrame([])
		self.Documents=[]
		self.Init()

	def Init(self):
		self.appconfig=Utils.getJSONAsClass(AppConfig,self.appconfigfileName)
		self.path_api_key=self.path_api_key+self.appconfig.api_key_file_name
		with open(self.path_api_key, "r") as f:
			openai.api_key = ' '.join(f.readlines())
		self.path_books=self.path_books+self.appconfig.data_source_file_name
		self.GetSourceData()
		self.CreateDocuments()

	def	GetSourceData(self):
		col_Price='Price (INR)'
		df=pd.read_csv(self.path_books, quoting=csv.QUOTE_ALL,quotechar='"', encoding='utf-8')
		df[col_Price] = df[col_Price].str.replace(',', '').astype(int)
		self.DataSource=df
		return self.DataSource
	
	def CreateDocuments(self):
		for idx, row in self.DataSource.iterrows():
			content = "\n".join([f"{col}: {row[col]}" for col in self.important_columns])
			self.Documents.append(Document(text=content, metadata={"row": idx}))


	def moderation_check(self,user_input):
		# Call the OpenAI API to perform moderation on the user's input.
		response = openai.moderations.create(model=self.appconfig.moderation_model,input=user_input)
		# Extract the moderation result from the API response.
		# Check if the input was flagged by the moderation system.
		if response.results[0].flagged == True:
			return Utils.Keys.Flagged
		else:
			return Utils.Keys.NotFlagged

	def llamaindex_intent_confirmation_layer(self,prompt_query):
		index = VectorStoreIndex.from_documents(self.Documents)
		_llm=OpenAI(model=self.appconfig.base_llm, temperature=0)
		Settings.llm = OpenAI(model=self.appconfig.base_llm, temperature=0)
		binary_prompt = PromptTemplate(
			"You are verifying product specifications based ONLY on the following context.\n"
			"If the information is found, answer 'Yes'.\n"
			"If the information is missing or unclear, answer 'No'.\n"
			"Be strictly based on context. Do not guess.\n"
			"Context:\n{context_str}\n\n"
			"Question: {query_str}\n"
			"Answer:"
		)
		query_engine = index.as_query_engine(
				llm=_llm,
				text_qa_template=binary_prompt,
			similarity_top_k=self.appconfig.similarity_top_k 
		)
		# Query
		response = query_engine.query(prompt_query)
		retrieved_nodes=query_engine.retrieve(prompt_query)
		return response,retrieved_nodes,self.Documents

	def compute_match_score(self,doc_text, query_text):
		total_score = 0
		for attr in self.important_columns:
			if attr.lower() in doc_text.lower():
				# Extract attribute value
				attr_value_start = doc_text.lower().find(attr.lower()) + len(attr) + 2
				attr_value_end = doc_text.lower().find('\n', attr_value_start)
				attr_value = doc_text[attr_value_start:attr_value_end if attr_value_end != -1 else None].strip()

				if attr_value:
					attr_value_lower = attr_value.lower()
					query_lower = query_text.lower()

					# 3 points → Strong match: full attribute value found
					if attr_value_lower in query_lower:
						total_score += 3
					# 2 points → Medium match: all keywords from attribute found separately
					elif all(word in query_lower for word in attr_value_lower.split()):
						total_score += 2
					# 1 point → Weak match: any keyword from attribute found
					elif any(word in query_lower for word in attr_value_lower.split()):
						total_score += 1
		return total_score

	def mapProductsByScoring(self,retrieved_nodes,query):
		scored_results = []
		dictionary_ScoredResults=[]
		score_threshold=1
		for node in retrieved_nodes:
			text = node.node.text
			match_score = self.compute_match_score(text, query)
			if match_score>=score_threshold:
				item={}
				item["Score"]=match_score
				for _text in text.split("\n"):
					key=_text.split(":")[0].strip()
					value=_text.split(":")[1].strip()
					item[key]=value
					dictionary_ScoredResults.append(item)
		dfScoredResult=pd.DataFrame.from_dict(dictionary_ScoredResults)
		return dfScoredResult

	def information_extraction(self,dfScoredResult):
		df=self.DataSource
		filtered_df=df.copy()
		new_df=pd.DataFrame([])
		if dfScoredResult.empty==False: #and ["Publication Year",'Page Count','Price (INR)'] in dfScoredResult.columns.tolist():
			dfScoredResult['Publication Year']=dfScoredResult['Publication Year'].astype(int)
			dfScoredResult['Page Count']=dfScoredResult['Page Count'].astype(int)
			dfScoredResult['Price (INR)']=dfScoredResult['Price (INR)'].astype(float)
			new_df = pd.merge(
				left=df,
				right=dfScoredResult,
				how='inner',
				left_on=['Genre', 'Publication Year', 'Page Count', 'Price (INR)'],
				right_on=['Genre', 'Publication Year', 'Page Count', 'Price (INR)'],
			)
		return (new_df)

	def process(self,query):
		_appMessage=AppMessage()
		moderation = self.moderation_check(query)
		if moderation==Utils.Keys.Flagged:
			_appMessage.Response_Message=Utils.Messages.Flagged
			_appMessage.Message_Type=MessageType.Warnings
		else:
			response_intent,retrieved_nodes,documents=self.llamaindex_intent_confirmation_layer(query)
			if response_intent.response=='No':
				_appMessage.Response_Message=Utils.Messages.CannotProcess
				_appMessage.Message_Type=MessageType.Warnings
			else:
				scored_results=self.mapProductsByScoring(retrieved_nodes,query)		
				if len(scored_results)==0:
					_appMessage.Response_Message=Utils.Messages.RewordPrompt.format(self.RecommendedAttributes)
					_appMessage.Message_Type=MessageType.Warnings
				else:
					filtered_df=self.information_extraction(scored_results)
					_appMessage.Data=filtered_df.drop_duplicates()
					_appMessage.Message_Type=MessageType.Success
		return _appMessage
