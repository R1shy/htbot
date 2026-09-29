from discord import Interaction

message = """

# Can roles be gender bent?
yes, we are totally fine with gender bending

# When do Auditions close?
<t:1791172740:f>

# Who is running this?
The management team of this production is in no particular order:
    Katze, Lime, R1shy, Vecotr, RKMaria, Rex, Cloversghost, Nat, Ume

# Can I be crew?
No, unfortunately the crew for this production has already been chosen

# How do I audition?

in https://discord.com/channels/1531513098551431228/1532163389722202294 read https://discord.com/channels/1531513098551431228/1534795482008780901 and https://discord.com/channels/1531513098551431228/1531517330817945760

"""

async def faq(interaction: Interaction):
    await interaction.response.send_message(message)
