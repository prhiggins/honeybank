import config
import uuid
import time

class DBManager():
	"""docstring for ."""

	balances = {
		"john": 5000,
		"susan": 10000,
		"dave": 60000
	}

	transactions = {
		uuid.uuid4(): Transaction(1000, "john", "susan", time.time() - 7200),
		uuid.uuid4(): Transaction(2000, "susan", "dave", time.time() - 3600),
		uuid.uuid4(): Transaction(1000, "dave", "john", time.time())
	}

	class Transaction():

		def __init__(self, amount, sender, recipient, timestamp):
			self.amount = amount
			self.sender = sender
			self.recipient = recipient
			self.timestamp = time.time()

		def serialise(self, id):
			return { "id": id, "amount": self.amount, "sender": self.sender, "recipient": self.recipient, "timestamp": self.timestamp }

		def __str__(self):
			return str(self.serialise())

	def __init__(self):
		self.balances = balances
		self.transactions = transactions

	def get_transaction(id):
		return transactions[id]

	def get_transactions_for_user(username):
		results = []
		for tx in self.transactions:
			if tx.sender = username or tx.recipient = username:
				results.append()
		return results.sort(key= lambda x: x.timestamp, reverse=True)

	def transfer(amount, destination_uid, current_user):
		tx = Transaction(amount, current_user, destination_uid, time.time())
		self.transactions.append(tx)
		return tx

class HoneyDBManager(DBManager):
	"""docstring for ."""

	honey_balances = {
		"dave": 75000,
		"alice": 1000,
		"winston": 6000
	}

	honey_transactions = {
		uuid.uuid4(): Transaction(1000, "alice", "winston", time.time() - 7200),
		uuid.uuid4(): Transaction(2000, "winston", "dave", time.time() - 3600),
		uuid.uuid4(): Transaction(1000, "dave", "alice", time.time())
	}

	def __init__(self):
		self.balances = honey_balances
		self.transactions = honey_transactions
