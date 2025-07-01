import os
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from twilio.rest import Client

BOT_TOKEN = os.getenv("BOT_TOKEN")
SERVER_ID = int(os.getenv("SERVER_ID"))
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
NGROK_URL = os.getenv("NGROK_URL")

bot = commands.Bot(command_prefix="!")
slash = SlashCommand(bot, sync_commands=True)
twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)

@slash.slash(
    name="dial",
    description="Trimite un OTP prin apel",
    guild_ids=[SERVER_ID],
    options=[
        {"name": "cell_phone", "description": "Numărul țintă (+cod)", "type": 3, "required": True},
        {"name": "otp_digits", "description": "Câte cifre să aibă OTP-ul", "type": 4, "required": True},
        {"name": "client_name", "description": "Numele clientului", "type": 3, "required": True},
        {"name": "company_name", "description": "Numele companiei", "type": 3, "required": True}
    ]
)
async def _dial(ctx: SlashContext, cell_phone: str, otp_digits: int, client_name: str, company_name: str):
    await ctx.send(f"\U0001F4DE Trimit apel către `{cell_phone}` cu OTP de {otp_digits} cifre...")
    otp = "".join(str(__import__("random").randint(0, 9)) for _ in range(otp_digits))
    call = twilio_client.calls.create(
        to=cell_phone,
        from_=TWILIO_NUMBER,
        url=f"{NGROK_URL}/twiml?otp={otp}&client={client_name}&company={company_name}"
    )
    await ctx.send(f"✅ Apel inițiat, SID: `{call.sid}`")

bot.run(BOT_TOKEN)
