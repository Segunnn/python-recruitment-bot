import datetime

import discord
from discord.ui import Select, View, Modal, TextInput, Button
from discord.ext import commands


# Это код бота для набора на должности который был написан для дискорд сервера XOLN
XOLN_BEST_DISCORD_IT_SERVER = 'https://discord.gg/xoln-xln-1050370421184278618'
CREATOR = """#+++++++++++++++++++++++++++++++++++++++#
#   █████████████████▀████████████████  #
#   █─▄▄▄▄█▄─▄▄─█─▄▄▄▄█▄─██─▄█▄─▀█▄─▄█  #
#   █▄▄▄▄─██─▄█▀█─██▄─██─██─███─█▄▀─██  #
#   ▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▀▄▄▄▄▀▀▄▄▄▀▀▄▄▀  #
#+++++++++++++++++++++++++++++++++++++++#
"""
print(f"{CREATOR}\n{XOLN_BEST_DISCORD_IT_SERVER}")


bot = commands.Bot(command_prefix=commands.when_mentioned_or("~"), intents=discord.Intents.all(), help_command=None)

TOKEN='token'


@bot.event 
async def on_ready():
    print(f"---------------------------------------\nLogged in as {bot.user} | {bot.user.id}")


@bot.command()
async def START(ctx): # Команда которая отправляет ембед с выпадающим меню в чат

        await ctx.message.delete() # Удаляем сообщение с командой

        select = Select(
                placeholder= "Выберите должность", # Текст на выпадающем меню пока вы на него не нажали
                min_values=1, # Минимальное количество опций которое пользователь может выбрать
                max_values=1, # Максимальное количество опций которое пользователь может выбрать
                options= [ # Сами опции
                    discord.SelectOption(
                        label="Partner Manager",
                        value="id_PM",
                        description="Partner Manager (PM) заключает партнерства.",
                        emoji=discord.PartialEmoji(name="pm", id=1122185251700101170)
                    ),
                    discord.SelectOption(
                        label="Warden",
                        value="id_Warden",
                        description="Warden должен следить за чатом",
                        emoji=discord.PartialEmoji(name="warden", id=1122185331819679824),
                    ),
                    discord.SelectOption(
                        label="Event Manager",
                        value="id_Eventor",
                        description="Event Manager должны делать ивенты",
                        emoji=discord.PartialEmoji(name="event", id=1122185297006968953),
                    )
                ]
            )

        async def my_callback(i): # Действие которое вызвается при выборе опции в модальном меню
            match select.values[0]: # Если вам не известно что это то загуглите: "Python Matching Pattern"
                case "id_PM": # Если пользователь выбрал опцию с значением id_PM то отправляем в чат модальное окно рапологабщееся на строке 175:
                    await i.response.send_modal(MyModalPM())
                case "id_Warden": # Если пользователь выбрал опцию с значением id_Warden то отправляем в чат модальное окно рапологабщееся на строке 200:
                    await i.response.send_modal(MyModalWarden())
                case "id_Eventor": # Если пользователь выбрал опцию с значением id_Eventor то отправляем в чат модальное окно рапологабщееся на строке 216:
                    await i.response.send_modal(MyModalEventor())

        # Строим ембед:
        embed = discord.Embed(title="Подача анкет", 
                              description="""**Выберите должность на которую хотите подать анкету, 
                              после чего заполните форму которая откроется автоматически. 
                              Если модераторы примут вашу заявку то вам в личные сообщения придет уведомление об этом**""",
                                color=3158840)

        embed.add_field(name="Partner Manage | PM", 
                        value="PM заключает партнерства с другими серверамии тем самым помогает продвижанию сервер. Все подробности буду после принятия вас на должность")

        embed.add_field(name="Warden", 
                        value="Warden следит за чатом и в случае если участник нарушит правила Warden быдет должен выдать наказание указанное в правилах сервера")
        embed.add_field(name="Event Manager | EM", value="EM должен делать интересные евенты по IT на серве, EM должен быть готов читать документации и досканально изучать тему по который хочет провести ивент")

        embed.set_image(url="https://i.ibb.co/zGLmJPM/ankets2.png")

        select.callback = my_callback # Обозначаем что при выборе опции будет выполняться функция my_callback
        view = View() # Засовываем класс View в перемнную
        view.add_item(select) # Добавляем наше выпадающее меню в класс View

        await ctx.send(embed=embed, view=view) # Отправляем сообщение с ембедом и выпадающим меню



