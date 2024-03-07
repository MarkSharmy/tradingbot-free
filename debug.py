import asyncio
import deriv_bot

deriv_bot.initialize("demo")
asyncio.run(deriv_bot.place_entry(contract_type = "CALLE", symbol = "R_100"))