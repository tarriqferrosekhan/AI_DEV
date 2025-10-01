import os
import warnings
import vertexai
from google.cloud import language_v1

from google.auth import credentials
from vertexai.generative_models import GenerativeModel
warnings.filterwarnings('ignore')
os.system('cls')
from google.auth import default
credentials, project_id = default()
print(credentials)
print(project_id)

#vertexai.init(project=project_id,location="asia-south1",credentials=credentials)
#https://cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions
#model = GenerativeModel("gemini-2.5-flash")

# Classify urgency
prompt = """
Classify this request into High, Medium, or Low urgency.
Request: "Our production server is down and customers are impacted."
Answer with only one word: High, Medium, or Low.
"""

#response = model.generate_content(prompt)
#print("Urgency:", response.text.strip())
text = "Our production server is down and customers are impacted."
client = language_v1.LanguageServiceClient.from_service_account_file("predict-text-project-a6f736e0ddff.json")
#client = language_v1.LanguageServiceClient(credentials=credentials)

document = language_v1.Document(
    content=text,
    type_=language_v1.Document.Type.PLAIN_TEXT,
)

# Analyze sentiment
response = client.analyze_sentiment(request={"document": document})
print(response)



