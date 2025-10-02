from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
import logging
import asyncio
from aiogram import Bot,Dispatcher,types,F
from aiogram.filters import Command

admin_id = 5570471897
api = '8268639113:AAFN1cqURXUD68266f_pM-F728ZMwXkIkqY'
bot = Bot(api)
dp=Dispatcher()
class ToAdminState(StatesGroup):
    text = State()
    yes_no = State()
    photo = State()



@dp.message(Command('start'))
async def send_hi(sms:types.Message):
    await sms.answer(text='Salem')

@dp.message(F.text=='Feedback')
async def send_to_admin(sms:types.Message,state:FSMContext):
    await sms.answer(text='Bizge xat jollan:')
    await state.set_state(ToAdminState.text)

@dp.message(ToAdminState.text)
async def save_text(sms:types.Message,state:FSMContext):
    await state.update_data(text=sms.text)
    await sms.answer(text='Sizde suwret barma?')
    await state.set_state(ToAdminState.yes_no)
   

@dp.message(ToAdminState.yes_no)
async def save_answer(sms:types.Message,state:FSMContext):
    if sms.text=='yes':
        await state.update_data(yes_no=sms.text)
        await sms.answer(text='Aha, suwret jiberin:')
        await state.set_state(ToAdminState.photo)
    else:
        await sms.answer(text='Hop, sizdin xat adminge jollandi')
        datas = await state.get_data()
        await bot.send_message(chat_id=admin_id,
                               text=datas['text'])
        await state.clear()
    # await state.update_data(text=sms.text)
    # await sms.answer(text='Sizde suwret barma?')
    # await state.set_state(ToAdminState.yes_no)

@dp.message(ToAdminState.photo)
async def save_photo(sms:types.Message,state:FSMContext):
    await state.update_data(photo=sms.photo[0].file_id)
    datas = await state.get_data()
    await state.clear()
    await bot.send_photo(chat_id=admin_id,
                         photo=datas['photo'],
                         caption=datas['text'])
    # print(sms.photo)


async def main():
    await dp.start_polling(bot)


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
