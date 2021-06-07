import config
import uuid
import time

class Transaction():

	def __init__(self, amount, sender, recipient, timestamp):
		self.amount = amount
		self.sender = sender
		self.recipient = recipient
		self.timestamp = time.time()

	def serialise(self):
		return {"amount": self.amount, "sender": self.sender, "recipient": self.recipient, "timestamp": self.timestamp }

	def __str__(self):
		return str(self.serialise())

	def get_timestamp(self):
		return self.timestamp

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

	def __init__(self):
		self.balances = DBManager.balances
		self.transactions = DBManager.transactions

	def get_transaction(self, id):
		return transactions[id]

	def get_transactions_for_user(self, username):
		results = []
		for tx in self.transactions.values():
			if tx.sender == username or tx.recipient == username:
				results.append(tx)
		
		return sorted(results, key= lambda x: x.timestamp, reverse=True)

	def transfer(self, amount, destination_uid, current_user):
		tx = Transaction(amount, current_user, destination_uid, time.time())
		self.transactions.append(tx)
		return tx

	def get_balance_for_user(self, username):
		return self.balances[username]

class HoneyDBManager(DBManager):
	"""docstring for ."""

	honey_balances = {
		"dave": 75000,
		"alice": 1000,
		"winston": 6000
	}

	honey_transactions = {
		uuid.uuid4(): Transaction(500, "alice", "winston", time.time() - 7200),
		uuid.uuid4(): Transaction(3000, "winston", "dave", time.time() - 3600),
		uuid.uuid4(): Transaction(1000, "dave", "alice", time.time())
	}

	def __init__(self):

		self.balances = HoneyDBManager.honey_balances
		self.transactions = HoneyDBManager.honey_transactions
