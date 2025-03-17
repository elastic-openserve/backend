from fastapi import FastAPI, Request, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
import asyncio
import os
import shutil
from dotenv import load_dotenv
from app.openserve_service.do_task import do_task
from app.openserve_service.respond_chat_message import respond_chat_message
from app.openserve_service.api import APIClient

from app.service.common_utils import load_json_data, save_json_data

from app.agent_service.trend_analyzer import TREND_ANALYZER
from app.agent_service.site_log_agent import SITE_LOG_AGENT
from app.agent_service.site_log_refiner_agent import SITE_LOG_REFINER_AGENT
from app.agent_service.script_writer_agent import SCRIPT_WRITER_AGENT
from app.agent_service.image_generator_agent import IMAGE_GENERATOR_AGENT
from app.agent_service.audio_agent import AUDIO_AGENT
from app.agent_service.video_agent import VIDEO_AGENT
from app.agent_service.email_agent import EMAIL_AGENT


# Load environment variables
load_dotenv()
# os.environ["TREND_ANALYZER_OPENSERV_API_KEY"] = ""
# os.environ["SITE_LOG_AGENT_OPENSERV_API_KEY"] = ""
# os.environ["SITE_LOG_REFINER_OPENSERV_API_KEY"] = ""
# os.environ["SCRIPT_WRITER_OPENSERV_API_KEY"] = ""
# os.environ["IMAGE_GENERATOR_OPENSERV_API_KEY"] = ""
# os.environ["AUDIO_AGENT_OPENSERV_API_KEY"] = ""
# os.environ["VIDEO_AGENT_OPENSERV_API_KEY"] = ""
# os.environ["EMAIL_AGENT_OPENSERV_API_KEY"] = ""

app = FastAPI()

# API Clients (Dependency Injection ready)
def get_api_clients():
    return {
        "trend_analyzer": {
            "client": APIClient(os.getenv("TREND_ANALYZER_OPENSERV_API_KEY")),
            "function": TREND_ANALYZER.run
        },
        "site_log_agent": {
            "client": APIClient(os.getenv("SITE_LOG_AGENT_OPENSERV_API_KEY")),
            "function": SITE_LOG_AGENT.run
        },
        "site_log_refiner_agent": {
            "client": APIClient(os.getenv("SITE_LOG_REFINER_OPENSERV_API_KEY")),
            "function": SITE_LOG_REFINER_AGENT.run
        },
        "script_writer_agent": {
            "client": APIClient(os.getenv("SCRIPT_WRITER_OPENSERV_API_KEY")),
            "function": SCRIPT_WRITER_AGENT.run
        },
        "image_generator_agent": {
            "client": APIClient(os.getenv("IMAGE_GENERATOR_OPENSERV_API_KEY")),
            "function": IMAGE_GENERATOR_AGENT.run
        },
        "audio_agent": {
            "client": APIClient(os.getenv("AUDIO_AGENT_OPENSERV_API_KEY")),
            "function": AUDIO_AGENT.run
        },
        "video_agent": {
            "client": APIClient(os.getenv("VIDEO_AGENT_OPENSERV_API_KEY")),
            "function": VIDEO_AGENT.run
        },
        "email_agent": {
            "client": APIClient(os.getenv("EMAIL_AGENT_OPENSERV_API_KEY")),
            "function": EMAIL_AGENT.run
        }
    }

# Background task cleanup
active_tasks = set()

def cleanup_task(task):
    active_tasks.discard(task)


