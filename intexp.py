class Expr:
	def is_constant(self):
		return False

	def contains_bool(self, bool_exp):
		return False

	def size(self):
		return 1

	def is_var(self):
		return False

	def type(self):
		return ""

	def depth(self):
		return 1

	def num_appearances(self, other_type):
		if self.type() == other_type:
			return 1
		return 0

	def largest_constant(self):
		return 0

	def fill_data(self, type_data):
		return

class Const(Expr):

	def __init__(self, val):
		self.val = val

	def execute(self, varmap):
		return self.val

	def exp_to_string(self):
		return str(self.val)

	def is_constant(self):
		return True

	def equals(self, other):
		if (other.is_constant()):
			return self.val == other.val
		return False

	def largest_constant(self):
		return self.val

	def fill_data(self, type_data):
		type_data[0] += 1
		type_data[1] += 1




class Variable(Expr):

	def __init__(self, name):
		self.name = name

	def execute(self, varmap):
		return varmap[self.name].execute(varmap)

	def is_var(self):
		return True

	def exp_to_string(self):
		return self.name

	def equals(self, other):
		if (other.is_var()):
			return other.name == self.name
		return False

	def type(self):
		return self.name


class BinExpr(Expr):

	def __init__(self, exp1, exp2):
		self.exp1 = exp1
		self.exp2 = exp2

	def contains_bool(self, bool_exp):
		return self.exp1.contains_bool(bool_exp) or self.exp2.contains_bool(bool_exp)

	def size(self):
		d1 = self.exp1.size()
		d2 = self.exp2.size()
		return 1 + d1 + d2

	def equals(self, other):
		if self.type() == other.type():
			if self.exp1.equals(other.exp1):
				return self.exp2.equals(other.exp2)
			elif self.exp2.equals(other.exp1):
				return self.exp1.equals(other.exp2)
		return False

	def depth(self):
		a = self.exp1.depth()
		b = self.exp2.depth()
		if a > b:
			return 1 + a
		return 1 + b

	def num_appearances(self, other_type):
		if self.type() == other_type:
			return 1 + self.exp1.num_appearances(other_type) + self.exp2.num_appearances(other_type)
		return self.exp1.num_appearances(other_type) + self.exp2.num_appearances(other_type)

	def largest_constant(self):
		a = self.exp1.largest_constant()
		b = self.exp2.largest_constant()
		if a > b:
			return a
		return b


class Add(BinExpr):

	def __init__(self, exp1, exp2):
		BinExpr.__init__(self, exp1, exp2)

	def execute(self, varmap):
		return self.exp1.execute(varmap) + self.exp2.execute(varmap)

	def exp_to_string(self):
		return "(" " + " + self.exp1.exp_to_string() + " " + self.exp2.exp_to_string() + ")"

	def type(self):
		return "add"

	def fill_data(self, type_data):
		type_data[2] += 1
		type_data[3] += self.depth()
		self.exp1.fill_data(type_data)
		self.exp2.fill_data(type_data)


class Subtract(BinExpr):

	def __init__(self, exp1, exp2):
		BinExpr.__init__(self, exp1, exp2)

	def execute(self, varmap):
		return self.exp1.execute(varmap) - self.exp2.execute(varmap)

	def exp_to_string(self):
		return "(" " - " + self.exp1.exp_to_string() + " " + self.exp2.exp_to_string() + ")"

	def type(self):
		return "subtract"

	def fill_data(self, type_data):
		type_data[4] += 1
		type_data[5] += self.depth()
		self.exp1.fill_data(type_data)
		self.exp2.fill_data(type_data)


class Multiply(BinExpr):

	def __init__(self, exp1, exp2):
		BinExpr.__init__(self, exp1, exp2)

	def execute(self, varmap):
		return self.exp1.execute(varmap) * self.exp2.execute(varmap)

	def exp_to_string(self):
		return "(" " * " + self.exp1.exp_to_string() + " " + self.exp2.exp_to_string() + ")"

	def type(self):
		return "multiply"

	def fill_data(self, type_data):
		type_data[6] += 1
		type_data[7] += self.depth()
		self.exp1.fill_data(type_data)
		self.exp2.fill_data(type_data)


class ITE(Expr):

	def __init__(self, exp, exp1, exp2):
		self.exp = exp
		self.exp1 = exp1
		self.exp2 = exp2

	def execute(self, varmap):
		if self.exp.execute(varmap):
			return self.exp1.execute(varmap)
		else:
			return self.exp2.execute(varmap)

	def exp_to_string(self):
		return "(" " ite " + self.exp.exp_to_string() + " " + self.exp1.exp_to_string() + " " + self.exp2.exp_to_string() + ")"

	def contains_bool(self, bool_exp):
		if self.exp.exp_to_string() == bool_exp.exp_to_string():
			return True
		'''
		if self.exp.type() != "not" and self.exp.type() != "equals" and bool_exp.type() != "not" and bool_exp.type() != "equals":
			# basically, don't allow redundant statements like x >= y and y >= x
			# when y = x would be sufficient
			if (self.exp.exp1.equals(bool_exp.exp1) and self.exp.exp2.equals(bool_exp.exp2)) or (self.exp.exp1.equals(bool_exp.exp2) and self.exp.exp2.equals(bool_exp.exp1)):
				return True
		'''
		return False

	def size(self):
		d1 = self.exp1.size()
		d2 = self.exp2.size()
		return 1 + d1 + d2

	def type(self):
		return "ite"

	def equals(self, other):
		if self.type() == other.type():
			if self.exp1.equals(other.exp1):
				return self.exp2.equals(other.exp2)
			elif self.exp2.equals(other.exp1):
				return self.exp1.equals(other.exp2)
		return False

	def depth(self):
		a = self.exp1.depth()
		b = self.exp2.depth()
		if a > b:
			return 1 + a
		return 1 + b

	def num_appearances(self, other_type):
		if self.type() == other_type:
			return 1 + self.exp1.num_appearances(other_type) + self.exp2.num_appearances(other_type)
		return self.exp.num_appearances(other_type) + self.exp1.num_appearances(other_type) + self.exp2.num_appearances(other_type)

	def largest_constant(self):
		a = self.exp1.largest_constant()
		b = self.exp2.largest_constant()
		if a > b:
			return a
		return b

	def fill_data(self, type_data):
		type_data[8] += 1
		type_data[9] += self.depth()
		self.exp1.fill_data(type_data)
		self.exp2.fill_data(type_data)


