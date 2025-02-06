import os
from dotenv import load_dotenv
from agency_swarm import Agency, set_openai_key
from ReportGeneratorAgent import ReportGeneratorAgent
from CodeAnalyzerAgent import CodeAnalyzerAgent
from CEOAgent import CEOAgent

# Load environment variables from .env file
load_dotenv()

set_openai_key(os.getenv('OPEN_AI_KEY'))

ceo = CEOAgent()
code_analyzer = CodeAnalyzerAgent()
report_generator = ReportGeneratorAgent()

agency = Agency([ceo, [ceo, code_analyzer],
                 [code_analyzer, report_generator]],
                shared_instructions='./agency_manifesto.md',  # shared instructions for all agents
                max_prompt_tokens=25000,  # default tokens in conversation for all agents
                temperature=0.3,  # default temperature for all agents
                )

if __name__ == '__main__':
    agency.demo_gradio()
