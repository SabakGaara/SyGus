from intexp import *
from model import *
from oracle import *

def synthesize(checker, model, add_flag = False, const_flag = False):
    constraint_list = model.get_constraints()
    var_name_list = model.get_var_names()
    function_name = model.get_function()
    list_start_op = model.get_op_start()
    list_bool_op = model.get_bool_op()
    list_bool_start = model.get_bool_start()
    list_const = model.get_const()

    
    points_to_check = []

    # list of results encountered for the expression, encoded into a bit vector
    # used to determine whether or not something goes in used_expressions
    signatures_to_check = {}

    expressions = [] # queue of expressions to check the constraints against

    used_expressions = {} # solely for the purposes of forming new expressions

    # size of the expressions to form
    target_size = 3

    for i in range(1, 1000):
        used_expressions[i] = []


    bool_expressions_to_use = [] # queue of boolean expressions to use for ITE

    # initialize the first terms
    for var in var_name_list:
        expressions.append(Variable(var))
    
    for const in  list_const:
        expressions.append(Const(const))
    


    # initialize the first booleans out of the constants and variables
    for i in range(len(expressions) - 1):
        for j in range(i + 1, len(expressions)):
            if not (expressions[i].is_constant() and expressions[j].is_constant()):
                if ">=" in list_bool_start:
                    bool_expressions_to_use.append(GTE(expressions[i], expressions[j]))
                if "<=" in list_bool_start:
                    bool_expressions_to_use.append(LTE(expressions[i], expressions[j]))
                if "=" in list_bool_start:
                    bool_expressions_to_use.append(Equals(expressions[i], expressions[j]))
                if "<" in list_bool_start:
                    bool_expressions_to_use.append(LT(expressions[i], expressions[j]))
                if ">" in list_bool_start:
                    bool_expressions_to_use.append(GT(expressions[i], expressions[j]))

    # for i in range(len(bool_expressions_to_use)):
    #     for j in range(i+1, len(bool_expressions_to_use)):
    #         if not (bool_expressions_to_use[i].is_constant() and bool_expressions_to_use[j].is_constant()):
    #             if "and" in list_bool_op:
    #                 bool_expressions_to_use.append(And(bool_expressions_to_use[i], bool_expressions_to_use[j]))
    #             if "or" in list_bool_op:
    #                 bool_expressions_to_use.append(Or(bool_expressions_to_use[i], bool_expressions_to_use[j]))
    #     if "not" in list_bool_op:
    #         bool_expressions_to_use.append(Not(bool_expressions_to_use[i]))

    i = 0
    cc1 = 0
    cc2 = 0
    left_bound = 1
    num_stored = 0
    num_enumerated = 0
    num_const = 2
    target_size = 3
    # how big we want our boolean to be
    bool_target_size = 3
    while (1):
        i += 1
        if (len(expressions) == 0):
            #make more candidate expressions
            iters = 0
            for index_left in range(left_bound, int((target_size + 1) / 2), 2):
                if (iters > 10000):
                    left_bound = index_left
                    break
                index_right = target_size - index_left - 1
                for exp1 in used_expressions[index_left]:
                    for exp2 in used_expressions[index_right]:
                        iters += 1
                        if (add_flag and not (exp1.is_constant() or exp2.is_constant())):
                            if "+" in list_start_op:
                                expressions.append(Add(exp1, exp2))
                            if "-" in list_start_op:
                                expressions.append(Subtract(exp1, exp2))
                                expressions.append(Subtract(exp2, exp1))
                            if "*" in list_start_op:
                                expressions.append(Multiply(exp1, exp2))
                            if "mod" in list_start_op:
                                expressions.append(Mod(exp1, exp2))
                        
                        for bool_exp in bool_expressions_to_use:
                            if not (exp1.contains_bool(bool_exp) or exp2.contains_bool(bool_exp)):
                                if not (exp1.equals(exp2)):
                                    if "ite" in list_start_op:
                                        # print(exp1, exp2)
                                        # print("-----------------------------------------------------------------------")
                                        expressions.append(ITE(bool_exp, exp1, exp2))
                                        expressions.append(ITE(bool_exp, exp2, exp1))

            num_enumerated += len(expressions)

            if (iters <= 10000 and len(expressions) != 0):
                target_size += 2
                left_bound = 1


        if (len(expressions) == 0):
            # add another layer of boolean expressions
            iters = 0

            for exp1 in used_expressions[bool_target_size]:
                for exp2 in used_expressions[bool_target_size]:
                    if (exp1.is_constant() and exp2.is_constant()):
                        continue
                    if iters > 20:
                        break
                    iters += 1
                    # print(i, j)
                    if not exp1.type() == "ite":
                        if ">=" in list_bool_start:
                            bool_expressions_to_use.append(GTE(exp1, exp2))
                        if "<=" in list_bool_start:
                            bool_expressions_to_use.append(LTE(exp1, exp2))
                        if "=" in list_bool_start:
                            bool_expressions_to_use.append(Equals(exp1, exp2))
                        if "<" in list_bool_start:
                            bool_expressions_to_use.append(LT(exp1, exp2))
                        if ">" in list_bool_start:
                            bool_expressions_to_use.append(GT(exp1, exp2))
                if iters > 20:
                    break
            if iters <= 20:
                bool_target_size = target_size - 2
            iters = 0
            continue

        # if (i % 1000 == 0):
        #     print(i)


        exp = expressions.pop(0)
        # for exp in expressions:
        #     print(exp.exp_to_string())
        # print(exp.exp_to_string())
    
        flag = True
        new_signature = []
        for k in range(len(points_to_check)):
            points_to_check[k][function_name] = exp
            if not check(constraint_list, points_to_check[k]):
                flag = False
            new_signature.append(exp.execute(points_to_check[k]))
        if flag:

            ''''''''' Just shows how much was stored '''''''''
            stored_size = 0
            for k in range(1, 15):
                stored_size += len(used_expressions[k])
            # print("NUM STORED: " + str(stored_size))
            ''''''''''''''''''''''''''''''''''''''''''''
            # for con in constraint_list:
            #     print(con.exp_to_string())
            # new_point = z3_check(checker, model, constraint_list, exp, var_name_list, function_name)
            # print(exp.exp_to_string())
            new_point = query(checker, model, constraint_list, exp, var_name_list, function_name)

            if new_point == None:
                str_for_z3 = "(define-fun " + function_name + " " + model.get_arg_string(
                    var_name_list) + " " + model.get_ret_string() + " " + exp.exp_to_string() + ")"
                tmp = checker.check(str_for_z3)
                if (tmp != None): continue
                # print(num_const)
                # print("INPUT")
                # for c in constraint_list:
                #     print(c.exp_to_string())
                # print("OUTPUT")
                print(str_for_z3)
                return
            else:
                # print(new_point)

                points_to_check.append(new_point)

                for k in range(1, 1000):
                    used_expressions[k] = []

                expressions = []
                signatures_to_check = {}
                left_bound = 1
                target_size = 3
                for var in var_name_list:
                    expressions.append(Variable(var))
                for const in list_const:
                    expressions.append(Const(const))

                num_const += 1


        else:
            cc1 += 1
            if new_signature not in signatures_to_check.values():
                num_stored += 1
                used_expressions[exp.size()].append(exp)
                signatures_to_check[exp] = new_signature
            
    
    print("Did not find anything!")
    return None