class And(BinExpr):
	def __init__(self, exp1, exp2):
		BinExpr.__init__(self, exp1, exp2)

	def execute(self, varmap):
		return self.exp2.execute(varmap) and self.exp1.execute(varmap)

	def exp_to_string(self):
		return "(" " and " + self.exp1.exp_to_string() + " " + self.exp2.exp_to_string() + ")"

	def type(self):
		return "and"

	def fill_data(self, type_data):
		type_data[10] += 1
		type_data[11] += self.depth()
		self.exp1.fill_data(type_data)
		self.exp2.fill_data(type_data)


class Or(BinExpr):
	def __init__(self, exp1, exp2):
		BinExpr.__init__(self, exp1, exp2)

	def execute(self, varmap):
		return self.exp2.execute(varmap) or self.exp1.execute(varmap)

	def exp_to_string(self):
		return "(" " or " + self.exp1.exp_to_string() + " " + self.exp2.exp_to_string() + ")"

	def type(self):
		return "or"

	def fill_data(self, type_data):
		type_data[12] += 1
		type_data[13] += self.depth()
		self.exp1.fill_data(type_data)
		self.exp2.fill_data(type_data)


class Not(Expr):
	def __init__(self, exp):
		self.exp = exp

	def execute(self, varmap):
		return not self.exp.execute(varmap)

	def exp_to_string(self):
		return "(" + "not " + self.exp.exp_to_string() + ")"

	def type(self):
		return "not"

	def fill_data(self, type_data):
		type_data[14] += 1
		type_data[15] += self.depth()
		self.exp.fill_data(type_data)


class GTE(BinExpr):
	def __init__(self, exp1, exp2):
		BinExpr.__init__(self, exp1, exp2)

	def execute(self, varmap):
		return self.exp1.execute(varmap) >= self.exp2.execute(varmap)

	def exp_to_string(self):
		return "(" " >= " + self.exp1.exp_to_string() + " " + self.exp2.exp_to_string() + ")"

	def type(self):
		return "gte"

	def fill_data(self, type_data):
		type_data[16] += 1
		type_data[17] += self.depth()
		self.exp1.fill_data(type_data)
		self.exp2.fill_data(type_data)


class LTE(BinExpr):
	def __init__(self, exp1, exp2):
		BinExpr.__init__(self, exp1, exp2)

	def execute(self, varmap):
		return self.exp1.execute(varmap) <= self.exp2.execute(varmap)

	def exp_to_string(self):
		return "(" " <= " + self.exp1.exp_to_string() + " " + self.exp2.exp_to_string() + ")"

	def type(self):
		return "lte"

	def fill_data(self, type_data):
		type_data[18] += 1
		type_data[19] += self.depth()
		self.exp1.fill_data(type_data)
		self.exp2.fill_data(type_data)


class GT(BinExpr):
	def __init__(self, exp1, exp2):
		BinExpr.__init__(self, exp1, exp2)

	def execute(self, varmap):
		return self.exp1.execute(varmap) > self.exp2.execute(varmap)

	def exp_to_string(self):
		return "(" " > " + self.exp1.exp_to_string() + " " + self.exp2.exp_to_string() + ")"

	def type(self):
		return "gt"


class LT(BinExpr):
	def __init__(self, exp1, exp2):
		BinExpr.__init__(self, exp1, exp2)

	def execute(self, varmap):
		return self.exp1.execute(varmap) < self.exp2.execute(varmap)

	def exp_to_string(self):
		return "(" " < " + self.exp1.exp_to_string() + " " + self.exp2.exp_to_string() + ")"

	def type(self):
		return "lt"

class Equals(BinExpr):
	def __init__(self, exp1, exp2):
		BinExpr.__init__(self, exp1, exp2)

	def execute(self, varmap):
		return self.exp1.execute(varmap) == self.exp2.execute(varmap)

	def exp_to_string(self):
		return "(" " = " + self.exp1.exp_to_string() + " " + self.exp2.exp_to_string() + ")"
		
	def type(self):
		return "equals"

	def fill_data(self, type_data):
		type_data[20] += 1
		type_data[21] += self.depth()
		self.exp1.fill_data(type_data)
		self.exp2.fill_data(type_data)


class Mod(BinExpr):
	def __init__(self, exp1, exp2):
		BinExpr.__init__(self, exp1, exp2)

	def execute(self, varmap):
		return self.exp1.execute(varmap) % self.exp2.execute(varmap)

	def exp_to_string(self):
		return "(" + self.exp1.exp_to_string() + " mod " + self.exp2.exp_to_string() + ")"

	def type(self):
		return "mod"
