# Weather.OpenAI.NOMCP

## How to execute this code

1. Pull this code to your local directory
2. Ensure to have an active Open AI Account and the Secret key is saved in local .env file

   **OPENAI_API_KEY=<Your_KEY>**
   
3. Ensure to Server.py and Client.py are placed in same folder (just in case)
4. Open a new a terminal (from the location where Server.py is saved) and run below command to launch the server:
   
  **uvicorn server:app --reload --host 0.0.0.0 --port 8000**
  
4. Open another terminal (from the same location where Client.py is saved) and run below command to launch the client
   
   **py client.py**
## Process Flow
<ul>
<li>The User asks the LLM for weather + alerts.</li>
<li>The LLM decides to call the two functions (get_forecast,  | get_alerts).)</li>
<li>These functions are handled by a custom wrapper (manually coded by developers).</li>
<li>The wrapper calls the Weather API in parallel (/points → /forecast and /alerts).</li>
<li>Results return → wrapper → LLM → natural language answer for the user.!</li>
</ul>

<img width="300" height="350" alt="image" src="https://github.com/user-attachments/assets/352a0e1f-2ce7-4264-ab4e-bd133dfe3e44" />
