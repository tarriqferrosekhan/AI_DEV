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
<img width="1215" height="678" alt="image" src="https://github.com/user-attachments/assets/f1622cc8-b15b-46e4-8688-443def1dc9c6" />

##### Process Steps
1. User Prompt is passed to Books.RAG Component.
2. **Moderation Layer - Guard Rails**:
   1. Checks the prompt for any Illegal or Unethical Query using [OpenAI Moderation API](https://platform.openai.com/docs/guides/moderation)
   2. The response message is Flagged if inappropriate otherwise returned as "Not Flagged"
   3. If Flagged a warning message is returned to User.
4. **Intent Confirmation Layer**
    1. This Layer helps to check if the User Prompt is **Not** out of context.
    2. Uses a [**temperature=0**](https://community.openai.com/t/cheat-sheet-mastering-temperature-and-top-p-in-chatgpt-api/172683) setting to avoid LLM going out of context.
    3. Takes care of [Prompt Injection attacks](https://www.ibm.com/think/topics/prompt-injection) as well and returns a Warning, if the  intent response is "No". 
    5. Creates [Document](https://docs.llamaindex.ai/en/stable/module_guides/loading/documents_and_nodes/) from Data Source.
    6. Creates [Vector Store Index](https://docs.llamaindex.ai/en/stable/module_guides/indexing/vector_store_index/)
    7. Instantials OpenAI model [GPT 3.5 turbo](https://platform.openai.com/docs/models/gpt-3.5-turbo)
    8. [PromptTemplate] (https://docs.llamaindex.ai/en/v0.10.17/api_reference/prompts.html) is created to set the context to return "Intent Yes" if the Query is not Out of Context , othwerwise returns "No
    9. [Vector Store Index's Query Engine](https://docs.llamaindex.ai/en/stable/module_guides/indexing/vector_store_guide/) is used to query the In-Memory Vector Document Store, using the : LLM , Prompt Template with similarity_top_k setting (from AppConfig)
    11. Response with retreived Nodes and Documents is returned. 
5. **Product Mapping, Scoring and Result**:
   1. Expects Few Attributes as mandatory attributes in the User Prompt.
   2. If user out of context shows warning.
   3. Basis the Match of User Prompt and Document Nodes a Scoring is done.
   4. Basis the Score the Node is retrieved and returns results.
   5. Tested successfully for [Prompt Injection](https://www.ibm.com/think/topics/prompt-injection) and [Jailbreak prompts - DAN, STAN, DUDE & Mongo Tom](https://gist.github.com/coolaj86/6f4f7b30129b0251f61fa7baaa881516)
6. **App Demo**<br>
**Information Extraction**<br>
  ![app_demo_information_extraction](https://github.com/user-attachments/assets/e8eb918d-97eb-4414-8c45-28fde3ac6f88)
 **Tested for Moderation**:<br>
  ![app_demo_moderation_check](https://github.com/user-attachments/assets/69c540e1-ae8e-490d-ad9d-a2481a416793)
**Tested for Prompt Injection attack prevention**<br>
  ![app_demo_prompt_injection](https://github.com/user-attachments/assets/89453c14-7f81-45e3-91b6-df002db2f828)
**Tested for Jail Break Prompts (DAN, STAN, DUDE and Mongo Tom Prompt)**<br>   
**Tested for Mongo Tom Prompt** <br>
TBD
**Tested for DAN , STAN, DUDE** <br>
      



