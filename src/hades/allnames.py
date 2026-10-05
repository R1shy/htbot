from discord import Interaction, ForumChannel
import os

async def an(interaction: Interaction):
    audchannelid = os.getenv("AUDCHANNELID") or "-1"
    guild = interaction.guild
    if guild is None:
        return await interaction.response.send_message("Not in a server")
        
    channel = await guild.fetch_channel(int(audchannelid))
    if isinstance(channel, ForumChannel):
        # 1. Get active threads
        active_threads = channel.threads
        
        archived_threads = []
        async for t in channel.archived_threads(limit=None):
            archived_threads.append(t) # pyright: ignore[reportUnknownMemberType]

        tt = active_threads + archived_threads
        
        print(len(tt) == len(active_threads) + len(archived_threads)) # pyright: ignore[reportUnknownArgumentType]

        res = ""
        i = 0
        for thread in tt:
            try:
                print(thread.name)
                res += thread.name + "\n"
            except Exception:
                print(f"skip number {i}")
                i += 1
                continue
                
        with open("meow", "w") as f:
            f.write(res)
            
        await interaction.response.send_message("done")

