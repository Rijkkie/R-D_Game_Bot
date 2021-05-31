import discord


def balance(user, money):
    embed = discord.Embed(title=" ", description="")
    embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url=user.avatar_url)
    embed.add_field(name="Rank", value=f"\#{money[1]}", inline=True)
    embed.add_field(name="Balance :moneybag:", value=money[0], inline=True)  # [0][0]
    return embed


def stats(user, user_stats, ranks, total_stats):
    width = 12
    t1 = """
```css
Game         w/l/d     Score    Rank
"""
    t2 = ""
    t3 = f"""
{"Total:":{width}} {str(total_stats[0][1])+'/'+str(total_stats[0][2])+'/'+str(total_stats[0][3]):{width-6}} {total_stats[0][4]:{width-4}}     #{total_stats[0][5]}

Boardgames played: {total_stats[0][1] + total_stats[0][2] + total_stats[0][3]}
```"""
    for i in range(len(user_stats)):
        t2 += f"{user_stats[i][0]:{width}} {str(user_stats[i][2])+'/'+str(user_stats[i][3])+'/'+str(user_stats[i][4]):{width-6}} {user_stats[i][5]:{width-4}}     #{ranks[i]}\n"
    embed = discord.Embed(title=" ", description="```      Personal Boardgame Stats```" + t1 + t2 + t3)
    embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url=user.avatar_url)
    return embed


def top_balance(top, page):
    width = 4
    t1 = f"""
```css
{"Rank":{width}} {"Balance":{width+5}} Name
"""
    t2 = ""
    t3 = "```"
    for i in range(len(top)):
        t2 += f" {'#'+str(top[i][5]):{width}} {top[i][1]:{width+2}}   {top[i][0]}\n"
    embed = discord.Embed(title=" ", description="```Global balance leaderboard```" + t1 + t2 + t3)
    embed.set_footer(text=f"page {page}/{round(top[0][2] / 10 + .5)}")
    return embed


def top_boardgame(top, page):
    width = 3
    t1 = f"""
```css
{"Rank":{width+5}} {"score":{width+3}} {"w/l/d":{width+4}} User
"""
    t2 = ""
    t3 = "```"
    for i in range(len(top)):
        t2 += f" {'#'+str(top[i][8]):{width}} {top[i][6]:{width+6}}  {str(top[i][3])+'/'+str(top[i][4])+'/'+str(top[i][5]):{width+4}} {top[i][1]}\n"
    embed = discord.Embed(title=" ", description="```Global stats leaderboard```" + t1 + t2 + t3)
    embed.set_footer(text=f"page {page}/{round(top[0][7] / 10 + .5)}")
    return embed
