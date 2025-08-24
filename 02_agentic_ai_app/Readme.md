### Agentic AI App Development
#### Introduction
<ol>
  <li>Pre-Read:<br>
    <a href='https://arxiv.org/abs/2505.10468'>AI Agents vs. Agentic AI</a> </li><br>
<p>
<b>Agentic AI:</b> The comprehensive system that exhibits autonomy, reasoning, and planning to achieve a complex, high-level goal.<br>
It orchestrates the activity of individual AI agents and adapts its strategy based on feedback.<br>
<b>AI agents:</b> The individual, task-specific components that execute the sub-tasks required by the agentic AI framework.<br>
An agent may use tools, memory, and specialized skills to complete its assignment. 
</p>
  
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
  <li><b>What are the ✅ Pros of an AI Agent ?</b><br>
   - Application Logic is not Predefined.<br>
   - <b>Enables User Centred App Flow </b><br>
   - Can enable rendering the that part of the UI (Widget - say, register User) that the User needs <br>
   - For instance, when user says "register me" only (then) registration form is displayed.
  </li>
  <li><b>What are the ❌ Cons of an AI Agent ?</b><br>
   - <b>Probabilistic</b> - Harder to enforce strict control flow.<br>
   - May hallucinate tool calls if not grounded well.<br>
   - Debugging reasoning steps can be tricky.<br>
  </li>
  <li>
    <b>Any Alternative to make it more deterministic?</b><br>
    - Yes, you can use <a href='https://docs.llamaindex.ai/en/stable/understanding/workflows/' target='_blank'>Workflows</a>
  </li>
 </ol>
