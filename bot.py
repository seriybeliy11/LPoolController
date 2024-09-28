from pyrogram import Client, filters
from pyromod import listen
from stonfi import APIClient
import asyncio
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from os import path
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


from stonfi.types import Pool


from config import *

stonfi_client = APIClient()
app = Client(name='nikitos',api_hash=api_hash, api_id=api_id, bot_token=bot_token)

engine = create_engine('sqlite:///pools.db')
Session = sessionmaker(bind=engine)

Base = declarative_base()

class Pool(Base):
    __tablename__ = 'pools'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    token_lqd = Column(String)
    token_base = Column(String)
        
    
class Watchlist(Base):
    __tablename__ = 'watchlists'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    name_pool = Column(String)

    pool = relationship("Pool")


    
class Pager:
    def __init__(self, total_items, page_size):
        self.total_items = total_items
        self.page_size = page_size
        self.current_page = 0

    @property
    def start_index(self):
        return self.current_page * self.page_size

    @property
    def end_index(self):
        return self.start_index + self.page_size

    def next_page(self):
        self.current_page = max(0, self.current_page +1)

    def prev_page(self):
        self.current_page = max(0, self.current_page - 1)


if not path.exists('pools.db'):
    Base.metadata.create_all(engine)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Welcome to the pool tracker bot!")
    
    
@app.on_message(filters.command("about"))
async def about(client, message):
    await message.reply("Pools Alerter by Equel==Team (Stonfi Location)")
    
    
@app.on_message(filters.command("get_quantity_pools"))
async def quantity(client, message):
    engine = create_engine('sqlite:///pools.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(func.count(Pool.id)).scalar()
    session.close()
    await message.reply(f"Количество пулов в базе данных: {result}")



@app.on_message(filters.command("get_info_by_pool"))
async def get_info_by_pool(client, message):
    s_client = APIClient()
    response = await client.ask(message.chat.id, 'Введите адрес пула')
    pool_addr = response.text

    pool = await s_client.get_pool(pool_addr)

    name_asset = pool.token0_address
    main_asset = pool.token1_address

    asset_from_pool = await s_client.get_asset(name_asset)
    main_asset_from_pool = await s_client.get_asset(main_asset)

    info_pool = await client.send_message(
    message.chat.id,
    f'**POOL {pool.address}**\n'
    f'Amount of the first token (in basic token units): **{pool.reserve0}** coins\n'
    f'Amount of the second token (in basic token units): **{pool.reserve1}** coins\n'
    f'Token: **{asset_from_pool.display_name}**\n'
    f'Base Unit: **{main_asset_from_pool.display_name}**\n'
    f'LP Fee: **{pool.lp_fee}**\n'
    f'Protocol Fee: **{pool.protocol_fee}**\n'
    f'Ref Fee: **{pool.ref_fee}**\n'
    f'Sub-contract for fees: **{main_asset_from_pool.display_name}**\n'
    f'Collected Token 0 Protocol Fee: **{pool.collected_token0_protocol_fee}**\n'
    f'Collected Token 1 Protocol Fee: **{pool.collected_token1_protocol_fee}**\n'
    f'Estimated Price: **{int(pool.reserve1) / int(pool.reserve0)}$ at {datetime.datetime.now()}**\n'
    f'TVL: **{pool.reserve0 * asset_from_pool.price + pool.reserve1 * main_asset_from_pool.price}$**\n'
    f'Total Fees Earned: **{pool.collected_token0_protocol_fee + pool.collected_token1_protocol_fee}**\n'
    f'Percentage of TVL: {(pool_liquidity / dex_liquidity) * 100}\n'
    f'CPMM: {(actual_price - expected_price) / expected_price * 100}\n'
    f'LPs Holding: {2 * sqrt(pool.reserve0 * pool.reserve1) - pool.reserve0 - pool.reserve1}'
    
    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Add to Watchlist", callback_data=f"add_watchlist_{pool.address}")]])
    )
    
    
@app.on_callback_query(filters.regex("^add_watchlist_"))
async def add_to_watchlist(client, callback_query):
    user_id = callback_query.from_user.id
    pool_address = callback_query.data.split("_")[2]

    session = Session()
    pool = session.query(Pool).filter_by(address=pool_address).first()
    watchlist_entry = Watchlist(user_id=user_id, name_pool=pool_address)
    session.add(watchlist_entry)
    session.commit()
    session.close()

    await callback_query.answer("Pool added to watchlist.")


@app.on_message(filters.command("top10_pools"))
async def top10_TVL_pools(client, message):
    s_client = APIClient()
    
    pools = await s_client.get_pool()
    
    top10_pools = []
    
    for pool in pools:
        if 
    
    


@app.on_message(filters.command("show_watchlist"))
async def show_watchlist(client, message):
    user_id = message.from_user.id

    session = Session()
    watchlist_entries = session.query(Watchlist).filter_by(user_id=user_id).all()
    session.close()

    if not watchlist_entries:
        await message.reply("Your watchlist is empty.")
        return

    keyboard = []
    for entry in watchlist_entries:
        pool = entry.pool
        keyboard.append([InlineKeyboardButton(pool.name, callback_data=f"get_info_{pool.address}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply("Here's your watchlist:", reply_markup=reply_markup)

 

    

app.run()