async def process_action(
    typ: str,
    action,
    background_tasks: BackgroundTasks,
    api_client: dict,
    output_key: str
):
    try:
        if typ not in api_client:
            raise HTTPException(status_code=400, detail="Invalid API client")

        print("\nReceived new request")
        print("Request data:", action)
        print(f"Action type: {action.get('type')}")

        # Handle action types
        if action["type"] == "do-task":
            print("Processing do-task action")
            task = asyncio.create_task(
                do_task(
                    action,
                    task_function=api_client[typ]["function"],
                    api_client=api_client[typ]["client"],
                    output_key=output_key
                )
            )
            active_tasks.add(task)
            task.add_done_callback(cleanup_task)

        elif action["type"] == "respond-chat-message":
            print("Processing respond-chat-message action")
            task = asyncio.create_task(
                respond_chat_message(
                    action,
                    api_client=api_client[typ]["client"]
                )
            )
            active_tasks.add(task)
            task.add_done_callback(cleanup_task)

        else:
            raise HTTPException(status_code=400, detail="Unknown action type")

        background_tasks.add_task(dummy_cleanup)
        return JSONResponse({"message": "OK"})

    except Exception as e:
        print(f"Error in process_action: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# FastAPI Route Handlers
@app.post("/trend-analyzer")
async def handle_action_trend_analyzer(
    request: Request,
    background_tasks: BackgroundTasks,
    api_client: dict = Depends(get_api_clients)
):
    action = await request.json()
    action['task']['input'] = action['task']['input']
    save_json_data(f"assets/{action['workspace']['id']}/user_input.json", {"product_description": action['task']['input']})

    output_key = "trend_result"

    return await process_action("trend_analyzer", action, background_tasks, api_client, output_key=output_key)



@app.post("/site-log-agent")
async def handle_action_site_log_agent(
    request: Request,
    background_tasks: BackgroundTasks,
    api_client: dict = Depends(get_api_clients)
):
    action = await request.json()

    workspace_id = action['workspace']['id']
    input_fname = f"assets/{workspace_id}/trend_result.json"
    input_data = load_json_data(input_fname)
    action['task']['input'] = input_data['product_id']

    output_key = "site_log_result"

    return await process_action("site_log_agent", action, background_tasks, api_client, output_key=output_key)



@app.post("/site-log-refiner-agent")
async def handle_action_site_log_refiner_agent(
    request: Request,
    background_tasks: BackgroundTasks,
    api_client: dict = Depends(get_api_clients)
):
    
    action = await request.json()
    workspace_id = action['workspace']['id']
    input_fname = f"assets/{workspace_id}/site_log_result.json"
    input_data = load_json_data(input_fname)
    action['task']['input'] = input_data

    output_key = "site_log_refiner_result"

    return await process_action("site_log_refiner_agent", action, background_tasks, api_client, output_key=output_key)


@app.post("/script-writer-agent")
async def handle_action_script_writer_agent(
    request: Request,
    background_tasks: BackgroundTasks,
    api_client: dict = Depends(get_api_clients)
):
    action = await request.json()
    workspace_id = action['workspace']['id']
    input_fname_0 = f"assets/{workspace_id}/user_input.json"
    input_fname_1 = f"assets/{workspace_id}/trend_result.json"
    input_fname_2 = f"assets/{workspace_id}/site_log_refiner_result.json"

    input_data_0 = load_json_data(input_fname_0)
    input_data_1 = load_json_data(input_fname_1)
    input_data_2 = load_json_data(input_fname_2)

    action['task']['input'] = {
        "product_description": input_data_0,
        "trend_result": input_data_1,
        "site_log_refiner_result": input_data_2
    }

    output_key = "script_result"


    return await process_action("script_writer_agent", action, background_tasks, api_client, output_key=output_key)

@app.post("/image-generator-agent")
async def handle_action_image_generator_agent(
    request: Request,
    background_tasks: BackgroundTasks,
    api_client: dict = Depends(get_api_clients)
):
    
    action = await request.json()
    workspace_id = action['workspace']['id']
    input_fname = f"assets/{workspace_id}/script_result.json"
    input_data = load_json_data(input_fname)
    action['task']['input'] = input_data

    output_key = "image_script_result"

    return await process_action("image_generator_agent", action, background_tasks, api_client, output_key=output_key)

@app.post("/audio-agent")
async def handle_action_audio_agent(
    request: Request,
    background_tasks: BackgroundTasks,
    api_client: dict = Depends(get_api_clients)
):
    
    action = await request.json()
    workspace_id = action['workspace']['id']
    input_fname = f"assets/{workspace_id}/image_script_result.json"
    input_data = load_json_data(input_fname)
    action['task']['input'] = input_data

    output_key = "audio_script_result"

    return await process_action("audio_agent", action, background_tasks, api_client, output_key=output_key)


@app.post("/video-agent")
async def handle_action_video_agent(
    request: Request,
    background_tasks: BackgroundTasks,
    api_client: dict = Depends(get_api_clients)
):
    action = await request.json()
    input_data = int(action['workspace']['id'])
    action['task']['input'] = input_data

    output_key = "video_result"

    return await process_action("video_agent", action, background_tasks, api_client, output_key=output_key)

@app.post("/email-agent")
async def handle_action_email_agent(
    request: Request,
    background_tasks: BackgroundTasks,
    api_client: dict = Depends(get_api_clients)
):
    
    action = await request.json()
    workspace_id = action['workspace']['id']
    input_fname = f"assets/{workspace_id}/audio_script_result.json"
    input_data = load_json_data(input_fname)
    action['task']['input'] = input_data

    output_key = "email_result"

    return await process_action("email_agent", action, background_tasks, api_client, output_key=output_key)





@app.get("/remove-assets")
async def remove_assets(request: Request):
    shutil.rmtree("assets")
    os.makedirs("assets", exist_ok=True)
    return JSONResponse({"message": "Assets removed successfully"}), 200


async def dummy_cleanup():
    pass


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down gracefully...")
    if active_tasks:
        await asyncio.gather(*active_tasks, return_exceptions=True)
    for key, client in get_api_clients().items():
        await client["client"].close()
    print("Shutdown complete ✅")





# from flask import Blueprint, request, jsonify
# import asyncio}
# import os
# from dotenv import load_dotenv
# from app.openserve_service.do_task import do_task
# from app.openserve_service.respond_chat_message import respond_chat_message
# from app.openserve_service.api import APIClient
# from app.agent_service.trend_analyzer import TREND_ANALYZER

# # Load environment variables
# load_dotenv()

# openserve_bp = Blueprint('openserve', __name__)

# # Store active tasks globally
# active_tasks = set()

# # API Clients 
# api_client = {
#     "trend_analyzer": {
#         "client": APIClient(os.getenv("TREND_ANALYZER_OPENSERV_API_KEY")),
#         "function": TREND_ANALYZER.run,
#     }
# }

# def cleanup_task(task):
#     active_tasks.discard(task)

# @openserve_bp.route("/", methods=["POST"])
# def handle_action():
#     try:
#         typ = request.args.get("typ")
#         if typ not in api_client:
#             return jsonify({"error": "Invalid API client"}), 400

#         print("\nReceived new request")
#         action = request.get_json()
#         print("Request data:", action)
#         print(f"Action type: {action.get('type')}")

#         # Always create a new event loop for the thread
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)

