# Weather.OpenAI.MCP

## How to Execute this code
1. Pull this code to your local folder
2. Ensure to have an active Open AI Account and the Secret key is saved in local .env file

   **OPENAI_API_KEY=<Your_KEY>**
   
3. Ensure to Server.py and Client.py are placed in same folder (just in case)
4. Open a new a terminal (from the location where Server.py is saved) and run below command to launch the server:
   
  **py server.py**
  
  *Please note after above command server will print anything. so move on to below step if not getting any error*
  
4. Open another terminal (from the same location where Client.py is saved) and run below command to launch the client
   
   **py client.py server.py**

## Process Flow
<ul>
<li>User asks a natural-language query (“Weather for NYC + Alerts for CA”).</li>
<li>LLM decides which tools to call → get_forecast and get_alerts.</li>
<li>MCP Client executes both tool calls in parallel against the MCP Server.</li>
<li>MCP Server queries the NWS API endpoints in parallel (/points+forecast and /alerts).</li>
<li>Results flow back up: NWS → MCP Server → MCP Client → LLM.</li>
<li>The LLM synthesizes the tool outputs into a natural-language answer for the User.</li>
</ul>

<img width="300" height="350" alt="image" src="https://github.com/user-attachments/assets/c34f56ce-1d42-43a8-91b2-d894e996125d"/>

