#!/usr/bin/env python3
import re
from discord.ext import commands
from Users import Users

# short decorator function declaration, confirm that command user has an account in database
def has_account():
    def predicate(ctx):
        user = Users(ctx.message.author.id)
        if user.find_user() == 0:
            return False
        else:
            return True

    return commands.check(predicate)

<<<<<<< HEAD
# short decorator function declaration, confirm that command user has NO account in database
def has_no_account():
    def predicate(ctx):
        user = Users(ctx.message.author.id)
        if user.find_user() == 0:
            return True
        else:
            return False
    return commands.check(predicate)


=======
>>>>>>> 008c5f06951d5649d50dd67bce87cc913d6260b0
class Account:
    def __init__(self, client):
        self.client = client

    @commands.command(name='create', description='make a user',
                      brief='start a user account', aliases=['register'], pass_context=True)
    async def register(self, context):
        # create new user instance with their discord ID to store in database
        new_user = Users(context.message.author.id)

        if new_user.find_user() == 1:
            await self.client.say('<:worrymag1:531214786646507540> You **already** have an account registered!')
            return

        msg = new_user.add_user()
        await self.client.say(context.message.author.mention + msg)

    @has_account()
    @commands.command(name='delete', description='delete your user',
                      brief='delete your user account', aliases=['del'], pass_context=True)
    async def delete(self, context):
        # create user instance with their discord ID, delete user from database based off their discord ID
        await self.client.say('Do you really want to delete your account? Type **confirm** to confirm.')
        # wait for user's input
        guess = await self.client.wait_for_message(author=context.message.author, timeout=60)
        if guess.clean_content.upper() == 'CONFIRM':
            user = Users(context.message.author.id)
            await self.client.say(context.message.author.mention + user.delete_user())
        else:
            await self.client.say(context.message.author.mention + ' Cancelled deletion of account')

    @has_account()
    @commands.command(name='money', aliases=['m', 'MONEY'], pass_context=True)
    async def money(self, context, *args):
        # this 'try' will process if they want to check another person's bank account
        # it will only process if they passed that user as an argument
        try:
            # use regex to extract only numbers to get their discord ID,
            # ex: <@348195501025394688> to 348195501025394688
            # create user instance with their target's discord ID, check database for their money field
            user = Users(re.findall("\d+", args[0])[0])
            await self.client.say(context.message.author.mention +
                                  " That user's :moneybag: balance: " + user.get_user_money())
        # if they passed no parameter, get their own money
        except:
            # create user instance with their discord ID, check database for their money field
            user = Users(context.message.author.id)
            await self.client.say(context.message.author.mention +
                                  " :moneybag: balance: " + user.get_user_money())

    @has_account()
    @commands.command(name='bank', aliases=['balance'], pass_context=True)
    async def check_bank_balance(self, context):
        user = Users(context.message.author.id)
        bank_amount = user.get_user_bank_balance()
        await self.client.say(f"{context.message.author.mention} :computer: Bank balance is: {user.get_user_bank_balance()}")

    @has_account()
    @commands.cooldown(1, 14400, commands.BucketType.user) # 4hours cooldown to avoid abuse
    @commands.command(name='transfer', description='transfer a giving ammount to user bank',
                      brief='transfer money', aliases=['xfer'], pass_context=True)
    async def deposit_bank(self, context, *args):
        if args:
            amount = int(args[0])
            user = Users(context.message.author.id)
            user_money = user.get_user_money(0)
            user_bank_money = user.get_user_bank_balance(0)

            # check if user has the amount in his/her bag
            if amount > user_money or amount < 1:
                await self.client.say(" You don't have enough money to "
                                      "make a deposit <a:pepehands:485869482602922021> "
                                      + context.message.author.mention)
                return
            # check if user is carrying at least $50 in his/her bag
            aux = user_money-50
            if user_money-amount < 50:
                await self.client.say(f"Invalid amount, you have to carry at "
                                      f"least $50 in your bag!\n"
                                      f"Max amount for transfering is: ${aux}")
                return

            new_user_money = amount * -1 # autistic but ok :feelsbothman:
            await self.client.say(f"{context.message.author.mention} Thank you! Your money has been transfered "
                                  f" <a:pepehack:525159339007148032>")
            await self.client.say(f'{context.message.author.mention} {user.update_user_bank_balance(amount)}')
            await self.client.say(f'{context.message.author.mention} {user.update_user_money(new_user_money)}')
        else:
            await self.client.say("Invalid input!\n ```Usage: '=transfer x' or '=xfer x' -- x being money to deposit```")
            return

    @has_account()
    @commands.command(name='withdraw', description='withdraw a giving amount to user bag',
                      brief='withdraw money', aliases=['draw', 'extract'], pass_context=True)
    async def withdraw_bank(self, context, *args):
        if args:
            user = Users(context.message.author.id)
            amount = int(args[0])

            # check if user has the amount in his bank Account
            if amount > user.get_user_bank_balance(0) or amount < 1:
                await self.client.say(f" You don't have ${amount} in your bank."
                                      f" <:pepethink1:356600456165851136>")
                return

            new_user_bank_money = amount * -1
            await self.client.say(f"{context.message.author.mention} Thank you! {user.update_user_money(amount)}\n"
                                  f" {user.update_user_bank_balance(new_user_bank_money)}")
        else:
            await self.client.say("Invalid input!\n ```Usage: '=draw x' or '=extract x' -- x being money to withdraw```")
            return

    @has_account()
    @commands.command(name='level', aliases=['LEVEL', 'lvl', 'LVL'], pass_context=True)
    async def level(self, context, *args):
        # this 'try' will process if they want to check another player's level
        # it will only process if they passed that user as an argument
        try:
            # use regex to extract only numbers to get their discord ID,
            # ex: <@348195501025394688> to 348195501025394688
            # create user instance with their target's discord ID, check database for their level field
            user = Users(re.findall("\d+", args[0])[0])
            await self.client.say(context.message.author.mention +
                                  " That user's level: " + user.get_user_level())
        # if they passed no parameter, get their own level
        except:
            # create user instance with their discord ID, check database for their level field
            user = Users(context.message.author.id)
            await self.client.say(context.message.author.mention +
                                  " Your level: " + user.get_user_level())


    @has_account()
    @commands.command(name='give', aliases=['DONATE', 'GIVE', 'pay', 'donate', 'PAY', 'gift', 'GIFT'], pass_context=True)
    async def give(self, context, *args):
        # will automatically go to exception if all arguments weren't supplied correctly
        try:
            receiver_string = args[0]
            amnt = int(args[1])
            if amnt < 1:
                await self.client.say("Can’t GIFT DEBT!")
                return
            # create user instance with their discord ID, check database for their level field
            donator = Users(context.message.author.id)
            # use regex to extract only numbers from "receiver_string" to get their discord ID,
            # ex: <@348195501025394688> to 348195501025394688
            receiver = Users(re.findall("\d+", receiver_string)[0])

            # check if receiver has account
            if receiver.find_user() == 0:
                await self.client.say(context.message.author.mention +
                                      " The target doesn't have an account."
                                      "\nUse **=create** to make one.")
                return
            # check if donator has enough money for the donation
            # pass 0 to return integer version of money, see USERS.PY function
            if int(amnt) > donator.get_user_money(0):
                await self.client.say(context.message.author.mention +
                                      " You don't have enough money for that donation..."
                                      " <a:pepehands:485869482602922021> ")
                return

            # pass the donation amount, pass the receiver user object, and pass the receiver's string name
            msg = donator.donate_money(int(amnt), receiver, receiver_string)
            await self.client.say(msg)
        except:
            await self.client.say(context.message.author.mention +
                                  '```ml\nuse =give like so: **=give @user X**    -- X being amnt of money to give```')

    @has_account()
    @commands.command(name='stats', aliases=['battles', 'BRECORDS', 'STATS'], pass_context=True)
    async def battlerecords(self, context, *args):
        # this 'try' will process if they want to check another person's battle records
        # it will only process if they passed that user as an argument
        try:
            # use regex to extract only numbers to get their discord ID,
            # ex: <@348195501025394688> to 348195501025394688
            # create user instance with their target's discord ID, check database for their money field
            user = Users(re.findall("\d+", args[0])[0])
            await self.client.say(context.message.author.mention + " _Target's battle stats..._"
                                  + user.get_user_battle_stats())

        # if they passed no parameter, get their own records
        except:
            # create user instance with their discord ID, check database for their level field
            user = Users(context.message.author.id)
            await self.client.say(context.message.author.mention + user.get_user_battle_stats())

    @has_account()
    @commands.command(name='levelup', aliases=['lup', 'LEVELUP'], pass_context=True)
    async def levelup(self, context):
        # create instance of user who wants to level-up
        user = Users(context.message.author.id)
        # get the user's current level
        # calculate the cost of their next level-up
        user_level = user.get_user_level(0) # get int version of level, SEE USERS.PY
        # level up cost algorithm, inspired by D&D algorithm
        level_up_cost = int(300 * ((user_level + 1)**1.43) - (300 * user_level))

        if user_level == 13:
            self.client.say('You are already level 13, the max level!')
            return

        # check if they have enough money for a level-up
        if user.get_user_money(0) < level_up_cost:
            await self.client.say(context.message.author.mention + ' Not enough money for level-up...'
                                                                 + ' <a:pepehands:485869482602922021>\n'
                                                                 + '** **\nAccount balance: '
                                                                 + user.get_user_money() + '\nLevel **'
                                                                 + str(user_level + 1) + '** requires: **$'
                                                                 + str(level_up_cost) + '**')
            return

        # passed conditional, so they have enough money to level up
        # confirm if they really want to level-up
        await self.client.say(context.message.author.mention + '\nAccount balance: ' + user.get_user_money()
                                                             + '\nLevel **' + str(user_level + 1)
                                                             + '** requires: **$' + str(level_up_cost)
                                                             + '**\n** **\nDo you want to level-up?'
                                                             + ' Type **confirm** to confirm.')

        # wait for user's input
        confirm = await self.client.wait_for_message(author=context.message.author, timeout=60)
        if confirm.clean_content.upper() == 'CONFIRM':
            # deduct the level-up cost from their account
            user.update_user_money(level_up_cost*-1)
            # increase level by 1 and print new level
            await self.client.say(context.message.author.mention + user.update_user_level())
        else:
            await self.client.say(context.message.author.mention + ' Cancelled level-up.')


    @has_account()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command(name='daily', aliases=['DAILY', 'dailygamble'], pass_context=True)
    async def daily(self, context):
        # create instance of user who wants to get their daily money
        user = Users(context.message.author.id)
        # get the user's current level
        # calculate the cost of their next level-up
        user_level = user.get_user_level(0) # get int version of level, SEE USERS.PY
        dailyreward = user_level * 60

        await self.client.say('<a:worryswipe:525755450218643496> Daily **$' + str(dailyreward) +
                              '** received! <a:worryswipe:525755450218643496>\n' + user.update_user_money(dailyreward))
              
def setup(client):
    client.add_cog(Account(client))
