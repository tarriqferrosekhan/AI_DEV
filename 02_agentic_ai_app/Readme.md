### Agentic AI App Development
#### Introduction
<ol>
  <li><h3>In Simple terms tell me what an AI Agent does?</h3>
    <ul>
     <li>Reads User's Prompt</li>
     <li>Calls the Corresponding User Defined Function via an AI Agent Configuration</li>
     <li>This User Defined Function executes your application's logic</li>
    </ul>
  </li>
<li>
  <b>How this AI Agent differs from the <a href='https://github.com/tarriqferrosekhan/AI_DEV/tree/main/01_rag_data_app/HelpMate.AI.Books' target='_blank'>HelpMate.AI.Books</a> RAG application we built earlier?</b>
  <br>
  <table>
    <tr>
      <td>RAG</td>
      <td>Agentic AI</td>
    </tr>
    <tr>
      <td>
        - Your enterprise data (books_gpt.csv) was exposed to LLM.<br>
        - Via UI you interacted with your data to extract information based on certain conditions.<br>
        - <b>But Managing Application Logic Flow was not possible. </b><br>
      </td>
      <td>
          - You write User Defined Functions & Expose your methods to an <a href='https://docs.llamaindex.ai/en/stable/use_cases/agents/'  target='_blank'>AI Agent</a> or a <a href='https://docs.llamaindex.ai/en/stable/understanding/workflows/' target='_blank'>Workflow</a><br>
          - Pass the User's prompt to AI Agent , which in-turn will (or supposed to) call your method<br>
          - For eg., when user says "register me" the user defined function <b>register()</b> will be triggered by the Agent<br>
      </td>
    </tr>
  </table>
 </li>
 <li><b>Difference between an Agent and Workflow ,  are the Pros and Cons here here?</b><br> 
   ✅ Pros<br>
   - <b>Enables User Centred App Design and can evolve over the period of time.</b><br>
   - Application Logic is not Predefined.<br>
   - UI Will render only that Widget (say, register User) that the User is intended to interact with.<br>
   
 </li>
 <li>
   
 </li> 
 </ol>
