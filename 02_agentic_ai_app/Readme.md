# WIP - Yet to be Published.
Author: [TarriqFerroseKhan](https://www.linkedin.com/in/tarriq-ferrose-khan-ba527080)
### Agentic AI App Development
#### Introduction
<b>This Article details the Agentic AI, AI Agents (using LLAMAINDEX) and demonstrates a sample app.</b><br>
<b>Pre-Read:</b><br>
<ol>
  <li>
    <a href="https://www.ibm.com/think/topics/reinforcement-learning" target="_blank">What is reinforcement learning?</a>

  </li>
    <li>
    <a href='https://arxiv.org/abs/2505.10468'>AI Agents vs. Agentic AI</a> 
  </li>

  <br>
<p>
<b>Agentic AI:</b> The comprehensive system that exhibits autonomy, reasoning, and planning to achieve a complex, high-level goal.<br>
It orchestrates the activity of individual AI agents and adapts its strategy based on feedback.<br>
<b>AI agents:</b> The individual, task-specific components that execute the sub-tasks required by the agentic AI framework.<br>
An agent may use tools, memory, and specialized skills to complete its assignment. 
</p>
</ol>
<ol>
  <li><h3>In Simple terms tell me what an AI Agent does?</h3>
    <ul>
     <li>Reads User's Prompt</li>
     <li>Calls the Corresponding User Defined Function via an AI Agent (or Worflow)</li>
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
        - <b>But Managing Application Logic Flow was not intended. </b><br>
      </td>
      <td>
          - You write User Defined Functions & Expose your methods to an <a href='https://docs.llamaindex.ai/en/stable/use_cases/agents/'  target='_blank'>AI Agent</a> or a <a href='https://docs.llamaindex.ai/en/stable/understanding/workflows/' target='_blank'>Workflow</a><br>
          - Pass the User's prompt to AI Agent , which in-turn will (or supposed to) call your method<br>
          - For eg., when user says "register me" the user defined function <b>register()</b> will be triggered by the Agent<br>
      </td>
    </tr>
  </table>
 </li>
 <li><b>Difference between LlamaIndex Agent and WorkFlow?</b><br>
  <table>
    <tr>
      <td>Sections</td>
      <td><a href='https://docs.llamaindex.ai/en/stable/use_cases/agents/'  target='_blank'>Agent</a></td>
      <td><a href='https://docs.llamaindex.ai/en/stable/understanding/workflows/' target='_blank'>Workflow</a></td>
    </tr>
    <tr>
      <td>Purpose</td>
      <td>Agents are designed for dynamic decision-making and tool use</td>
      <td>Workflows define deterministic, step-by-step pipelines.</td>
    </tr>
    <tr>
      <td>How It Works </td>
      <td>
        - Write and Configure a Set of tools/functions (e.g., SQL query engine, search tool, custom function)<br>
        - The LLM decides when and which tool (Eg., User Defined Function) to call, based on the user prompt.<br>
        - Typically uses reasoning traces (like <a href="https://www.ibm.com/think/topics/react-agent">ReAct</a>) or function-calling to orchestrate.<br>
      </td>
      <td>
        - Explicitly define steps (@step) and transitions (via Event / StopEvent).<br>
        - The Workflow engine executes steps in a controlled order.<br>
        - <b>The Flow is developer-defined, not LLM-driven.</b>
      </td>
    </tr>
    <tr>
      <td>
        Best for
      </td>
      <td>
        - Natural conversations where the LLM has to pick the right tool.<br>
        - Cases where logic is not strictly sequential (e.g., chatbot, Q&A, multi-tool workflows).<br>
      </td>
      <td>
      - Business processes, multi-step forms, approvals, UI-driven flows.<br>
      - Agentic RAG pipelines with well-defined stages (retrieval → reasoning → response).<br>
      </td>
    </tr>
    <tr>
      <td>✅ Pros</td>
      <td>
        - Flexible, LLM decides dynamically.<br>
        - Faster to implement.<br>
        - Works well when tasks are loosely structured.<br>
      </td>
      <td>
      - Deterministic and predictable.<br>
      - Easier to debug.<br>
      - Good for UI workflows (registration, issue handling, etc.).<br>
      </td>
    </tr>
    <tr>
      <td>❌ Cons</td>
      <td>
        - Harder to enforce strict control flow.<br>
        - May hallucinate tool calls if not grounded well.<br>
        - Debugging reasoning steps can be tricky.<br>
      </td>
      <td>
        - More boilerplate.<br>
        - Less flexible — flow is fixed, not adaptive.<br>
        - Overkill for simple tasks.
      </td>
    </tr>
    <tr>
      <td>
        Sample Code
      </td>
      <td>
        <a href="https://github.com/tarriqferrosekhan/AI_DEV/blob/main/02_agentic_ai_app/AgentApp/agent_books.py">Agent Sample Code</a>
      </td>
      <td>
        <a href="https://github.com/tarriqferrosekhan/AI_DEV/blob/main/02_agentic_ai_app/WorkFlowApp/workflow_books.py">Workflow Sample Code</a>
      </td>
    </tr>
  </table>
  </li>
  </ol>
