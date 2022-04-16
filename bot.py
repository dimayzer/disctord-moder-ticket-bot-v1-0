import time
import discord
from discord.ext import commands
import string
from config import *
import random
from discord.ext import tasks
from discord_components import *
bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())
logs_id = 942391965226500166
role1_id =754029920518144010
role2_id =873222057498927134
enter_channel = 942459052221431828

#запуск бота
@bot.event
async def on_ready():
	print("Бот запущен!")


#ивент на присоединение пользователя к серверу
@bot.event
async def on_member_join (member):
	role = discord.utils.get (member.guild.roles, id=595307817829793794) #айди роли, которая выдается каждому зашедшему
	channel = bot.get_channel(logs_id)
	enter_channel_id = bot.get_channel(enter_channel) #канал с логами
	emb = discord.Embed(title="Информация о пользователе", color=member.color)
	emb.add_field(name="Имя:", value=member.mention,inline=False)
	emb.add_field(name="Айди пользователя:", value=member.id,inline=False)
	t = member.status
	if t == discord.Status.online:
		d = " В сети"

	t = member.status
	if t == discord.Status.offline:
		d = "⚪ Не в сети"

	t = member.status
	if t == discord.Status.idle:
		d = " Не активен"

	t = member.status
	if t == discord.Status.dnd:
		d = " Не беспокоить"

	emb.add_field(name="Активность:", value=d,inline=False)
	emb.add_field(name="Статус:", value=member.activity,inline=False)
	emb.add_field(name="Акаунт был создан:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),inline=False)
	emb.set_thumbnail(url=member.avatar_url)
	await enter_channel_id.send(embed = emb) #отправка логов
	await channel.send(f"[log] {member.mention} зашел на сервер") #отправка логов
	print(f"[log] {member.mention} зашел на сервер")
	await member.add_roles( role ) #выдача роли зашедшему
	try:
		embed = discord.Embed(
			title = "Добро пожаловать на сервер!",
			description = f"{member.mention}, добро пожаловать на сервер, для получения ролей заходи в канал <#763118872877727821>",
			color =0x0c0c0c
			)
		msg = await member.send(embed=embed) #отправление приветственного сообещния в лс пользователю
	except Exception as e:
		await channel.send(f"[log] Начальное сообщение пользователю {member.mention} не было отправлено: {e}") #отправка логов		



# выдаем пользователю роли по нажатию
@bot.event
async def on_raw_reaction_add(payload):
	ourMessageID = 964872911863283813 #айди сообщения, к которому аттачатся роли

	if ourMessageID == payload.message_id:
		member = payload.member
		guild = member.guild


		emoji = payload.emoji.name
		if  emoji == '💎':
			role = discord.utils.get(guild.roles, name = "💎 Rockford 💎")
	


		await member.add_roles(role) #добавляем роль
		channel = bot.get_channel(logs_id) #снова логи
		await channel.send(f"[log] {member.mention} получил роль {role.mention}")
		print(f"[log] {member} получил роль {role}")


#удаляем роли у пользователя по нажатию
@bot.event
async def on_raw_reaction_remove(payload):
	ourMessageID = 964872911863283813

	if ourMessageID == payload.message_id:
		guild = await(bot.fetch_guild(payload.guild_id))
		emoji = payload.emoji.name
		if emoji == '💎':
			role = discord.utils.get(guild.roles, name = "💎 Rockford 💎")



		member = await(guild.fetch_member(payload.user_id))
		if member is not None:
			await member.remove_roles(role)
			channel = bot.get_channel(logs_id)
			await channel.send(f"[log] {member.mention} снял роль {role.mention}")
			print(f"[log] {member} снял роль {role}")

		else:
			print("[log] Участник не найден!")


#приветственное сообщение
@bot.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def welcome(ctx):
	embed = discord.Embed(
		title = "Добро пожаловать на сервер!",
		description = "Для получения роли нажми на эмоцию",
		color =0x1abc9c
		)

	msg = await ctx.send(embed=embed)
	await msg.add_reaction('💎')
		


#создание тикетов
@bot.command()
async def ticket(ctx):
	channell = bot.get_channel(logs_id) #канал с логами
	channel_s = ctx.message.channel.id
	guild = ctx.message.guild
	if channel_s == 942428554480726077:
		length = 8
		letters_and_digits = string.ascii_letters + string.digits
		num = ''.join(random.sample(letters_and_digits, length)) #генерация номера
		ticket_channel = await guild.create_text_channel(f"ticket-{num}") #создаем канал для тикета
		print(f"[log] {ctx.message.author} создал тикет")

		embed = discord.Embed(
			title = f"Вы успешно создали тикет **№{num}**!",
			description = f"{ctx.message.author.mention}, подробно опишите свою проблему и дождитесь ответа администрации!",
			color =0x1abc9c
			)
		await ticket_channel.send(embed=embed)
		role_everyone = ctx.guild.get_role(role_id=595212036909170689) #роль everyone
		overwrite1 = discord.PermissionOverwrite()
		overwrite1.send_messages = False
		overwrite1.read_messages = False
		overwrite1.read_message_history = False
		overwrite1.attach_files = False
		overwrite1.view_channel = False

		await ticket_channel.set_permissions(role_everyone, overwrite=overwrite1) #закрываем доступ роли everyone к каналу тикет

		overwrite = discord.PermissionOverwrite()
		overwrite.send_messages = True
		overwrite.read_messages = True
		overwrite.read_message_history = True
		overwrite.attach_files = True
		overwrite.view_channel = True

	    # Задаём права автору сообщения и тегаем
		await ticket_channel.set_permissions(ctx.message.author, overwrite=overwrite)

		
		msg = await channell.send(f"[log] {ctx.message.author.mention} создал тикет <#{ticket_channel.id}> **{ticket_channel}**. Тег админов: {ctx.guild.get_role(role_id=role1_id).mention}, {ctx.guild.get_role(role_id=role2_id).mention}")
	else:
		await ctx.message.delete()

#создание войс канала
@bot.command()
async def voice(ctx, name):
    
	guild = ctx.message.guild
	channel = ctx.message.channel.id
	reference = guild.get_channel(channel) # берем какой-нибудь канал за "основу"
	name = "{} {}".format(reference, name)
	if channel == 595298337683406888: #айди канала, из которого нельзя создать войс
		embed = discord.Embed(
		title = "Ошибка!",
		description = f"{ctx.message.author.mention}, Вы не можете создать войс-канал!",
		color =0x1abc9c
		)
		msg = await ctx.send(embed=embed)

	elif channel == 595298111778193428: #айди канала, из которого нельзя создать войс
		embed = discord.Embed(
		title = "Ошибка!",
		description = f"{ctx.message.author.mention}, Вы не можете создать войс-канал!",
		color =0x1abc9c
		)
		msg = await ctx.send(embed=embed)

	else:	
		channel = await guild.create_voice_channel(
	    name, 
	    position=reference.position+1, # создаём канал под "основой"
	    category=reference.category, # в категории канала-"основы"
	    reason="создан с помощью бота by. dimayzer", # С причиной "ABC" (отображается в Audit Log)
		)
		
		embed = discord.Embed(
		title = "Готово!",
		description = f"{ctx.message.author.mention}, Вы успешно создали войс-канал <#{channel.id}>!",
		color =0x1abc9c
		)
		msg = await ctx.send(embed=embed)
		channell = bot.get_channel(logs_id)
		
		await channell.send(f"[log] {ctx.message.author.mention} создал войс канал <#{channel.id}> **{name}**")
		print(f"[log] {ctx.message.author} создал войс канал {name}")


#удаление канала, если в нем 0 юзеров
@bot.event
async def on_voice_state_update(member, before, after):
	channel = bot.get_channel(logs_id)
	if before.channel is None and after.channel is not None:
		await channel.send(f"[log] {member.mention} зашёл в канал <#{after.channel.id}> **{after.channel}**, в канале пользователей: {len(after.channel.members)}")
	elif before.channel is not None and after.channel is None:
		await channel.send(f"[log] {member.mention} вышел из канала <#{before.channel.id}> **{before.channel}**, в канале пользователей: {len(before.channel.members)}")
		channel1 = before.channel
		if (len(before.channel.members)) == 0: #проверяем сколько юзеров в канале
			channel = bot.get_channel(logs_id)
			if channel1.id == 942419810422255626: #проверяем, какой это канал (можно удалить или нет)
				await channel.send(f"[log] Канал <#{before.channel.id}> **{channel1}** свободен.")
			elif channel1.id == 942418430156472353:
				await channel.send(f"[log] Канал <#{before.channel.id}> **{channel1}** свободен.")
			elif channel1.id == 595302393948667967:
				await channel.send(f"[log] Канал <#{before.channel.id}> **{channel1}** свободен.")
				



			else:
				await channel.send(f"[log] {member.mention} вышел из канала **{channel1}**. Канал удален.")
				await channel1.delete() #удаляем канал
				print(f"[log] {member.mention} вышел из канала **{channel1}**. Канал удален.")

@bot.command()
@commands.has_permissions(administrator=True) #обязательно права админа
async def del_ticket(ctx):

	channel = ctx.message.channel
	await channel.delete() #удаляем канал с тикетом
	channell = bot.get_channel(logs_id)
	await channell.send(f"[log] {ctx.message.author.mention} удалил тикет**{channel}**.")
	print(f"[log] {ctx.message.author.mention} удалил тикет**{channel}**.")


#приветственное сообщение
@bot.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def wel_help(ctx):
	file = discord.File("1.mp4")
	embed = discord.Embed(
		title = "Команды бота",
		color =0x1abc9c
		)
	embed.add_field(name = "!voice {название}", value = "создается голосовой канал. Можно использовать в каналах вашего сервера.", inline = False)
	embed.add_field(name = "!ticket", value = "создается тикет. Для создания необходимо перейти в канал <#942428554480726077>.", inline = False)

	msg = await ctx.send(embed=embed, file=file)



bot.run(TOKEN)
