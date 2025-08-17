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
1. User Prompt is passed to Books.RAG Component.
2. **Moderation Layer - Guard Rails**:
   1. Checks the prompt for any Illegal or Unethical Query using [OpenAI Moderation API](https://platform.openai.com/docs/guides/moderation)
   2. The response message is Flagged if inappropriate otherwise returned as "Not Flagged"
   3. If Flagged a warning message is returned to User.
4. **Intent Confirmation Layer**
    1. This Layer helps to check if the User Prompt is not out of context.
    2. [**temperature=0**](https://community.openai.com/t/cheat-sheet-mastering-temperature-and-top-p-in-chatgpt-api/172683)  is used to avoid LLM going out of context.
    3. Takes care of [Prompt Injection attacks](https://www.ibm.com/think/topics/prompt-injection) and returns a Warning.
    4. 
    5. Creates Document from Data Source using [Vector Store Index](https://docs.llamaindex.ai/en/stable/module_guides/indexing/vector_store_index/)
    6. Instantials OpenAI model [GPT 3.5 turbo](https://platform.openai.com/docs/models/gpt-3.5-turbo)
    7. 
    8.  [PromptTemplate] (https://docs.llamaindex.ai/en/v0.10.17/api_reference/prompts.html) is created to set the context to return "Intent Yes" if the Query is not Out of Context , othwerwise returns "No"
    9. [Vector Store Index's Query Engine](https://docs.llamaindex.ai/en/stable/module_guides/indexing/vector_store_guide/) is used to query the In-Memory Vector Document Store, using the : LLM , Prompt Template with similarity_top_k setting (from AppConfig)
    10. Response with retreived Nodes and Documents is returned.
    11. 
    
5. **Product **
#####  Moderation
##### Agentic Version of Same App in next Section




