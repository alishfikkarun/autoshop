# - *- coding: utf- 8 - *-
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from tgbot.data.config import db
from tgbot.data.config import lang_ru as texts
from tgbot.services.crypto_bot import CryptoBot
from tgbot.keyboards.inline_admin import payments_settings_info, payments_settings, payments_back
from tgbot.filters.filters import IsAdmin
from tgbot.data.loader import dp
from tgbot.data import config

try:
    crypto = CryptoBot(config.crypto_bot_token)
except:
    pass


@dp.callback_query_handler(IsAdmin(), text='payments', state="*")
async def payments_settings_choose(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text("<b>⚙️ Выберите способ оплаты</b>", reply_markup=payments_settings())


@dp.callback_query_handler(IsAdmin(), text_startswith="payments:", state="*")
async def payments_info(call: CallbackQuery, state: FSMContext):
    await state.finish()
    way = call.data.split(":")[1]
    s = await db.get_payments()
    def pay_info(way, status):
        if status == "True":
            status = "✅ Включен"
        elif status == "False":
            status = "❌ Выключен"

        msg = f"""
<b>{way}

Статус: <code>{status}</code></b>
"""
        return msg

    if way == "cryptoBot":
        ways = texts.cryptoBot_text
        status = s['pay_crypto']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))


@dp.callback_query_handler(IsAdmin(), text_startswith="payments_on_off:", state="*")
async def off_payments(call: CallbackQuery):

    way = call.data.split(":")[1]
    action = call.data.split(":")[2]
    def pay_info(way, status):
        if status == "True":
            status = "✅ Включен"
        elif status == "False":
            status = "❌ Выключен"

        msg = f"""
<b>{way}

Статус: <code>{status}</code></b>
    """
        return msg

    if way == "cryptoBot":
        ways = texts.cryptoBot_text

        if action == "off":
            await db.update_payments(pay_crypto="False")
        else:
            await db.update_payments(pay_crypto="True")

        s = await db.get_payments()
        status = s['pay_crypto']

        await call.message.edit_text(pay_info(ways, status), reply_markup=payments_settings_info(way, status))


@dp.callback_query_handler(IsAdmin(), text_startswith="payments_balance:", state="*")
async def payments_balance_call(call: CallbackQuery, state: FSMContext):
    await state.finish()
    way = call.data.split(":")[1]

    if way == "cryptoBot":
        ways = texts.cryptoBot_text

        balance = await crypto.get_balance()
        bal = ""
        for ball in balance['result']:
            bal += f"<b>{ball['currency_code']}: <code>{round(float(ball['available']), 2)} {ball['currency_code']}</code></b>\n"

        await call.message.edit_text(text=f"{ways} \n\nВаш баланс: \n{bal}", reply_markup=payments_back())


@dp.callback_query_handler(IsAdmin(), text_startswith="payments_info:", state="*")
async def payments_info_open(call: CallbackQuery, state: FSMContext):
    await state.finish()

    way = call.data.split(":")[1]

    if way == "cryptoBot":
        ways = texts.cryptoBot_text

        await call.message.edit_text(f"{ways} \n\nТокен: <code>{config.crypto_bot_token}</code>", reply_markup=payments_back())
