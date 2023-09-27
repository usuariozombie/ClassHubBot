import discord
import discord.ext
import requests
from discord import app_commands
from discord.ext import commands

# Bot Configuration

TOKEN = "YOUR_TOKEN"  # Replace with your bot's token
API_BASE_URL = "http://localhost:8080/api"  # Replace with your Spring Boot server URL

# Create the client

bot = discord.Client(intents=discord.Intents.all())
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="/help for more information"))
    print("Bot started")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {synced} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="add", description="Add a schedule")
@app_commands.describe(days="Day of the week", hours="Time of day", subject="Subject")
@app_commands.choices(
    days=[
        discord.app_commands.Choice(name="Monday", value="Monday"),
        discord.app_commands.Choice(name="Tuesday", value="Tuesday"),
        discord.app_commands.Choice(name="Wednesday", value="Wednesday"),
        discord.app_commands.Choice(name="Thursday", value="Thursday"),
        discord.app_commands.Choice(name="Friday", value="Friday"),
        discord.app_commands.Choice(name="Saturday", value="Saturday"),
        discord.app_commands.Choice(name="Sunday", value="Sunday"),
    ])
@app_commands.choices(hours=[discord.app_commands.Choice(name=f"{str(i).zfill(2)}:00", value=f"{str(i).zfill(2)}:00") for i in range(24)])
async def add_schedule(interaction: discord.Interaction, days: discord.app_commands.Choice[str], hours: discord.app_commands.Choice[str], subject: str):
    # Make a POST request to the API to add the schedule
    payload = {
        "serverId": str(interaction.guild.id),
        "day": days.name,
        "hour": hours.name,
        "subject": subject
    }
    response = requests.post(f"{API_BASE_URL}/add", params=payload)

    if response.status_code == 200:
        await interaction.response.send_message(
            f"Schedule added: Day: {days.name}, Time: {hours.name}, Subject: {subject}"
        )
    else:
        await interaction.response.send_message(f"Error adding schedule: {response.text}")

@bot.tree.command(name="show", description="Show schedules")
async def show_schedule(interaction: discord.Interaction):
    # Get schedules (replace this with your code to retrieve schedules)
    response = requests.get(
        f"{API_BASE_URL}/schedule", params={"serverId": str(interaction.guild.id)}
    )

    if response.status_code == 200:
        # Parse the response to get schedules
        schedule_text = response.text

        # Create a custom embed
        embed = discord.Embed(
            title="Class Schedules",
            description="Below are the class schedules for this server.",
            color=discord.Color.blue(),
        )

        # Split the response into lines and process it
        lines = schedule_text.strip().split("\n")
        current_day = ""
        for line in lines:
            if ":" in line:
                current_day, schedule_info = line.split(":", 1)
                embed.add_field(
                    name=current_day,
                    value=schedule_info,
                    inline=False,
                )
            else:
                # Ignore the line if it doesn't have the correct format
                continue

        # Add an image (optional)
        embed.set_thumbnail(url=interaction.guild.icon)

        # Add a footer (optional)
        embed.set_footer(
            text="More information on our website", icon_url=interaction.guild.icon
        )

        # Send the embed as a response to the interaction
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(
            f"Error getting schedules: {response.text}"
        )

@bot.tree.command(name="edit", description="Edit a schedule")
@app_commands.describe(days="Day of the week", hours="Time of day", subject="Subject")
@app_commands.choices(
    days=[
        discord.app_commands.Choice(name="Monday", value="Monday"),
        discord.app_commands.Choice(name="Tuesday", value="Tuesday"),
        discord.app_commands.Choice(name="Wednesday", value="Wednesday"),
        discord.app_commands.Choice(name="Thursday", value="Thursday"),
        discord.app_commands.Choice(name="Friday", value="Friday"),
        discord.app_commands.Choice(name="Saturday", value="Saturday"),
        discord.app_commands.Choice(name="Sunday", value="Sunday"),
    ])
@app_commands.choices(hours=[discord.app_commands.Choice(name=f"{str(i).zfill(2)}:00", value=f"{str(i).zfill(2)}:00") for i in range(24)])
async def edit_schedule(interaction: discord.Interaction, days: discord.app_commands.Choice[str], hours: discord.app_commands.Choice[str], subject: str):
    # Make a PUT request to the API to edit the schedule
    payload = {
        "serverId": str(interaction.guild.id),
        "day": days.name,
        "hour": hours.name,
        "subject": subject
    }
    response = requests.put(f"{API_BASE_URL}/edit", params=payload)

    if response.status_code == 200:
        await interaction.response.send_message(
            f"Schedule edited: Day: {days.name}, Time: {hours.name}, Subject: {subject}"
        )
    else:
        await interaction.response.send_message(f"Error editing schedule: {response.text}")

@bot.tree.command(name="delete", description="Delete a schedule")
@app_commands.describe(days="Day of the week", hours="Time of day")
@app_commands.choices(
    days=[
        discord.app_commands.Choice(name="Monday", value="Monday"),
        discord.app_commands.Choice(name="Tuesday", value="Tuesday"),
        discord.app_commands.Choice(name="Wednesday", value="Wednesday"),
        discord.app_commands.Choice(name="Thursday", value="Thursday"),
        discord.app_commands.Choice(name="Friday", value="Friday"),
        discord.app_commands.Choice(name="Saturday", value="Saturday"),
        discord.app_commands.Choice(name="Sunday", value="Sunday"),
    ])
@app_commands.choices(hours=[discord.app_commands.Choice(name=f"{str(i).zfill(2)}:00", value=f"{str(i).zfill(2)}:00") for i in range(24)])
async def delete_schedule(interaction: discord.Interaction, days: discord.app_commands.Choice[str], hours: discord.app_commands.Choice[str]):
    # Make a DELETE request to the API to delete the schedule
    payload = {
        "serverId": str(interaction.guild.id),
        "day": days.name,
        "hour": hours.name
    }
    response = requests.delete(f"{API_BASE_URL}/delete", params=payload)

    if response.status_code == 200:
        await interaction.response.send_message(
            f"Schedule deleted: Day: {days.name}, Time: {hours.name}"
        )
    else:
        await interaction.response.send_message(f"Error deleting schedule: {response.text}")

@bot.tree.command(name="help", description="Show help")
async def help(interaction: discord.Interaction):
    # Create a custom embed
    embed = discord.Embed(
        title="Class Schedules",
        description="Below are the commands for this bot.",
        color=discord.Color.blue(),
    )

    # Add fields
    embed.add_field(
        name="/add",
        value="Add a schedule",
        inline=False,
    )
    embed.add_field(
        name="/show",
        value="Show schedules",
        inline=False,
    )
    embed.add_field(
        name="/edit",
        value="Edit a schedule",
        inline=False,
    )
    embed.add_field(
        name="/delete",
        value="Delete a schedule",
        inline=False,
    )

    # Add an image (optional)
    embed.set_thumbnail(url=interaction.guild.icon)

    # Add a footer (optional)
    embed.set_footer(
        text="More information on our website", icon_url=interaction.guild.icon
    )

    # Send the embed as a response to the interaction
    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)