class ButtonsPM(View): # Кнопка которая отправляется когда участник заполнил модальное окно
    def __init__(self, user_id: int): 
        super().__init__(timeout=None) # Инициализируем все что было в наследственном классе
        self.user_id = user_id # Эта переменная нужна для того чтобы выдать роль пользователю если модераторы одобрят это
    @discord.ui.button(label="Accept",
                       style=discord.ButtonStyle.grey, 
                       custom_id="yes", 
                       emoji=discord.PartialEmoji(id=1051407213509480478, name="verify"))

    async def accept_button(self, i, button): # Действие вызываемое если нажата кнопка Accept
        role = i.guild.get_role(1053541842861432842) # Получаем роль по id

        for children in self.children: # Получаем вторую кнопку присутствующую под сообщением
            children.disabled = True # Делаем ее отключенной
            children.label = "Accepted!" # Меняем ее название на Accepted!

        button.disabled = True # Отключаем данную кнопку
        button.label = "Accepted!"  # Меняем ее название на Accepted!

        us = i.guild.get_member(self.user_id) # Получаем пользователя по id полученое в __init__

        await us.add_roles(role) # Добавляем полученому по id пользователю полученую по id роль

        em = discord.Embed(title="Вы приняты на должность Partner Manager", 
                           description=f"Модератор {i.user} принял вас. Если есть вопросы то пишите ему")

        await us.send("Вы приняты!", embed=em) # Отправляем полученому по id пользователю сообщение с ембедом в лс
        await i.response.edit_message(view=self) # Изменяем кнопки

    @discord.ui.button(label="Decline", 
                       style=discord.ButtonStyle.grey, 
                       custom_id="no", 
                       emoji=discord.PartialEmoji(id=1053641617438937138, name="x1")) 
    async def decline_button(self, i, button): # Здесь делаем все как в кнопке повыше, но в этот раз не выдаем роль

        for children in self.children:
            children.disabled = True
            children.label = "Declined!"

        button.disabled = True
        button.label = "Declined!"

        us = i.guild.get_member(self.user_id)

        await us.send("Модераторы отклонили вашу заявку")
        await i.response.edit_message(view=self)

class ButtonsWarden(View): # Длаем все что описанно в классе выше ^, но немного по другому
    def __init__(self, user_id: int):
        super().__init__(timeout=None)
        self.user_id = user_id
    @discord.ui.button(label="Accept",
                       style=discord.ButtonStyle.grey, 
                       custom_id="yes", 
                       emoji=discord.PartialEmoji(id=1051407213509480478, name="verify"))
    async def accept_button(self, i, button):
        role = i.guild.get_role(1050604300482662441)
        for children in self.children:
            children.disabled = True
            children.label = "Accepted!"
        button.disabled = True
        button.label = "Accepted!"
        us = i.guild.get_member(self.user_id)
        await us.add_roles(role)
        em = discord.Embed(title="Вы приняты на должность Warden", 
                           description=f"Модератор {i.user} принял вас. Если есть вопросы то пишите ему")
        await us.send("Вы приняты!", embed=em)
        await i.response.edit_message(view=self)

    @discord.ui.button(label="Decline",
                       style=discord.ButtonStyle.grey, 
                       custom_id="no", 
                       emoji=discord.PartialEmoji(id=1053641617438937138, name="x1"))
    async def decline_button(self, i, button):
        for children in self.children:
            children.disabled = True
            children.label = "Declined!"
        button.disabled = True
        button.label = "Declined!"
        us = i.guild.get_member(self.user_id)
        await us.send("Модераторы отклонили вашу заявку, удачи в следующий раз")
        await i.response.edit_message(view=self)

class ButtonsEM(View): # Длаем все что описанно в классе выше прошлого ^^, но немного по другому
    def __init__(self, user_id: int):
        super().__init__(timeout=None)
        self.user_id = user_id
    @discord.ui.button(label="Accept",
                       style=discord.ButtonStyle.grey, 
                       custom_id="yes", 
                       emoji=discord.PartialEmoji(id=1051407213509480478, name="verify"))
    async def accept_button(self, i, button):
        for children in self.children:
            children.disabled = True
            children.label = "Accepted!"
        button.disabled = True
        button.label = "Accepted!"
        role = i.guild.get_role(1121372281273335808)
        us = i.guild.get_member(self.user_id)
        await us.add_roles(role)
        em = discord.Embed(title="Вы приняты на должность Event Manager", 
                           description=f"Модератор {i.user} принял вас. Если есть вопросы то пишите ему")
        await us.send("Вы приняты!", embed=em)
        await i.response.edit_message(view=self)

    @discord.ui.button(label="Decline",
                       style=discord.ButtonStyle.grey, 
                       custom_id="no", 
                       emoji=discord.PartialEmoji(id=1053641617438937138, name="x1"))
    async def decline_button(self, i, button):
        for children in self.children:
            children.disabled = True
            children.label = "Declined!"
        button.disabled = True
        button.label = "Declined!" # change the button's label to something else
        us = i.guild.get_member(self.user_id)
        await us.send("Модераторы отклонили вашу заявку. Удачи в следующий раз")
        await i.response.edit_message(view=self)


# Дальше идут модальные окна
# Я опять прокоментирую только первое модальнео окно т.к остальные от него почти нечем не отличаются

