#[WIP]
### Introduction to RAG Application
### Retrieval Augmented Generation Application:
<ol>
  <li>Your enterprise Data indexed as Documents</li>
  <li>Exposed to LLM accessed via standard interface like ChatBot through a query engine</li>
  <li>Benefit - No Retraining LLM of the Domain specific data and No Hallucinations.</li>
  
</ol>

#### Key Components:
1. Knowledge Base - Your Data (eg., csv, PDF)
2. The Retreiver - using [LLAMAINDEX](https://docs.llamaindex.ai/en/stable/module_guides/indexing/) or [LANGCHAIN](https://python.langchain.com/api_reference/index.html)
3. Integration layer - Moderation, Checking the Intent , Scoring mechanism (optional) 
4. Generation - Generating the final output basis the Prompt.

#### HelpMateAI.Books RAG Application
1. This [application](https://github.com/tarriqferrosekhan/AI_DEV/tree/main/01_rag_data_app/HelpMate.AI.Books) is built using : OpenAI - [GPT 3.5 turbo](https://platform.openai.com/docs/models/gpt-3.5-turbo) and [LLAMAINDEX](https://docs.llamaindex.ai/en/stable/module_guides/indexing/vector_store_index/)'s Vector and Summary Indexes
##### Application Architecture
<img width="1208" height="672" alt="image" src="https://github.com/user-attachments/assets/e380ffd9-01db-4e32-96e9-ac93a8b8eb9c" />

##### Process Steps
##### Prompt Injection, Jailbreaks, Moderation
##### Agentic Version of Same App in next Section




