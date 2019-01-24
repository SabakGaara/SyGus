import random
from intexp import Const

def z3ret_to_mymodel(fun_name, fun_model, z3_ret):
	z3_str = str(z3_ret)
	z3_str = z3_str[1: -1]
	splited = z3_str.split(",")
	dict_ret = {}
	dict_ret[fun_name] = fun_model
	for it in splited:
		name_val = it.split("=")
		name = name_val[0].replace(" ", "")
		val = int(name_val[1])
		dict_ret[name] = Const(val)
	return dict_ret

def z3_check(z3_checker, model, constraint_list, candidate_expression, var_name_list, candidate_name):
	varmap = {}
	varmap[candidate_name] = candidate_expression

	# print(candidate_expression.exp_to_string())

	str_for_z3 = "(define-fun " + candidate_name + " " + model.get_arg_string(var_name_list) + " " + model.get_ret_string() + " " + candidate_expression.exp_to_string() + ")"
	counter_example = z3_checker.check(str_for_z3)
	# counter_example = z3_checker.check('(define-fun max2 ((y Int)(x Int)) Int x )')
	if (counter_example == None):
		return None

	else:
		varmap = z3ret_to_mymodel(candidate_name, candidate_expression, counter_example)
		return varmap


def query(checker, model, constraint_list, candidate_expression, var_name_list, candidate_name):
	# 900 randomly generated points against the proposed solution and constraints
	varmap = {}
	varmap[candidate_name] = candidate_expression
	# print(varmap['f'].exp_to_string())
	# print(var_name_list)

	for i in range(5):
		for j in range(5):
			for var_name in var_name_list:
				# create a random assignment of variables
				varmap[var_name] = Const(random.randint(-i, i))
			if not check(constraint_list, varmap):
				# return the point that broke it
				return varmap
	# z3ret = z3_check(checker, model, constraint_list, candidate_expression, var_name_list, candidate_name)
	return None



def check(constraint_list, varmap):
	for constraint in constraint_list:
		if not constraint.execute(varmap):
			return False
	return True