class MyModalPM(Modal, title="Partner Manager"): # Создаем класс с модальным окном с вопросами на должность Partner Manager
    # Первый вопрос:
    answer1 = TextInput(label="Расскажите о своем опыте работы", # Сам вопрос
                      style=discord.TextStyle.long, # Стиль (большое поле для ввода или маленькоу)
                      placeholder="Опыт работы", # То что написанно на поле ввода пока вы не нажали на него
                      required=True, # Обязательно ли в него что-то написать
                      min_length=5,  # Минимальная длина писанины
                      max_length=50) # Максимальная длина писанины
    answer2 = TextInput(
                    label="Готовы ли вы заключать 3+ партнерства в день?", # Сам вопрос
                    style=discord.TextStyle.short, # Стиль (большое поле для ввода или маленькоу)
                    placeholder="Я вижу, вы, готовы", # То что написанно на поле ввода пока вы не нажали на него
                    default="Да/Нет", # Текст который автоматически напечатан в поле ввода
                    required=True, # Обязательно ли в него что-то написать
                    min_length=2,  # Минимальная длина писанины
                    max_length=10) # Максимальная длина писанины

    async def on_submit(self, i): # Когда пользователь все заполнил и нажимает кнопку Подтвердить
        # Создаем ембед
        embed = discord.Embed(color=3158840, title="Новая анкета | PM", timestamp=datetime.datetime.now())
        embed.add_field(name="Опыт работы", value=f"{self.answer1}", inline=False)
        embed.add_field(name="Готовность заключать 3+ партнерств в день", value=f"{self.answer2}", inline=False)
        embed.add_field(name="Username | ID", value=f"{i.user} | {i.user.id}", inline=False)

        channel = bot.get_channel(1075348969527464017) # Получаем канал модераторов по id
        await channel.send(embed=embed, view=ButtonsPM(i.user.id)) # Отправляем в полученый канал ембед и кнопки которые мы писали раньше
        await i.response.send_message(f"**Ваша заявка успешно отправлена, ожидайте ответа модераторов от бота в личных сообщениях. Удачи**", 
                                      ephemeral=True) # Отправляем в чат сообщение которое видит только тот кто отправил заявку

# Остальные два модальных окна я коментировать не буду т.к они почти на отличаются от первого
class MyModalWarden(Modal, title="Warden"):
    answer1 = TextInput(label="Расскажите о своем опыте работы",
                        style=discord.TextStyle.long,
                        placeholder="Опыт работы",
                        required=True,
                        min_length=5,
                        max_length=50)
    answer2 = TextInput(
                    label="Сколько времени вы готовы уделять серверу?",
                    style=discord.TextStyle.short,
                    placeholder="Я вижу, вы, готовы",
                    default="25 часов",
                    required=True,
                    min_length=2,
                    max_length=10)

    async def on_submit(self, i):
        embed = discord.Embed(color=3158840, title="Новая анкета | Warden", timestamp=datetime.datetime.now())
        embed.add_field(name="Опыт работы", value=f"{self.answer1}", inline=False)
        embed.add_field(name="Время уделяемое серверу в день", value=f"{self.answer2}", inline=False)
        embed.add_field(name="Username | ID", value=f"{i.user} | {i.user.id}", inline=False)
        channel = bot.get_channel(1075348969527464017)
        await channel.send(embed=embed, view=ButtonsWarden(i.user.id))
        await i.response.send_message(f"**Ваша заявка успешно отправлена, ожидайте ответа модераторов от бота в личных сообщениях. Удачи**", ephemeral=True)

class MyModalEventor(Modal, title="Partner Manager"):
    answer1 = TextInput(label="Расскажите о своем опыте работы", style=discord.TextStyle.long, placeholder="Опыт работы", required=True, min_length=5, max_length=50)
    answer2 = TextInput(label="Оцените вашу креативность 1 - 100", style=discord.TextStyle.short, placeholder="Все 100", required=True, min_length=1, max_length=3)
    answer3 = TextInput(label="Готовы ли вы читать документации", style=discord.TextStyle.short, placeholder="Конечно да!", required=True, default="Конечно!", min_length=2, max_length=10)

    async def on_submit(self, i):
        embed = discord.Embed(color=3158840, title="Новая анкета | Eventor", timestamp=datetime.datetime.now())
        embed.add_field(name="Опыт работы", value=f"{self.answer1}", inline=False)
        embed.add_field(name="Креативность 1-100", value=f"{self.answer2}", inline=False)
        embed.add_field(name="Готовность читать документации", value=f"{self.answer3}", inline=False)
        embed.add_field(name="Username | ID", value=f"{i.user} | {i.user.id}", inline=False)
        channel = bot.get_channel(1075348969527464017)
        await channel.send(embed=embed, view=ButtonsEM(i.user.id))
        await i.response.send_message(f"**Ваша заявка успешно отправлена, ожидайте ответа модераторов от бота в личных сообщениях. Удачи**", ephemeral=True)


if __name__ == "__main__": 
    bot.run(TOKEN) # Запускаем бота
