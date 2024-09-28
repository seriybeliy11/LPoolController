import asyncio
from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.types import Integer, String, Float, Boolean, DateTime
from stonfi import APIClient
from stonfi.types import Operation

Base = declarative_base()

class OperationModel(Base):
    __tablename__ = 'operations'

    def __init__(self, operation):
        for attr_name in dir(operation):
            if not callable(getattr(operation, attr_name)) and not attr_name.startswith("__"):
                attr_value = getattr(operation, attr_name)
                setattr(self, attr_name, attr_value)

def map_type(attr_value):
    if isinstance(attr_value, int):
        return Integer
    elif isinstance(attr_value, str):
        return String
    elif isinstance(attr_value, float):
        return Float
    elif isinstance(attr_value, bool):
        return Boolean
    elif isinstance(attr_value, datetime.datetime):
        return DateTime
    else:
        return String

async def get_wallet_operations(wallet_addr: str, since: str, until: str, op_type: str | None = None) -> list[Operation]:
    client = APIClient()
    url = f"{client.base_url}/v1/wallets/{wallet_addr}/operations"
    params = {
        "since": since,
        "until": until,
        "op_type": op_type
    }
    response = await client.get(url, params=clean_dict(params))
    return [Operation.from_dict(operation) for operation in response.json()["operations"]]

async def save_wallet_operations_to_db(wallet_addr: str, since: str, until: str, op_type: str | None = None):
    operations = await get_wallet_operations(wallet_addr, since, until, op_type)

    engine = create_engine('sqlite:///operations.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    for operation in operations:
        for attr_name in dir(operation):
            if not callable(getattr(operation, attr_name)) and not attr_name.startswith("__"):
                attr_value = getattr(operation, attr_name)
                column = Column(attr_name, map_type(attr_value))
                if not hasattr(OperationModel, attr_name):
                    setattr(OperationModel, attr_name, column)

        operation_model = OperationModel(operation)
        session.add(operation_model)

    session.commit()
    session.close()

asyncio.run(save_wallet_operations_to_db('your_wallet_address', 'start_date', 'end_date', 'operation_type'))
