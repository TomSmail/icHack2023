from types import coroutine
import click
import asyncpg
import toml
import asyncio


with open('config.toml', 'r') as f:
    parsed_toml = toml.loads(f.read())


async def connect():
    return await asyncpg.connect(parsed_toml["DB_CONN"])


async def initialize():
    conn = await connect()
    with open('sql/schema.sql', 'r') as f:
        await conn.execute(f.read())


async def clear():
    conn = await connect()
    with open('sql/drop.sql', 'r') as f:
        await conn.execute(f.read())


async def seed():
    conn = await connect()
    with open('sql/seed.sql', 'r') as f:
        await conn.execute(f.read())


@click.group()
def cli():
    pass


@cli.command()
def reset():
    asyncio.run(clear())
    asyncio.run(initialize())

    click.echo('Initialized the database')


@cli.command()
def seed():
    asyncio.run(seed())
    click.echo('seed ')


if __name__ == '__main__':
    cli()
