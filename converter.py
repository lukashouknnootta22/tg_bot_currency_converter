import freecurrencyapi

class ClientCurrency:

	def __init__(self, api_key: str):
		self.client = freecurrencyapi.Client(api_key)

	def get_values(self, list_currency="") -> str:
		cur = self.client.currencies(currencies=["EUR", "USD", "RUB"])
		for code, values in cur["data"].items():
			list_currency += (f"{code} {values['name']} {values['symbol_native']}\n ")
		return list_currency

	def get_exchange_currency_rates(self, base: str, cur: str) -> int:
		cur_list = cur.split(',')
		result = self.client.latest(base, cur_list)["data"]
		return result[cur]