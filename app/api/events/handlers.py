async def on_startup():  # set telegram webhook on startup
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post(WEBHOOK_PATH)  # telegram events handler
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


@dp.message_handler(commands="start")  # start command handler
async def new_message(message: types.Message):
    text = 'REACT'
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Launch react', web_app=WebAppInfo(url=REACT_URL)))
    await bot.send_message(message.chat.id, text, reply_markup=keyboard)


@app.on_event("shutdown")  # close session on shutdown event
async def on_shutdown():
    await bot.get_session()
    await bot.session.close()
    logging.info("Bot stopped")
