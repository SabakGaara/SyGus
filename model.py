class my_model:

	def __init__(self, constraint_list, const, int_var_name_list, function_name, op_start, bool_op, bool_start, dict_var, ret_type):
		self.constraint_list = constraint_list
		self.int_var_name_list = int_var_name_list
		self.function_name = function_name
		self.op_start = op_start
		self.bool_op = bool_op
		self.bool_start = bool_start
		self.const = const
		self.dict_var = dict_var
		self.ret_type = ret_type

	def get_var_names(self):
		return self.int_var_name_list

	def get_constraints(self):
		return self.constraint_list
	def get_function(self):
		return self.function_name
	def get_op_start(self):
		return self.op_start
	def get_bool_op(self):
		return self.bool_op
	def get_bool_start(self):
		return self.bool_start
	def get_const(self):
		return self.const

	def get_arg_string(self, var_name_list):
		str = "("
		for k in var_name_list:
			str += "(" + k + " " + self.dict_var[k] + ")"
		str += ") "
		return str

	def get_ret_string(self):
		return self.ret_type
