
#used for the main program
import threading

import json

import os
#discord stuff imported
import discord #gets the discord and asyncio librarys
import asyncio
import time

#irc stuff
import pydle


discordMSG = []

#irc
ircNickname = "MyBot"
ircServerIP = "irc.server.net"
ircChannel = "#test"
customStart = ""


##broken
#seems to not like my code in the discordCheckMsg function
##its the part where it sets the value to the delete code.
#this then causes the delete thread to crash trying to find the shift value to go by




##problems
#unsure what will happen in a headless enviroment if the oauth hasnt been set
##if the token and you input a invalid token the first time it will continue to say invalid token for tokens that are even valid



##ideas
#possiblity of use of file io to get the information of the client token for discord and stuff.
#use regex to help format the chat (honestly not needed)


##youtube chat porition
#this will handle getting chat from youtube which will then be pushed to discord

#!/usr/bin/python




####variables
config = {"channelName": "", "pageToken": "", "serverName": "", "discordToken": "","discordToIRCFormating": "", "IRCToDiscordFormatting":""}

botName = "none"

youtube = ""

firstRun = "off"

#used as global varibles and were defined before we start using them to avoid problems down the road
channelToUse = ""

haltDiscordMSG = 0
haltDeleteMSG = 0

##jadens shift code
#delete code is: 98reghwkjfgh8932guicdsb98r3280yioufsdgcgbf98
#delete code is: 98reghwkjfgh8932guicdsb98r3280yioufsdgcgbf98
def shift(value, messages):
    if value == 0:
        return messages
    messagesTemp = [] #Assign temp list
    for i in messages: #For every message
        messagesTemp += [i,] #Add to temp list
    messages.clear() #Delete old list
    for i in messagesTemp[value:]: #For all values after last delete code
        messages += [i,] #Take value from temp list and put in new spot
    messagesTemp.clear() #Delete temp list
    return messages

def checkDeleteCode(messages):
    i = 0 #Set i to 0
    #print("{0} : {1}".format(haltDeleteMSG,haltDiscordMSG)) #debug that isnt really nessisary if this code isnt used.
    while(messages[i] == "98reghwkjfgh8932guicdsb98r3280yioufsdgcgbf98"): #While value at index is the delete code
        i += 1 #Add 1 to i
    return i #Return value of i when message is not delete code



def deleteIrcToDiscordMsgThread():
    global discordMSG, haltDeleteMSG, haltDiscordMSG
    while True:
        #print(discordMSG)
        #print("{0} : {1}".format(haltDeleteMSG,haltDiscordMSG))
        if haltDeleteMSG == 0:
            haltDiscordMSG = 1
            #shiftValue = checkDeleteCode(discordMSG)
            #discordMSG = shift(shiftValue, discordMSG)
            haltDiscordMSG = 0
        #print(discordMSG)
        time.sleep(4)




##discord portion of the bot
#this will be the main code

client = discord.Client() #sets this to just client for reasons cuz y not? (didnt have to be done like this honestly could of been just running discord.Client().)


async def discordSendMsg(msg): #this is for sending messages to discord
    global config
    global channelToUse #pulls in the global variable
    await client.send_message(channelToUse, msg) #sends the message to the channel specified in the beginning
    
async def discordCheckMsg(): #checks for a discord message
    global discordMSG, haltDiscordMSG, haltDeleteMSG
    j = 0
    for msg in discordMSG: #this cycles through the array for messages unsent to discord and sends them
        if msg != "98reghwkjfgh8932guicdsb98r3280yioufsdgcgbf98": 
            await discordSendMsg(msg) #sends message
            discordMSG[j] = "98reghwkjfgh8932guicdsb98r3280yioufsdgcgbf98"#promptly after sets that to the delete code
        j = j + 1
        

@client.event
async def on_ready(): #when the discord api has logged in and is ready then this even is fired
    global ircClient
    if firstRun == "off":
        #these 2 variables are used to keep track of what channel is thre real channel to use when sending messages to discord
        global config , botName, discordMSG, haltDiscordMSG,haltDeleteMSG
        global channelToUse #this is where we save the channel information (i think its a class)
        global channelUsed #this is the channel name we are looking for
        #this is just to show what the name of the bot is and the id
        print('Logged in as') ##these things could be changed a little bit here
        print(client.user.name+ "#" + client.user.discriminator)
        botName = client.user.name+ "#" + client.user.discriminator #gets and saves the bots name and discord tag
        print(client.user.id)
        for server in client.servers: #this sifts through all the bots servers and gets the channel we want
            #should probly add a check in for the server in here im guessing
            for channel in server.channels:
                if channel.name == config["channelName"] and str(channel.type) == "text": #checks if the channel name is what we want and that its a text channel
                    channelToUse = channel #saves the channel that we wanna use since we found it    
        #print(ircClient.connected())
        while True:
            if haltDiscordMSG == 0:
                haltDeleteMSG = 1
                await discordCheckMsg()
                haltDeleteMSG=0
            await asyncio.sleep(1)
            
    else:
        await getFirstRunInfo()
                
            
