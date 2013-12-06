

import datetime


class Age:

	"""
	Basic age class for dealing with kids' ages in years and months.
	Should implement some functionality..
	"""

	def __init__(self, years, months):

		self.years=int(years)
		self.months=int(months)

	def __repr__(self):
		return "{0} years and {1} months old".format(self.years, self.months)

	def as_months(self):
		return 12*self.years+self.months

	def as_float(self):
		return float(self.as_months())

	def as_number(self):
		return self.as_months()

	#TODO:
	#stuff using datetime class
	def is_older(self):
		pass

