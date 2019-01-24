import sys
import os
import sexp
import pprint
import translator
from intexp import *
from model import *
from oracle import *
from solver import *
list_con_constraint = []


def dfs_con(exp, fun_name):
    if type(exp) == list and len(exp) == 3 and len(exp) != 0:
        opcode = exp[0]
        if type(exp[1]) == list:
            var1 = dfs_con(exp[1], fun_name)
        else:
            if exp[1].isdigit():
                var1 = Const(exp[1])
            else:
                var1 = Variable(exp[1])

        if len(exp) == 3 and type(exp[2]) == list:
            var2 = dfs_con(exp[2], fun_name)

        elif len(exp) == 3:
            if type(exp[2]) == tuple:
                var2 = Const(exp[2][1])
            else:
                var2 = Variable(exp[2])
        if opcode == "<=":
            return LTE(var1, var2)
        elif opcode == ">=":
            return GTE(var1, var2)
        elif opcode == "+":
            return Add(var1, var2)
        elif opcode == "-":
            return Subtract(var1, var2)
        elif opcode == "or":
            return Or(var1, var2)
        elif opcode == "*":
            return Multiply(var1, var2)
        elif opcode == "mod":
            return Mod(var1, var2)
        elif opcode == "not":
            return Not(var1)
        elif opcode == "and":
            return And(var1, var2)
        elif opcode == "=":
            return Equals(var1, var2)
        elif opcode == ">":
            return GT(var1, var2)
        elif opcode == "<":
            return LT(var1, var2)
        elif opcode == "=>":
            return ITE(var1, var2, Const(True))
        elif opcode == fun_name:
            return Variable(fun_name)
    elif len(exp) >= 3:

        if exp[0] == fun_name:
            return Variable(fun_name)



def Extend(Stmts,Productions):
    ret = []
    for i in range(len(Stmts)):
        if type(Stmts[i]) == list:
            TryExtend = Extend(Stmts[i],Productions)
            if len(TryExtend) > 0 :
                for extended in TryExtend:
                    ret.append(Stmts[0:i]+[extended]+Stmts[i+1:])
        elif Productions.has_key(Stmts[i]):
            for extended in Productions[Stmts[i]]:
                ret.append(Stmts[0:i]+[extended]+Stmts[i+1:])
    return ret

def stripComments(bmFile):
    noComments = '('
    for line in bmFile:
        line = line.split(';', 1)[0]
        noComments += line
    return noComments + ')'