@client.event
async def on_message(message): #waits for the discord message event and pulls it somewhere
    if firstRun == "off":
        if str(channelToUse.name) == str(message.channel) and str(message.author) != botName: #this checks to see if it is using the correct discord channel to make sure its the right channel. also checks to make sure the botname isnt our discord bot name
            print("{0} : {1}".format(message.author,message.content)) #prints this to the screen
            #await client.send_message(message.channel, 'Hello.')          
            ircSendMSG(message.author,"#test",message.content)

##file load and save stuff

def fileSave(config):
    print("Saving")
    f = open("config.json", 'w') #opens the file your saving to with write permissions
    f.write(json.dumps(config) + "\n") #writes the string to a file
    f.close() #closes the file io


def fileLoad():
    f = open("config.json", 'r') #opens the file your saving to with read permissions 
    config = "" 
    for line in f: #gets the information from the file
        config = json.loads(line) #this will unserialize the table
    return config


##first run stuff


def getToken(): #gets the token 
    global config
    realToken = "false" #this is just for the while loop
    while realToken == "false":
        config["discordToken"] = input("Discord Token: ") #gets the user input
        try:
            client.run(config["discordToken"]) #atempts to run it and if it fails then execute the next bit of code if not then save it and go on
        except:
            print("Please enter a valid token")
            sys.exit(0) #this is a work around for the bug that causes the code not think the discord token is valid even tho it is after the first time of it being invalid
        else:
            realToken = "true"


async def getFirstRunInfo():
    global config 
    print('Logged in as') ##these things could be changed a little bit here
    print(client.user.name)
    print(client.user.id)
    while config["serverName"] == "":
        for server in client.servers: #this sifts through all the bots servers and gets the channel we want
            print(server.name)
            if input("If this is the server you want type yes if not hit enter: ") == "yes":
                config["serverName"] = server.name
                break    
    while config["channelName"] == "":
        for server in client.servers: #this sifts through all the bots servers and gets the channel we want
            #should probly add a check in for the server in here im guessing
            #print(server.name)
            for channel in server.channels:
                if str(channel.type) == "text":
                    print(channel.name)
                    if input("If this is the channel you want type yes if not hit enter: ") == "yes":
                        config["channelName"] #starts the discord bot= channel.name
                        break
    while config["IRCToDiscordFormatting"] == "": #fills the youtube to discord formating
        config["IRCToDiscordFormatting"] = input("""Please enter the chat formatting for chat coming from irc to go to discord. 
{1} is the placeholder for the username
{2} is the placeholder for the message
Ex. "{0} : {1}: """)
    while config["discordToIRCformating"] == "": #fills the discord to youtube formating
        config["discordToIRCFormating"] = input("""Please enter the chat formatting for chat coming from discord to go to irc. 
{0} is the placeholder for the username
{1} is the placeholder for the message
Ex. "{0} : {1}": """)
    print("Configuration complete")
    fileSave(config) #saves the file
    print("Please run the command normally to run the bot")
    await client.close()
            
if os.path.isfile("config.json") == False:#checks if the file exists and if it doesnt then we go to creating it
    print("Config missing. This may mean this is your first time setting this up")
    firstRun = "on"
else:
    config = fileLoad() #if it exists try to load it
if firstRun == "on":
    config = {"channelName": "", "pageToken": "", "serverName": "", "discordToken": "","discordToIRCFormating": "", "IRCToDiscordFormatting":""}
    getToken()



ircClient = 0



##this is the event loop for the irc client
class MyClient(pydle.Client):
    """ This is a simple bot that will greet people as they join the channel. """

    def on_connect(self):
        super().on_connect()
        # Can't greet many people without joining a channel.
        self.join(ircChannel)

    def on_join(self, channel, user):
        super().on_join(channel, user)
        
        
    def on_channel_message(self,target,by,message):
        global discordMSG
        super().on_channel_message(target,by,message) 
        print(target + ":" + by +  ":" + message )
        msg = config["IRCToDiscordFormatting"].format(target,by,message) #this reformats the irc chat for discord
        discordMSG.append(msg)#this adds the new message to the end of the array/list


def ircSendMSG(user,target,msg): #sends a message to the irc
    global config
    ircClient.message(target,config["discordToIRCFormating"].format(user,msg))#sends the message to the irc from whatever
    

#this starts everything for the irc client 
##possibly could of put all this in a class and been done with it?
def start():
    global ircClient
    ircClient = MyClient(ircNickname)
    ircClient.connect(ircServerIP) ##add a option for /pass user:pass this is how znc lets u login
    ircClient.handle_forever()




##main loop for the code
ircThread = threading.Thread(target=start) #creates the thread for the irc client
ircThread.start() #starts the irc bot

#deleteThread = threading.Thread(target=deleteIrcToDiscordMsgThread) #this is broken and needs rewriting
#deleteThread.start()

discordThread = threading.Thread(target=client.run(config["discordToken"]))#creates the thread for the discord bot
discordThread.start() #starts the discord bot




