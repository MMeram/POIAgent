from smolagents import CodeAgent,DuckDuckGoSearchTool, HfApiModel,load_tool,tool, LiteLLMModel
import datetime
import requests
import pytz
import yaml
import os
from tools.final_answer import FinalAnswerTool
# import mapbox methods
from tools.mapbox_tools import geocode_location, search_nearby_places

from Gradio_UI import GradioUI


final_answer = FinalAnswerTool()

# Create a DuckDuckGo search tool
search_tool = DuckDuckGoSearchTool()

# If the agent does not answer, the model is overloaded, please use another model or the following Hugging Face Endpoint that also contains qwen2.5 coder:
# model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud' 

#model = HfApiModel(
#max_tokens=2096,
#temperature=0.5,
#model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud',
#model_id='Qwen/Qwen2.5-Coder-32B-Instruct',# it is possible that this model may be overloaded
#custom_role_conversions=None,
#)
model = LiteLLMModel(model_id="gemini/gemini-2.0-flash-lite", api_key=os.getenv(key="GEMINI_API_KEY"))

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)
    
agent = CodeAgent(
    model=model,
    tools=[
        geocode_location,
        search_nearby_places,
        final_answer], ## add your tools here (don't remove final answer)
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)


GradioUI(agent).launch()