#         # Handle different action types asynchronously
#         if action["type"] == "do-task":
#             print("Processing do-task action")
#             task = loop.create_task(
#                 do_task(
#                     action,
#                     task_function=api_client[typ]["function"],
#                     api_client=api_client[typ]["client"]
#                 )
#             )
#             active_tasks.add(task)
#             task.add_done_callback(cleanup_task)

#         elif action["type"] == "respond-chat-message":
#             print("Processing respond-chat-message action")
#             task = loop.create_task(
#                 respond_chat_message(
#                     action,
#                     api_client=api_client[typ]["client"]
#                 )
#             )
#             active_tasks.add(task)
#             task.add_done_callback(cleanup_task)

#         else:
#             print(f"Unknown action type: {action['type']}")

#         # Let the task start running
#         loop.call_soon(loop.stop)
#         loop.run_forever()
#         loop.close()

#         return jsonify({"message": "OK"}), 200

#     except Exception as e:
#         print(f"Error in handle_action: {str(e)}")
#         return jsonify({"error": str(e)}), 500



# @openserve_bp.teardown_app_request
# def shutdown_event(exception=None):
#     async def shutdown_async():
#         if active_tasks:
#             await asyncio.gather(*active_tasks, return_exceptions=True)
#         for key, client in api_client.items():
#             await client["client"].close()
#         print("Shutdown complete")

