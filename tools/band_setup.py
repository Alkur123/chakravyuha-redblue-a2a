"""One-time: Blue creates the BAND room and adds Red and the owner (principal)."""
import os
from dotenv import load_dotenv
from band_rest import RestClient, ChatRoomRequest, ParticipantRequest

load_dotenv(".env")
blue = RestClient(api_key=os.environ["BAND_KEY_BLUE"])
red = RestClient(api_key=os.environ["BAND_KEY_RED"])
mb = blue.agent_api_identity.get_agent_me().data
mr = red.agent_api_identity.get_agent_me().data
print("blue", mb.handle, "red", mr.handle, "same owner:", mb.owner_uuid == mr.owner_uuid)
chat = blue.agent_api_chats.create_agent_chat(chat=ChatRoomRequest(title="Chakravyuha war room: Red vs Blue")).data
print("chat", chat.id)
for pid in (mr.id, mb.owner_uuid):
    try:
        blue.agent_api_participants.add_agent_chat_participant(chat.id, participant=ParticipantRequest(participant_id=pid))
        print("added", pid[:8])
    except Exception as e:
        print("add failed", pid[:8], str(e)[:300])
with open(".env", "a") as f:
    f.write(f"BAND_CHAT_ID={chat.id}\nBAND_PRINCIPAL_ID={mb.owner_uuid}\n")
for p in blue.agent_api_participants.list_agent_chat_participants(chat.id).data:
    print("participant", getattr(p, "name", None), getattr(p, "type", None))
