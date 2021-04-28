import chess
import chess.svg
import chess.pgn
import random
import os
import csv
from datetime import date
import discord, asyncio
from discord.ext import commands

class FunCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.first_move = True

    @commands.command()
    async def chess_puzzle(self, ctx, min_rating: int, max_rating: int):
        candidates = []
        with open("cogs/chess_puzzles.csv", 'r') as file:
            reader = csv.reader(file)
            for line in reader:
                if int(line[3])-(int(line[4])//2)>min_rating and int(line[3])+(int(line[4])//2) < max_rating:
                    candidates.append(line)

        if len(candidates) == 0:
            return await ctx.send("No results found! Please try to widen your rating range.")

        puzzle = random.choice(candidates)
        board = chess.Board(fen=puzzle[1])
        counter = 1
        moves = puzzle[2].split(" ")
        board.push_uci(moves[0])

        boardsvg = chess.svg.board(board=board, orientation=chess.WHITE if board.turn else chess.BLACK, lastmove=board.move_stack[-1])
        f = open("board.svg", "w")
        f.write(boardsvg)
        f.close()
        os.system("convert -density 200 board.svg board.png")
        file = discord.File("board.png", filename="image.png")
        embed = discord.Embed(title=f"Chess Puzzle ({puzzle[3]})", color=discord.Colour.orange())
        embed.set_image(url="attachment://image.png")
        embed.set_footer(text=f"{'White' if board.turn else 'Black'} to move || Puzzle link: {puzzle[-1]}")
        await ctx.send(file=file, embed=embed)

        def check(m):
            global the_message
            if m.author == ctx.author:
                the_message = m.content
                return True

        while True:
            try:
                await self.client.wait_for('message', check=check, timeout=180)
                try:
                    copy_board = board.copy()
                    move = board.push_san(the_message)
                    if move.uci() == moves[counter]:
                        if moves[counter] == moves[-1]:
                            boardsvg = chess.svg.board(board=board, orientation=chess.WHITE if board.turn else chess.BLACK, lastmove=board.move_stack[-1])
                            f = open("board.svg", "w")
                            f.write(boardsvg)
                            f.close()
                            os.system("convert -density 200 board.svg board.png")
                            file = discord.File("board.png", filename="image.png")
                            embed = discord.Embed(title=f"Puzzle Complete!", color=discord.Colour.orange())
                            embed.set_image(url="attachment://image.png")
                            embed.set_footer(
                                text=f"Puzzle Completed! || Puzzle link: {puzzle[-1]}")
                            return await ctx.send(file=file, embed=embed)

                        counter+=1
                        board.push_uci(moves[counter])
                        counter+=1
                        boardsvg = chess.svg.board(board=board, orientation=chess.WHITE if board.turn else chess.BLACK, lastmove=board.move_stack[-1])
                        f = open("board.svg", "w")
                        f.write(boardsvg)
                        f.close()
                        os.system("convert -density 200 board.svg board.png")
                        file = discord.File("board.png", filename="image.png")
                        embed = discord.Embed(title=f"Correct!", color=discord.Colour.orange())
                        embed.set_image(url="attachment://image.png")
                        embed.set_footer(
                            text=f"{'White' if board.turn else 'Black'} to move || Puzzle link: {puzzle[-1]}")
                        await ctx.send(file=file, embed=embed)

                    else:
                        copy_board.push_uci(moves[counter])
                        boardsvg = chess.svg.board(board=copy_board, orientation=chess.BLACK if copy_board.turn else chess.WHITE, lastmove=copy_board.move_stack[-1])
                        f = open("board.svg", "w")
                        f.write(boardsvg)
                        f.close()
                        os.system("convert -density 200 board.svg board.png")
                        file = discord.File("board.png", filename="image.png")
                        embed = discord.Embed(title=f"Incorrect! Best move was:", color=discord.Colour.orange())
                        embed.set_image(url="attachment://image.png")
                        embed.set_footer(
                            text=f"Puzzle Failed... || Puzzle link: {puzzle[-1]}")
                        return await ctx.send(file=file, embed=embed)

                except:
                    await ctx.send("Invalid move! Please try again.")

            except asyncio.TimeoutError:
                return await ctx.send(embed=discord.Embed(title="Puzzle timeout! Are you there?", color=discord.Color.red()))



    @commands.command()
    async def chess_challenge(self, ctx, time_format: str = "3+0", user: discord.Member = None):
        if ctx.channel.id != 836512663612686357:
            return await ctx.send("Please only use this command in the <#836512663612686357> channel.")

        try:
            game_time = int(time_format[0])
            increment = int(time_format[2])
            if len(time_format) != 3 or time_format[1] != "+":
                return await ctx.send(
                "Invalid time format specified. Please use this format `3+2` with the first number being the availabe minutes\nand the number after the + being the increment in seconds (It can be 0 for none).")
        except:
            return await ctx.send(
                "Invalid time format specified. Please use this format `3+2` with the first number being the availabe minutes\nand the number after the + being the increment in seconds (It can be 0 for none).")

        the_author = ctx.author
        channel = ctx.channel
        if user is None:
            embed = discord.Embed(title="Chess Battle", color=discord.Colour.orange(),
                                  description=f"{the_author.mention} is inviting anyone to a chess battle with the time of {time_format[0]} minutes with {time_format[2]} second increment!\n\nType `accept` now to accept the challenge and begin a game with them.")
        elif user != the_author and not user.bot:
            embed = discord.Embed(title="Chess Battle", color=discord.Colour.orange(),
                                  description=f"{the_author.mention} is inviting {user.mention} to a chess battle with the time of {time_format[0]} minutes with {time_format[2]} second increment!\n\nType `accept` now to accept the challenge and begin a game with them.")
        else:
            embed = discord.Embed(title="You can't invite yourself or a discord bot to a chess battle!")

        await channel.send(embed=embed)

        def check(m):
            global black, white
            if not user:
                if m.content.lower() == 'accept' and not m.author.bot and m.channel == channel and m.author != the_author:
                    black = random.choice([m.author, the_author])
                    if the_author == black:
                        white = m.author
                    else:
                        white = the_author
                    return True
            else:
                if m.content.lower() == 'accept' and not m.author.bot and m.author == user and m.channel == channel:
                    black = random.choice([m.author, the_author])
                    if the_author == black:
                        white = m.author
                    else:
                        white = the_author
                    return True

        def game_check(m):
            global the_message
            the_message = m.content
            if m.author == (white if board.turn else black) and m.channel == channel:
                return True

        try:
            await self.client.wait_for('message', check=check, timeout=60)
            white_time, black_time = game_time * 60, game_time * 60
            board = chess.Board()
            game = chess.pgn.Game()
            game.headers["White"] = white.name
            game.headers["Black"] = black.name
            game.headers["Site"] = "The Fire Army Discord Server"
            today = date.today()
            game.headers["Date"] = today.strftime("%Y.%m.%d")

            boardsvg = chess.svg.board(board=board, orientation=chess.WHITE if board.turn else chess.BLACK)
            f = open("board.svg", "w")
            f.write(boardsvg)
            f.close()
            os.system("convert -density 200 board.svg board.png")
            file = discord.File("board.png", filename="image.png")
            embed = discord.Embed(title=f"{white} (WHITE) vs {black} (BLACK)", color=discord.Colour.orange())
            embed.set_image(url="attachment://image.png")
            if board.turn:
                embed.set_footer(text=f"White to move || White time: {white_time}s")
            else:
                embed.set_footer(text=f"Black to move || Black time: {black_time}s")
            await channel.send(file=file, embed=embed)
            first_move = True
            while True:
                try:
                    await self.client.wait_for('message', check=game_check, timeout=1)
                    try:
                        if the_message == "resign":
                            await channel.send(embed=discord.Embed(
                                title=f"{white if board.turn else black} resigns! {black if board.turn else white} wins!",
                                color=discord.Color.red()))
                            game.headers["Result"] = "0-1" if board.turn else "1-0"
                            return await channel.send(f"Game PGN:\n```{game}```")

                        move = board.push_san(the_message)
                        if board.turn:white_time+=increment
                        else:black_time+=increment

                        if first_move:
                            node = game.add_variation(move)
                            first_move = False
                        else:
                            node = node.add_variation(move)

                        boardsvg = chess.svg.board(board=board, orientation=chess.WHITE if board.turn else chess.BLACK,
                                                   lastmove=board.move_stack[-1])
                        f = open("board.svg", "w")
                        f.write(boardsvg)
                        f.close()
                        os.system("convert -density 200 board.svg board.png")
                        file = discord.File("board.png", filename="image.png")
                        embed = discord.Embed(title=f"{white} (WHITE) vs {black} (BLACK)", color=discord.Colour.orange())
                        embed.set_image(url="attachment://image.png")
                        if board.turn:
                            embed.set_footer(text=f"White to move || White time: {white_time}s")
                        else:
                            embed.set_footer(text=f"Black to move || Black time: {black_time}s")
                        await channel.send(file=file, embed=embed)

                        if board.is_game_over():
                            the_result = board.result()
                            if the_result == "1-0":
                                await channel.send(embed=discord.Embed(title=f"{white} wins!", color=discord.Color.green()))
                            elif the_result == "0-1":
                                await channel.send(embed=discord.Embed(title=f"{black} wins!", color=discord.Color.green()))
                            else:
                                await channel.send(embed=discord.Embed(title=f"It's a draw!", color=discord.Color.orange()))

                            game.headers["Result"] = the_result
                            return await channel.send(f"Game PGN:\n```{game}```")
                    except:
                        await channel.send("Invalid move! Please try again.")
                except asyncio.TimeoutError:
                    if board.turn:
                        white_time-=1
                        if white_time == 0:
                            await channel.send(embed=discord.Embed(title=f"{white} timeout, {black} wins!", color=discord.Color.red()))
                            game.headers["Result"] = "0-1" if board.turn else "1-0"
                            return await channel.send(f"Game PGN:\n```{game}```")
                    else:
                        black_time-=1
                        if black_time == 0:
                            await channel.send(embed=discord.Embed(title=f"{black} timeout, {white} wins!", color=discord.Color.red()))
                            game.headers["Result"] = "0-1" if board.turn else "1-0"
                            return await channel.send(f"Game PGN:\n```{game}```")

        except asyncio.TimeoutError:
            await channel.send(
                embed=discord.Embed(title="Challenge timeout. Try again later...", color=discord.Color.red()))


def setup(client):
    client.add_cog(FunCommands(client))
