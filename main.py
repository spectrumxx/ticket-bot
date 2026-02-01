import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

SUPPORT_ID = 1461753229514641676  # SEU ID
TICKET_CATEGORY_NAME = "Tickets"

@bot.event
async def on_ready():
    print(f"🎫 Ticket Bot online como {bot.user}")

# ================= VIEW DO BOTÃO =================
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 Create a Ticket", style=discord.ButtonStyle.green)
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        category = discord.utils.get(guild.categories, name=TICKET_CATEGORY_NAME)
        if category is None:
            category = await guild.create_category(TICKET_CATEGORY_NAME)

        channel_name = f"ticket-{user.name}".lower()

        for channel in category.channels:
            if channel.name == channel_name:
                await interaction.response.send_message(
                    "❌ You already have an open ticket.",
                    ephemeral=True
                )
                return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.get_member(SUPPORT_ID): discord.PermissionOverwrite(
                view_channel=True, send_messages=True
            ),
        }

        channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites
        )

        await interaction.response.send_message(
            f"✅ Your ticket has been created: {channel.mention}",
            ephemeral=True
        )

        embed = discord.Embed(
            title="🎟️ Support Ticket",
            description=(
                "Welcome to your ticket!\n\n"
                "**Use this channel to:**\n"
                "• Report bugs\n"
                "• Send suggestions\n"
                "• Ask for support\n\n"
                "**Rules:**\n"
                "• Be respectful\n"
                "• One issue per ticket\n"
                "• No spam\n\n"
                "Our team will assist you soon."
            ),
            color=0x2ECC71
        )

        await channel.send(f"{user.mention} <@{SUPPORT_ID}>", embed=embed)

# ================= COMANDO !ticket =================
@bot.command()
@commands.has_permissions(administrator=True)
async def ticket(ctx):
    embed = discord.Embed(
        title="🎫 Create a Ticket",
        description=(
            "Need help or want to report something?\n\n"
            "Click the button below to:\n"
            "• Report bugs\n"
            "• Send suggestions\n"
            "• Get support"
        ),
        color=0x3498DB
    )
    embed.set_footer(text="Ticket System")

    await ctx.send(embed=embed, view=TicketView())

# ================= INICIAR BOT =================
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN não foi definido!")

bot.run(TOKEN)
