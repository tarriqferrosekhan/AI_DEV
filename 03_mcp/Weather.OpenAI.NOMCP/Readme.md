1. Ensure to have an active Open AI Account and the Secret key is saved in local .env file

   **OPENAI_API_KEY=<Your_KEY>**
   
3. Ensure to Server.py and Client.py are placed in same folder (just in case)
4. Open a new a terminal (from the location where Server.py is saved) and run below command to launch the server:
   
  **uvicorn server:app --reload --host 0.0.0.0 --port 8000**
  
4. Open another terminal (from the same location where Client.py is saved) and run below command to launch the client
   
   **py client.py**