if __name__ == '__main__':
    benchmarkFile = open(os.path.abspath('.') + "/libing/tests/open_tests/" + sys.argv[1])
    bm = stripComments(benchmarkFile)
    bmExpr = sexp.sexp.parseString(bm, parseAll=True).asList()[0] #Parse string to python list
    # print(bmExpr) [['set-logic', 'LIA'], ['synth-fun', 'max2', [['x', 'Int'], ['y', 'Int']], 'Int', [['Start', 'Int', ['x', 'y', ('Int', 0), ('Int', 1), ['+', 'Start', 'Start'], ['-', 'Start', 'Start'], ['ite', 'StartBool', 'Start', 'Start']]], ['StartBool', 'Bool', [['and', 'StartBool', 'StartBool'], ['or', 'StartBool', 'StartBool'], ['not', 'StartBool'], ['<=', 'Start', 'Start'], ['=', 'Start', 'Start'], ['>=', 'Start', 'Start']]]]], ['declare-var', 'x', 'Int'], ['declare-var', 'y', 'Int'], ['constraint', ['>=', ['max2', 'x', 'y'], 'x']], ['constraint', '>=', ['max2', 'x', 'y'], 'y'], ['constraint', ['or', ['=', 'x', ['max2', 'x', 'y']], ['=', 'y', ['max2', 'x', 'y']]]], ['check-synth']]
    checker=translator.ReadQuery(bmExpr)
    #print (checker.check('(define-fun f ((x Int)(y Int)) Int(ite (= x y) 0 ( ite ( >= x y) 1 -1)))'))
    #raw_input()
    SynFunExpr = []
    list_var = []
    list_s_var = []
    list_start_op = []
    list_bool_op = []
    list_bool_start = []
    list_const = []
    list_constraint = []
    list_define_fun = []
    list_declare_var = []
    list_fun_map = []
    list_con_constraint = []
    dict_var = {}
    list_fun = ""
    ret_type = ""

    StartSym = 'My-Start-Symbol' #virtual starting symbol
    for expr in bmExpr:
        # print(expr)
        if len(expr)==0:
            continue
        elif expr[0]=='synth-fun':
            SynFunExpr=expr
            list_fun = expr[1]
            # print SynFunExpr[2]
            ret_type = expr[3]
            for var in SynFunExpr[2]:
                list_var.append(var[0])
                dict_var[var[0]] = var[1]
            # print(SynFunExpr[4])
            for op in SynFunExpr[4][0][2]:
                if type(op) == str:
                    list_s_var.append(op)
                elif type(op) == tuple:
                    list_const.append(op[1])
                elif type(op) == list:
                    list_start_op.append(op[0])
            if len(SynFunExpr[4]) == 2:
                for bool_op in SynFunExpr[4][1][2]:
                    if type(bool_op) == list and bool_op[1] == "StartBool":
                        list_bool_op.append(bool_op[0])
                    elif bool_op[1] == "Start":
                        list_bool_start.append(bool_op[0])
        elif expr[0]=='declare-var':
            list_declare_var.append(expr[1])
            if (not dict_var.has_key(expr[1])):
                dict_var[expr[1]] = expr[2]

        elif expr[0]=='constraint':
            if len(expr) > 2:
                con_expr = expr[1:]
            else:
                con_expr = expr[1]
            con_constraint = dfs_con(con_expr, SynFunExpr[1])
            list_con_constraint.append(con_constraint)

        elif expr[0]=='define-fun':
            list_fun_map.append(expr)
    FuncDefine = ['define-fun']+SynFunExpr[1:4] #copy function signature
    #print(FuncDefine)

    # print(list_declare_var)
    #sample_model10 = Model([ITE(Equals(x, y), Equals(f, Const(4)), Equals(f, Const(3)))], ["x", "y", "z"], "f")
    checker_model = my_model(list_con_constraint, list_const, list_declare_var, list_fun, list_start_op, list_bool_op, list_bool_start, dict_var, ret_type)
    synthesize(checker, checker_model, True)
    # BfsQueue = [[StartSym]] #Top-down
    # Productions = {StartSym:[]}
    # Type = {StartSym:SynFunExpr[3]} # set starting symbol's return type
    #
    # for NonTerm in SynFunExpr[4]: #SynFunExpr[4] is the production rules
    #     NTName = NonTerm[0]
    #     NTType = NonTerm[1]
    #     if NTType == Type[StartSym]:
    #         Productions[StartSym].append(NTName)
    #     Type[NTName] = NTType
    #     #Productions[NTName] = NonTerm[2]
    #     Productions[NTName] = []
    #     for NT in NonTerm[2]:
    #         if type(NT) == tuple:
    #             Productions[NTName].append(str(NT[1])) # deal with ('Int',0). You can also utilize type information, but you will suffer from these tuples.
    #         else:
    #             Productions[NTName].append(NT)
    # Count = 0
    # TE_set = set()
    # while(len(BfsQueue)!=0):
    #     Curr = BfsQueue.pop(0)
    #     #print("Extending "+str(Curr))
    #     TryExtend = Extend(Curr,Productions)
    #     if(len(TryExtend)==0): # Nothing to extend
    #         FuncDefineStr = translator.toString(FuncDefine,ForceBracket = True) # use Force Bracket = True on function definition. MAGIC CODE. DO NOT MODIFY THE ARGUMENT ForceBracket = True.
    #         CurrStr = translator.toString(Curr)
    #         #SynFunResult = FuncDefine+Curr
    #         #Str = translator.toString(SynFunResult)
    #         Str = FuncDefineStr[:-1]+' '+ CurrStr+FuncDefineStr[-1] # insert Program just before the last bracket ')'
    #         Count += 1
    #         # print (Str)
    #         # if Count % 100 == 1:
    #             # print (Count)
    #             # print (Str)
    #             #raw_input()
    #         #print '1'
    #         # print Str (define-fun max2 ((x Int) (y Int)) Int (+ (- 1 0) 1))
    #
    #         counterexample = checker.check(Str)
    #         #print counterexample
    #         if(counterexample == None): # No counter-example
    #             Ans = Str
    #             break
    #         #print '2'
    #     #print(TryExtend)
    #     #raw_input()
    #     #BfsQueue+=TryExtend
    #     # x+s / s+x
    #     for TE in TryExtend:
    #         TE_str = str(TE)
    #         if not TE_str in TE_set:
    #             BfsQueue.append(TE)
    #             TE_set.add(TE_str)

    # print(Ans)

	# Examples of counter-examples    
	# print (checker.check('(define-fun max2 ((x Int) (y Int)) Int 0)'))
    # print (checker.check('(define-fun max2 ((x Int) (y Int)) Int x)'))
    # print (checker.check('(define-fun max2 ((x Int) (y Int)) Int (+ x y))'))
    # print (checker.check('(define-fun max2 ((x Int) (y Int)) Int (ite (<= x y) y x))'))
