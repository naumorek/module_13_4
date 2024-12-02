'''
Группа состояний:
Импортируйте классы State и StatesGroup из aiogram.dispatcher.filters.state.
Создайте класс UserState наследованный от StatesGroup.
Внутри этого класса опишите 3 объекта класса State: age, growth, weight (возраст, рост, вес).
Эта группа(класс) будет использоваться в цепочке вызовов message_handler'ов. Напишите следующие функции для обработки состояний:
Функцию set_age(message):
Оберните её в message_handler, который реагирует на текстовое сообщение 'Calories'.
Эта функция должна выводить в Telegram-бот сообщение 'Введите свой возраст:'.
После ожидать ввода возраста в атрибут UserState.age при помощи метода set.
Функцию set_growth(message, state):
Оберните её в message_handler, который реагирует на переданное состояние UserState.age.
Эта функция должна обновлять данные в состоянии age на message.text (написанное пользователем сообщение). Используйте метод update_data.
Далее должна выводить в Telegram-бот сообщение 'Введите свой рост:'.
После ожидать ввода роста в атрибут UserState.growth при помощи метода set.
Функцию set_weight(message, state):
Оберните её в message_handler, который реагирует на переданное состояние UserState.growth.
Эта функция должна обновлять данные в состоянии growth на message.text (написанное пользователем сообщение). Используйте метод update_data.
Далее должна выводить в Telegram-бот сообщение 'Введите свой вес:'.
После ожидать ввода роста в атрибут UserState.weight при помощи метода set.
Функцию send_calories(message, state):
Оберните её в message_handler, который реагирует на переданное состояние UserState.weight.
Эта функция должна обновлять данные в состоянии weight на message.text (написанное пользователем сообщение). Используйте метод update_data.
Далее в функции запомните в переменную data все ранее введённые состояния при помощи state.get_data().
Используйте упрощённую формулу Миффлина - Сан Жеора для подсчёта нормы калорий (для женщин или мужчин - на ваше усмотрение). Данные для формулы берите из ранее объявленной переменной data по ключам age, growth и weight соответственно.
Результат вычисления по формуле отправьте ответом пользователю в Telegram-бот.
Финишируйте машину состояний методом finish().
!В течение написания этих функций помните, что они асинхронны и все функции и методы должны запускаться с оператором await.

Пример результата выполнения программы:


Примечания:
При отправке вашего кода на GitHub не забудьте убрать ключ для подключения к вашему боту!
'''


from aiogram import Bot,Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio


api="7706788533:"
bot=Bot(token=api)
dp=Dispatcher(bot,storage=MemoryStorage())


class UserState(StatesGroup):
    growth=State()
    weight=State()
    age=State()

@dp.message_handler(text= "Calories")
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()               #ждем передачи сообщения от пользователя -> Состояние age

@dp.message_handler(state=UserState.age) #как только прило сообщение, происходит событие  UserState.age
async def set_growth(message,state):
    await state.update_data(age=message.text)   #записываем в дата с ключом age значение age

    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message,state):
    await state.update_data(growth=message.text)

    await message.answer('Введите свой вес')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()   # полуаем dat'у из записанных значений
    k_call=(10*float(data['weight'])+6.25*float(data['growth'])-5*float(data['age'])+5)*1.55
    await message.answer(f'Ваша норма каллорий: {k_call}')
    await state.finish()  #завершаем состояние



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)