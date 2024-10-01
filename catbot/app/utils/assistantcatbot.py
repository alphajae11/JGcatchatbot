import time
import json
from openai import OpenAI
from ..config import Config


client = OpenAI(
    api_key=Config.OPENAI_API_KEY
)

cat_bot_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_cat_image",
            "description": "Return the cat image based on breed and count.",
            "parameters": {
                "type": "object",
                "properties": {
                        "breed": {"type": "string"},
                        "count": {"type": "integer", "minimum": 1, "maximum": 10}
                    },
                "required": [],
            },
        }
    }
]


def start_cat_bot():
    assistant = client.beta.assistants.create(
        name="Cat Expert",
        instructions="You are a personal cat expert. Answer any questions about cats.",
        tools=cat_bot_tools,
        model="gpt-4o-mini",
    )
    return assistant.id


def start_bot_thread():
    thread = client.beta.threads.create()
    return thread.id


def chat_with_cat_bot(message, get_image):
    try:
        ASSISTANT_ID = start_cat_bot()
        THREAD_ID = start_bot_thread()

        client.beta.threads.messages.create(
            thread_id=THREAD_ID,
            role="user",
            content=message
        )

        run = client.beta.threads.runs.create(
            thread_id=THREAD_ID,
            assistant_id=ASSISTANT_ID
        )

        while run.status not in ["completed", "failed"]:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(thread_id=THREAD_ID, run_id=run.id)
            print(f"Status: {run.status}")

            if run.status == "requires_action":
                for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                    if tool_call.function.name == "get_cat_image":
                        arguments = json.loads(tool_call.function.arguments)
                        breed = arguments.get("breed")
                        count = arguments.get("count", 1)
                        cat_images = get_image(breed, count)

                        client.beta.threads.runs.submit_tool_outputs(
                            thread_id=THREAD_ID,
                            run_id=run.id,
                            tool_outputs=[{
                                "tool_call_id": tool_call.id,
                                "output": json.dumps(cat_images)
                            }]
                        )

                        yield f"Fetched cat images: {', '.join(cat_images)}"

            yield f"Status: {run.status}"

        messages = client.beta.threads.messages.list(thread_id=THREAD_ID)
        for message in messages.data:
            if message.role == "assistant":
                for content in message.content:
                    if content.type == "text":
                        yield content.text.value

    except Exception as e:
        yield f"An error occurred: {str(e)}"
