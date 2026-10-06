from discord import Interaction

message = """

# Who is running this?
The management team of this production is in no particular order:
    Katze, Lime, R1shy, Vecotr, RKMaria, Rex, Cloversghost, Nat, Ume

"""


async def faq(interaction: Interaction):
    await interaction.response.send_message(message)
