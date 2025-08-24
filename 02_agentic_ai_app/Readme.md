### Agentic AI App Development
#### Introduction

*Please Note the Fundamental Difference in AI app dev vs classical App Dev is*
<ul>
  <li>AI App Dev - probabilistic (Let LLM and Frameworks decide the flow and execute it)</li>
  <li>Classical App Dev - deterministic (App Logic is predefined)</li>
</ul>
<ol>
  
<li><h3>In Simple terms tell me what an AI Agent does?</h3>
  <ul>
   <li>Reads User's Prompt</li>
   <li>Calls the Corresponding User Defined Function via an AI Agent Configuration</li>
   <li>This User Defined Function executes your application's logic</li>
  </ol>
</li>
<li>
  <b>How this AI Agent differs from the <a href='https://github.com/tarriqferrosekhan/AI_DEV/tree/main/01_rag_data_app/HelpMate.AI.Books' target='_blank'>HelpMate.AI.Books</a> RAG application we built earlier?</b>
  <table>
    <tr>
      <td>RAG</td>
      <td>Agentic AI</td>
    </tr>
    <tr>
      <td>
        <ul>
          <li>your enterprise data (books_gpt.csv) was exposed to LLM</li>
          <li>Via UI you interacted with your data to extract information based on certain conditions</li>
          <li><b>But Managing Application Logic Flow was not possible. </b></li>
        </ul>
      </td>
      <td>
        <ul>
          <li>You write User Defined Functions like Register, IssueBook, ReturnBook etc</li>
          <li>Expose your methods to an AI Agent</li>
          <li>Pass the User's prompt to AI Agent , which in-turn will call your method</li>
          
          
        </ul>
      </td>
    </tr>
  </table>
  <ul>
    <li>In the RAG Application </li>
    <li>An user InterfaceIn the RAG Application your enterprise data (books_gpt.csv) was exposed to LLM</li>
    
  </ul>
  
</li>
<li><b>So how does An Agent Configuration would look like?</b>
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
   a. In the  your enterrpise data was exposed to LLM , allow user's to chat with the data via LLM
3.  
</ul>

Ingredients: 
- [OpenAI LLM](https://platform.openai.com/docs/models)
- [Llama Index Agent](https://docs.llamaindex.ai/en/stable/understanding/agent/)
- Two Approaches :
1. Agentic Tools (FunctionAgent
2. WorkFlow to build 
