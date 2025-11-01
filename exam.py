from aiogram import types, Router, F,  Bot
import psycopg2
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio



conn = psycopg2.connect(
    host="localhost",
    database="last_exam",
    port=25312,
    user="postgres",
    password="1234"
)
cursor = conn.cursor()


r = Router()

key1 = KeyboardButton(text = '/add_product')
key2 = KeyboardButton(text = '/show_all')
keys = ReplyKeyboardMarkup(
    keyboard=[[key1, key2]],
    resize_keyboard=True
    )



class Insert(StatesGroup):
    name = State()
    price = State()
    desc = State()
    quantity = State()
    image = State()





class Prod(StatesGroup):
    name = State()
    price = State()
    desc = State()
    quantity = State()
    image = State()



class Product:
    def create():
        cursor.execute('''
create table if not exists Products(
id serial primary key,
name varchar(50) not null,
description text not null,
price int not null,
quantity int not null,
imade_id text not null,
created_at date default current_date
)''')
        conn.commit()
    
    
    @staticmethod
    def insert(name, description, price, quantity, image_id):
        try:
            cursor.execute('insert into products(name, description, price, quantity, image_id) values(%s, %s, %s, %s, %s)',(name, description, price, quantity, image_id) )
            conn.commit()
            return "New product added."
        except:
            return "Error"
        
    @staticmethod
    def show():
        cursor.execute('select * from products')
        all = cursor.fetchall()
        return all



class Work:
    @r.message(Command('start'))
    async def start(message:types.Message):
        await message.answer("Choose buttons", reply_markup=keys)

    @r.message(Command('add_product'))
    async def add(message:types.Message, state:FSMContext):
        await message.answer('Enter product name')
        await state.set_state(Insert.name)
    
    @r.message(Insert.name)
    async def get_name(message:types.Message, state:FSMContext):
        await state.update_data(name = message.text)
        await message.answer('Enter price')
        await state.set_state(Insert.price)
        
    
    @r.message(Insert.price)
    async def get_name(message:types.Message, state:FSMContext):
        await state.update_data(price = message.text)
        await message.answer('Enter description')
        await state.set_state(Insert.desc)
    
    @r.message(Insert.desc)
    async def get_name(message:types.Message, state:FSMContext):
        await state.update_data(desc = message.text)
        await message.answer('Enter quantity')
        await state.set_state(Insert.quantity)
    
    
    @r.message(Insert.quantity)
    async def get_name(message:types.Message, state:FSMContext):
        await state.update_data(quantity = message.text)
        await message.answer('Send the photo of your product')
        await state.set_state(Insert.image)
    
    
    @r.message(Insert.image)
    async def get_name(message:types.Message, state:FSMContext):
        file_id = message.photo[-1].file_id
        print(file_id)
        await state.update_data(image = file_id)
        data = await state.get_data()
        await message.answer(Product.insert(data['name'], data['desc'], data['price'], data['quantity'], data['image'] ), reply_markup=keys)
        await state.clear()
        
    @r.message(Command('show_all'))
    async def add(message:types.Message):
        al=Product.show()
        for i in al:
            but1 = InlineKeyboardButton(text = 'delete', callback_data=f'delete_{i[0]}')
            but2 = InlineKeyboardButton(text = 'update', callback_data=f'update_{i[0]}')
            buts= InlineKeyboardMarkup(
                inline_keyboard=[[but1, but2]]
            )

            await message.answer_photo(i[5],caption = f'''
Id:  {i[0]}
Name: {i[1]} 
Price: {i[3]}
Description: {i[2]}
Quantity: {i[4]}
Created_at : {i[6]}
''', reply_markup=buts)
            
    @r.callback_query(F.data.startswith('delete_'))
    async def delete(callback:types.CallbackQuery):
        pro_id = callback.data.split("_")[1]
        try:
            cursor.execute('delete from products where id=%s', (pro_id, ))
            conn.commit()
            await callback.answer(f'Product with id:{pro_id} deleted')
        except:
            await callback.answer("Error")
        
        
    @r.callback_query(F.data.startswith('update_'))
    async def update(callback:types.CallbackQuery, state:FSMContext):
        pro_id = callback.data.split("_")[1]
        await state.update_data(p_id =pro_id )
        await callback.message.answer(f'''Update product with id:{pro_id} Enter name for new product''')
        await state.set_state(Prod.name)
        await callback.answer()
    
    
    @r.message(Prod.name)
    async def uget_name(message:types.Message, state:FSMContext):
        await state.update_data(name = message.text)
        await message.answer('Enter price')
        await state.set_state(Prod.price)
        
    
    @r.message(Prod.price)
    async def uget_name(message:types.Message, state:FSMContext):
        await state.update_data(price = message.text)
        await message.answer('Enter description')
        await state.set_state(Prod.desc)
    
    @r.message(Prod.desc)
    async def uget_name(message:types.Message, state:FSMContext):
        await state.update_data(desc = message.text)
        await message.answer('Enter quantity')
        await state.set_state(Prod.quantity)
    
    
    @r.message(Prod.quantity)
    async def uget_name(message:types.Message, state:FSMContext):
        await state.update_data(quantity = message.text)
        await message.answer('Send the photo of your product')
        await state.set_state(Prod.image)
    
    
    @r.message(Prod.image)
    async def uget_name(message:types.Message, state:FSMContext):
        file_id = message.photo[-1].file_id
        await state.update_data(image = file_id)
        data = await state.get_data()
        try:
            cursor.execute('''update products set name = %s, description=%s, price=%s, quantity=%s, image_id=%s   where id=%s''', (data['name'], data['desc'], data['price'], data['quantity'], data['image'], data['p_id']))
            conn.commit()
            await message.answer('Product updated', reply_markup=keys)
        except:
            await message.answer("Error")
