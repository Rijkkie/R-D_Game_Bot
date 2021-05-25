import discord


def balance(user, money, rank):
    embed = discord.Embed(title=" ", description="")
    embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url=user.avatar_url)
    embed.add_field(name="Rank", value=f"\#{rank}", inline=True)
    embed.add_field(name="Balance :moneybag:", value=money, inline=True)
    return embed


def stats(user, user_stats, ranks, total_stats, total_rank):  # MAKE TOTAL wins/score/rank. Leaderboard.
    width = 12
    t1 = """
```glsl
   game      w/l/d      score      rank
   
"""
    t2 = ""
    t3 = f"""
Total:       {total_stats[0][1]}/{total_stats[0][2]}/{total_stats[0][3]} {total_stats[0][4]:{width-3}}        #{total_rank}

Boardgames played: {total_stats[0][1] + total_stats[0][2] + total_stats[0][3]}
```"""
    for i in range(len(user_stats)):
        t2 += f"{user_stats[i][0]:{width}} {user_stats[i][2]}/{user_stats[i][3]}/{user_stats[i][4]} {user_stats[i][5]:{width-3}}        #{ranks[i]}\n"
    embed = discord.Embed(title=" ", description="```       Personal Boardgame Stats```" + t1 + t2 + t3)
    embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url=user.avatar_url)
    return embed
