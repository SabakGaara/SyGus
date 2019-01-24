from intexp import *
from model import *
from oracle import *
from sample_models import *
from solver import *

def convert_constraints(constraint_list):
	# encodes specified constraints to an integer array to be used as input for the
	# neural network
	data = []
	data.append(len(constraint_list))
	avg_size = 0
	avg_depth = 0
	for d in constraint_list:
		avg_size += ((1.0) * d.size()) / len(constraint_list)
		avg_depth += ((1.0) * d.depth()) / len(constraint_list)
	data.append(avg_size)
	data.append(avg_depth)
	numx = 0
	numy = 0
	numz = 0
	numf = 0
	for d in constraint_list:
		numx += d.num_appearances("x")
		numy += d.num_appearances("y")
		numz += d.num_appearances("z")
		numf += d.num_appearances("f")
	data.append(numx)
	data.append(numy)
	data.append(numz)
	data.append(numf)

	maxc = 0
	for d in constraint_list:
		if d.largest_constant() > maxc:
			maxc = d.largest_constant()

	data.append(maxc)
	type_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

	for d in constraint_list:
		d.fill_data(type_data)
	for i in range(11):
		if type_data[2 * i] != 0:
			type_data[2 * i + 1] = (1.0 * type_data[2 * i + 1]) / type_data[2 * i]

	data.extend(type_data)
	return data



'''
def convert_solution(exp):
	# maps a program to its attribute vector
	data = []
	data.append(exp.size())
	data.append(exp.depth())
	data.append(exp.num_appearances("x"))
	data.append(exp.num_appearances("y"))
	data.append(exp.num_appearances("z"))
	data.append(exp.largest_constant())
	type_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	exp.fill_data(type_data)
	for i in range(11):
		if type_data[2 * i] != 0:
			type_data[2 * i + 1] = (1.0 * type_data[2 * i + 1]) / type_data[2 * i]
	for i in range(len(type_data)):
		if i < 10 or i > 15:
			data.append(type_data[i])
	return data
'''
def convert_solution(exp):
	# maps a program to its attribute vector
	data = []
	data.append(exp.num_appearances("x"))
	data.append(exp.num_appearances("y"))
	data.append(exp.num_appearances("z"))
	type_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	exp.fill_data(type_data)
	for i in range(len(type_data)):
		if i < 10 or i > 15:
			if i % 2 == 0:
				data.append(type_data[i])
	s = max(data)
	for i in range(len(data)):
		data[i] = (1.0 * data[i]) / s
	return data
def set_up_problem():
	inputs = []
	outputs = []
	for s in sample_models:
		program = programs[sample_models.index(s)]
		print("PROGRAM:")
		print(program.exp_to_string())
		print("SATISFIES CONSTRAINTS:")
		for c in s.get_constraints():
			print(c.exp_to_string())
		print("")
		inputs.append(convert_constraints(s.get_constraints()))
		outputs.append(convert_solution(program))
	return (inputs, outputs)

def set_up_test_case():
	inputs = []
	outputs = []
	inputs.append(convert_constraints(sample_model11.get_constraints()))
	outputs.append(convert_solution(test_program))
	return (inputs, outputs)







