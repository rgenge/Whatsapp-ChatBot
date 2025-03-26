from fastapi import APIRouter, Body, HTTPException, Request, Response
from pydantic import BaseModel
import openai
import json
import requests
from app.core.config import settings

router = APIRouter(prefix="/utils", tags=["utils"])


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


# Chat Gpt Endpoint
@router.post("/chat/", response_model=ChatResponse)
async def chat(request: ChatRequest = Body(...)) -> ChatResponse:
    try:
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Answer the question in no more than 40 words and do not prompt for further assistance. Provide a single, unique answer.",
                },
                {"role": "user", "content": request.message},
            ],
        )
        assistant_response = completion.choices[0].message.content
        return ChatResponse(response=assistant_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")


# WhatsApp webhook verification endpoint
@router.get("/whatsapp")
async def verify_webhook(request: Request):
    """Verify webhook for WhatsApp integration"""
    # Get query parameters
    query_params = request.query_params
    mode = query_params.get("hub.mode")
    token = query_params.get("hub.verify_token")
    challenge = query_params.get("hub.challenge")

    # Verify token (matches what set in Meta Developer)
    if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
        return Response(content=challenge)
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/whatsapp")
async def receive_message(request: Request):
    try:
        # Log the raw request body
        body_bytes = await request.body()
        body_text = body_bytes.decode("utf-8")
        print(f"Raw webhook body: {body_text}")
        body = json.loads(body_text)

        if body.get("object") == "whatsapp_business_account":
            for entry in body.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    if "messages" in value:
                        for message in value["messages"]:
                            if message.get("type") == "text":
                                from_number = message.get("from")
                                message_text = message.get("text", {}).get("body", "")
                                # Use your OpenAI function to get a response
                                openai_request = ChatRequest(message=message_text)
                                openai_response = await chat(openai_request)
                                # Send response back to WhatsApp
                                result = await send_whatsapp_response(
                                    from_number, openai_response.response
                                )
                                print(f"WhatsApp API response: {result}")
        return {"status": "success"}

    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return {"status": "error", "message": str(e)}


async def send_whatsapp_response(to_number: str, message_text: str):
    url = (
        f"https://graph.facebook.com/v22.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    )
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_number,
        "type": "text",
        "text": {"preview_url": False, "body": message_text},
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()
