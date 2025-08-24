### Agentic AI App Development
#### Introduction
<ul>
<li><b>In Simple terms tell me what an AI Agent is:</b>
  <ol>
   <li>Reads User's Prompt</li>
   <li>Calls the Corresponding User Defined Function via an Agent Configuration</li>
   <li>This User Defined Function executes your application's logic</li>
  </ol>
 <li>So how does An Agent Configuration would look like?
     <ol>
       <li>
         It takes minimum 3 parameters for the configuration (may vary basis the type of Agent)
          <ul>
              <li>List of User Defined Functions to call</li>
              <li>LLM of your choice ( in our demo we use Open AI models)</li>
              <li>Prompt that indicates which function to call basis the scenario</li>
          </ul>         
       </li>
     </ol>
   </li>
    
   2. What's the difference compared to the RAG App:
   a. In the [RAG App](https://github.com/tarriqferrosekhan/AI_DEV/tree/main/01_rag_data_app/HelpMate.AI.Books) your enterrpise data was exposed to LLM , allow user's to chat with the data via LLM
3.  
</ul>

Ingredients: 
- [OpenAI LLM](https://platform.openai.com/docs/models)
- [Llama Index Agent](https://docs.llamaindex.ai/en/stable/understanding/agent/)
- Two Approaches :
1. Agentic Tools (FunctionAgent
2. WorkFlow to build 
