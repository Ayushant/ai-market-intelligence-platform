"""
AWS AgentCore Handler - Entry point for AgentCore deployment
This handler receives requests from AgentCore and invokes the CrewAI agent
"""

import json
import os
from datetime import datetime
from typing import Dict, Any
from langfuse import get_client
from openinference.instrumentation.crewai import CrewAIInstrumentor
from researcheragen1.crews.researchCrew import Emergingtechnologyresearch
from researcheragen1.utils.env import populateEnvWithSecrets

# Initialize logging
import logging
logger = logging.getLogger(__name__)

# Step1: Populate environment variables from AWS Secrets Manager
populateEnvWithSecrets()

# Step2: Setup Langfuse for observability/tracing
try:
    langfuse = get_client()
    if langfuse.auth_check():
        logger.info("Langfuse client authenticated successfully")
        CrewAIInstrumentor().instrument(skip_dep_check=True)
    else:
        logger.warning("Langfuse authentication failed")
        langfuse = None
except Exception as e:
    logger.warning(f"Langfuse setup failed: {e}")
    langfuse = None


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main handler function invoked by AWS AgentCore
    
    Args:
        event: Contains the research topic and other parameters
        context: AWS Lambda context object
        
    Returns:
        Dictionary with status and research report
    """
    try:
        # Step1: Extract input from AgentCore request
        topic = event.get("topic") or event.get("body", {}).get("topic")
        
        if not topic:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "Missing 'topic' parameter",
                    "message": "Please provide a topic to research"
                })
            }
        
        logger.info(f"Processing research request for topic: {topic}")
        
        # Step2: Prepare inputs for the crew
        inputs = {
            "topic": topic,
            "current_year": str(datetime.now().year)
        }
        
        # Step3: Execute the CrewAI crew with tracing
        response = ""
        span_name = f"emerging-technology-research-{topic[:30]}"
        
        if langfuse:
            with langfuse.start_as_current_span(name=span_name):
                response = Emergingtechnologyresearch().crew().kickoff(inputs=inputs)
                langfuse.update_current_trace(input=inputs, output=str(response))
            langfuse.flush()
        else:
            response = Emergingtechnologyresearch().crew().kickoff(inputs=inputs)
        
        # Step4: Format response for AgentCore
        result = {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "topic": topic,
                "report": response.json_dict if hasattr(response, 'json_dict') else str(response),
                "timestamp": datetime.now().isoformat()
            })
        }
        
        logger.info("Research completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "success": False,
                "error": str(e),
                "message": "An error occurred while processing the research request"
            })
        }


# For local testing without AgentCore
if __name__ == "__main__":
    test_event = {
        "topic": "Artificial Intelligence in 2025"
    }
    result = handler(test_event, None)
    print(json.dumps(json.loads(result["body"]), indent=2))
