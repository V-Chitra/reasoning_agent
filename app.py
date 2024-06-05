PROJECT_ID = "chitra-agent-project"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}
STAGING_BUCKET = "gs://grcv-bucket"  # @param {type:"string"}

import vertexai
vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)
import requests
from vertexai.preview import reasoning_engines

model = "gemini-1.5-pro-preview-0409"

def get_exchange_rate(
    currency_from: str = "USD",
    currency_to: str = "EUR",
    currency_date: str = "latest",
):
    """Retrieves the exchange rate between two currencies on a specified date."""
    import requests

    response = requests.get(
        f"https://api.frankfurter.app/{currency_date}",
        params={"from": currency_from, "to": currency_to},
    )
    return response.json()

get_exchange_rate(currency_from="USD", currency_to="SEK")
agent = reasoning_engines.LangchainAgent(
    model=model,
    tools=[get_exchange_rate],
    agent_executor_kwargs={"return_intermediate_steps": True},
)

agent = reasoning_engines.LangchainAgent(
    model=model,
    tools=[get_exchange_rate],
)

remote_agent = reasoning_engines.ReasoningEngine.create(
    agent,
    requirements=[
        "google-cloud-aiplatform==1.51.0",
        "langchain==0.1.20",
        "langchain-google-vertexai==1.0.3",
        "cloudpickle==3.0.0",
        "pydantic==2.7.1",
        "requests",
    ],
)

app = Flask(__name__)

if __name__ == "__main__":
    app.run(port=8080, host='0.0.0.0', debug=True)