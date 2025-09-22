# Weather.RESTAPI

## How to Execute this Code   
1. Pull to your local repo
2. Ensure to Server.py and Client.py are placed in same folder (just in case)
3. Open a new a terminal (from the location where Server.py is saved) and run below command to launch the server:
   
  **uvicorn server:app --reload --host 0.0.0.0 --port 8000**
  
4. Open another terminal (from the same location where Client.py is saved) and run below command to launch the client
   
   **py client.py**

## Process Flow
 <ul>
   <li>UI presents options: “Get Alerts” and “Get Forecasts.”</li>
   <li>User selects “Get Alerts”,Inputs Country Code : “IN” (India)</li>
   <li>UI invokes Client->calls->Server->calls->public weather API</li>
   <li>Response from Public API is propagated back to user</li>
   <li>Same Process followed for Forecast when requested by user.</li>
 </ul>
<br>
<img width="300" height="350" alt="image" src="https://github.com/user-attachments/assets/a26f4a17-4bc7-4c87-8bb1-f495b33a41b2" />
