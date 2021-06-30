import asyncio
import sys
import aiohttp
from prettytable import PrettyTable
import pandas as pd
from fpl import FPL


async def main():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        players = await fpl.get_players(return_json=True)
        # player = await fpl.get_player(300, return_json=True)

    # print(player)
    # print(player.web_name)
    # df = pd.DataFrame(data=players)
    df = pd.DataFrame(data=players)
    print(df.columns)
    # print(players[0].web_name)
    df.sort_values(by=["total_points"], inplace=True, ascending=False)

    print(df.loc[:, ["web_name", "total_points", "now_cost", "element_type"]].head(20))
    # print(df.element_type.describe())

    # for i in range(1):
    # player = players[i]
    # print(player.games_played)
    # dir(players)
    # print(player["now_cost"])
    # print(players[i])


if __name__ == "__main__":
    asyncio.run(main())