#     try:
#         asyncio.run(shutdown_async())
#     except RuntimeError as e:
#         # If event loop is already closed, log it and continue
#         print(f"Shutdown event loop error: {e}")


# """
# This is an Auto Ad Post Generator for a Brand's product.
#  - Create a Trend Analysis Report for my Product's category. - The user has to give a Product Description mentioning the Product ID, Description and Motive of its ad. The Product ID is 'P001'. Our brand is ElecX, revolutionizing electric scooters. We are passionate about creating fast, eco-friendly, and commuter-friendly scooters. The new ElecX Pro targets urban mobility solutions worldwide. The output result is called trend-result which is in a JSON format.
#  - Now generate extensive report for user traffic using different groupings based on Age, Demography, Gender, Month etc. using the the sitelog agent, good market analyst agent. The input is only a single string, PRODUCT_ID. In our case input is just P001. The output result is called sitelog-result which is in a JSON format.
#  - Now you refine the sitelog-result to get the top 2 months, top age group and top 2 regions with the highest number of user interactions. Your input is the sitelog-result, a raw JSON format. The output result is called sitelog-result which is in a JSON format.
#  - Now we have pass the trend-result and sitelog-refined-result to the script writer agent to generate a list of advertisement text scripts for the product based on the insights for each month, age group, and region. The input is the product description, trend-result, and sitelog-refined-result. The output result is called script-result which is in a JSON format.
#  - Now we have to pass the script-result to the image generator agent to generate images for the advertisement text scripts. The input is the script-result. The output result is called image-script-result which is in a JSON format.
#  - Now we have to pass the image-script-result to the audio agent to generate audio for the advertisement text scripts. The input is the image-script-result. The output result is called audio-script-result which is in a JSON format.
#  - Now we have to pass the audio-script-result to the video agent to generate video for the advertisement text scripts. The input is the audio-script-result. The output result is called video-result which is in a JSON format.
#  - Now we have to pass the audio-script-result to the email agent to send the advertisement text scripts and audio to the user. The input is the audio-script-result. The output result is called email-result which is in a JSON format.

 
#  Task of the agent:
# 1. Trend Analyzer Agent
# You are a marketing strategist helping a brand identify the most effective search terms for trend analysis. It receives a single input PRODUCT_DESCRIPTION. The output is Demography wise trend data for the product category.

# 2. Site Log Agent
# You are a good market analyst. Your job is to monitor the sitelogs based on a given PRODUCT_ID. You will generate a extensive report fior user traffic using different groupings based on Age, Demography, Gender, Month etc. It takes a single string only, PRODUCT_ID. Example input: 'P001'

# 3. Site Log Refiner Agent
# This agent is responsible for refining the sitelog-result to get the top 2 months, top age group and top 2 regions with the highest number of user interactions. The input is the sitelog-result, a raw JSON format. The output result is called sitelog-result which is in a JSON format.

# 4. Script Writer Agent
# This agent is responsible for generating advertisement text scripts for the product based on the insights for each month, age group, and region. The agent will receive the product description, trend-result, and sitelog-refined-result as input and generate a list of advertisement text scripts for the product. The output result is called script-result which is in a JSON format.
 
# 5. Image Generator Agent
# This agent is responsible for generating images for the advertisement text scripts. The agent will receive the script-result as input and generate images for the advertisement text scripts. The output result is called image-script-result which is in a JSON format.

# 6. Audio Agent

# This agent is responsible for generating audio for the advertisement text scripts. The agent will receive the image-script-result as input and generate audio for the advertisement text scripts. The output result is called audio-script-result which is in a JSON format.

# 7. Video Agent

# This agent is responsible for generating video for the advertisement text scripts. The agent will receive the audio-script-result as input and generate video for the advertisement text scripts. The output result is called video-result which is in a JSON format.

# 8. Email Agent

# This agent is responsible for sending the advertisement text scripts and audio to the user. The agent will receive the audio-script-result as input and send the advertisement text scripts and audio to the user. The acknowledgement will be in the form of email-result which is in a JSON format.
# """