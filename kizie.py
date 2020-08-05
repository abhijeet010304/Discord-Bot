import discord
import functfile as fp
import plots as pl
import verdicts as vd
import matplotlib.pyplot as plt

#read token  act as primary key
def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

client = discord.Client()

@client.event

#greet the newly joined member
async def on_member_join(member):
    for channel in member.server.channels:
        if str(channel) == "compare":
            await client.send_message(f"""Welcome to Compare Channel {member.mention}""")

@client.event
async def on_message(message):

    # message = message.content.lower()
    #server id
    id = client.get_guild(738424005345804370)
    channels = ["compare"]
    if str(message.channel) in channels:
        if message.content.find("!help") != -1:
                embed=discord.Embed(title="Kruskals", description="I am here to help you", color=0xef0101)
                embed.add_field(name="Send me a \"!hello\" then a \"yes\"    for comparing two CF profiles", value="Make sure both Usernames are valid ones to get the best results", inline=True)
                await message.channel.send(embed=embed)



        elif message.content.find("!hello") != -1:
            await message.channel.send("Hey I can compare stats of two Users for you\nDo you want me to do so ?\n")
            #check whether msg is sent by same author or not
            def check(m):
                return m.author == message.author

            msg = await client.wait_for('message', check=check)
            #lowered so that every yes gets accepted
            msg.content = msg.content.lower()
            if msg.content == 'yes':
                usernames = []
                for user_name in ('first', 'second'):
                    await message.channel.send(f"enter {user_name} username")

                    num = await client.wait_for('message', check=check)
                    # print(num.content)

                    usernames.append(num.content)
                await message.channel.send(f'{usernames[0]} and {usernames[1]}')
                await message.channel.send("Retrieving Data Please wait !!\n")

                user1 = usernames[0]

                #call embedThemAll function to get all data from api and
                # send data to decord
                embed_and_rating = fp.embedThemAll(user1)
                await message.channel.send(embed=embed_and_rating[0])
                #ratingPlot_user1 is for plotiing the data in line plot used later to plot rating graph
                ratingPlot_user1 = embed_and_rating[1]

                #get all data to print all types of graphs
                alldata = vd.verdict(user1)

                # print(alldata)
                #ax is plot object returned by fucntion
                #second parameter is index of values in alldata so that only relevent data is sent to function

                await message.channel.send("Retrieving Graphs Please wait !!\n")


                ax = pl.pie_plot(alldata, 4,user1)
                #this wway  we send plots
                plt.savefig(fname='plot')
                await message.channel.send(file=discord.File('plot.png'))
                # plt.show()
                plt.clf()
                ax = pl.pie_plot(alldata, 3,user1)
                plt.savefig(fname='plot')
                await message.channel.send(file=discord.File('plot.png'))
                # plt.show()
                plt.clf()

                ax = pl.pie_plot(alldata, 1,user1)
                plt.savefig(fname='plot')
                await message.channel.send(file=discord.File('plot.png'))
                # plt.show()
                plt.clf()
                ax = pl.pie_plot(alldata, 0,user1)
                plt.savefig(fname='plot')
                await message.channel.send(file=discord.File('plot.png'))
                # plt.show()
                plt.clf()
                #user2
                user2 = usernames[1]
                embed_and_rating = fp.embedThemAll(user2)
                await message.channel.send(embed=embed_and_rating[0])
                ratingPlot_user2 = embed_and_rating[1]
                # embed = fp.embedThemAll(user2)
                # await message.channel.send(embed=embed)
                alldata = vd.verdict(user2)

                # print(alldata)
                # print("verdict done")
                ax = pl.pie_plot(alldata, 4,user2)
                plt.savefig(fname='plot')
                await message.channel.send(file=discord.File('plot.png'))
                # plt.show()
                plt.clf()
                ax = pl.pie_plot(alldata, 3,user2)
                plt.savefig(fname='plot')
                await message.channel.send(file=discord.File('plot.png'))
                # plt.show()
                plt.clf()

                ax = pl.pie_plot(alldata, 1,user2)
                plt.savefig(fname='plot')
                await message.channel.send(file=discord.File('plot.png'))
                # plt.show()
                plt.clf()
                ax = pl.pie_plot(alldata, 0,user2)
                plt.savefig(fname='plot')
                await message.channel.send(file=discord.File('plot.png'))
                # plt.show()
                plt.clf()
                await message.channel.send("Thanks for all your Wait!!  \nFinal Ratings Graph is finally here!!\n"  )
                ax = pl.rating_plot(ratingPlot_user1,ratingPlot_user2,user1,user2)
                plt.savefig(fname='plot')
                await message.channel.send(file=discord.File('plot.png'))
                plt.clf()





            else:
                await message.channel.send("Sorry You did a TYPO to please restart from \"hello\"")


client.run(token)

#abhijeet_server where bot was created 739344586165452821
#https ://discordapp.com/oauth2/authorize?client_id=739344586165452821&scope=bot&permissions=0
#will add valid users later on
