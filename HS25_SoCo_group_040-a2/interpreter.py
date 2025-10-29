import sys
import json
import pprint

env = dict()

##### STEP 01 - START ######
## Arithmetic Ops
def do_multiply(args, env):            
    assert len(args) == 2
    left = do(args[0], env)
    right = do(args[1], env)
    return left * right

def do_divide(args, env):           
    assert len(args) == 2
    left = do(args[0], env)
    right = do(args[1], env)
    return left / right

def do_power(args, env):           
    assert len(args) == 2
    base = do(args[0], env)
    exp = do(args[1], env)
    return base ** exp

def do_modulo(args, env):            
    assert len(args) == 2
    left = do(args[0], env)
    right = do(args[1], env)
    return left % right

## Comparison Ops
def do_less_than(args, env):             
    assert len(args) == 2
    return 1 if do(args[0], env) <  do(args[1], env) else 0

def do_greater_than(args, env):            
    assert len(args) == 2
    return 1 if do(args[0], env) >  do(args[1], env) else 0

def do_less_than_or_equal_to(args, env):            
    assert len(args) == 2
    return 1 if do(args[0], env) <= do(args[1], env) else 0

def do_greater_than_or_equal_to(args, env):            
    assert len(args) == 2
    return 1 if do(args[0], env) >= do(args[1], env) else 0

def do_equal(args, env):           
    assert len(args) == 2
    return 1 if do(args[0], env) == do(args[1], env) else 0

def do_not_equal(args, env):            
    assert len(args) == 2
    return 1 if do(args[0], env) != do(args[1], env) else 0

## Boolean Ops
def do_and(args, env):
    assert len(args) == 2
    a = do(args[0], env)
    b = do(args[1], env)
    return 1 if (a== 1 and b ==1) else 0

def do_or(args, env):
    assert len(args) == 2
    a = do(args[0], env)
    b = do(args[1], env)
    return 1 if (a==1 or b==1) else 0

def do_not(args, env):
    assert len(args) == 1
    a = do(args[0], env)
    return 0 if (a==1) else 1

## Do until --- TODO: check!!
def do_do_until(args, env):
    assert len(args) == 2
    body, cond = args[0], args[1]
    result = None
    while True:
        result = do(body, env)
        if do(cond, env): ## TODO: check here...
            break
    return result

OPERATORS = {
    "*":  "multiply",
    "/":  "divide",
    "^":  "power",
    "%":  "modulo",
    "<":  "less_than",
    ">":  "greater_than",
    "<=": "less_than_or_equal_to",
    ">=": "greater_than_or_equal_to",
    "==": "equal",
    "!=": "not_equal", 
    "AND": "and",
    "OR":  "or", 
    "NOT": "not",
    "do_until": "do_until"
}
##### STEP 01 - ENDS #####

## lecture notes
def do_set(args,env):
    assert len(args) == 2
    assert isinstance(args[0],str)
    var_name = args[0]
    var_value = do(args[1],env)
    env[var_name] = var_value
    return var_value
    
def do_get(args,env):
    assert len(args) == 1
    assert isinstance(args[0],str)
    assert args[0] in env, f"Unknown variable {args[0]}"
    return env[args[0]]

def do_seq(args,env):
    # ["addieren", 2, 3], ["addieren", 4, 5]
    for each_ops in args:
        res = do(each_ops,env)
    return res

def do_addieren(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left + right

def do_absolutewert(args,env):
    assert len(args) == 1
    value = do(args[0],env)
    if value >= 0:
        return value
    return -value

def do_subtrahieren(args,env):
    assert len(args) == 2
    left = do(args[0],env)
    right = do(args[1],env)
    return left - right

def do_print(args, env):
    args = [do(env, a) for a in args]
    print(*args)
    return None

def do_func(args, env):
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["func",params,body]

def do_call(args,env):
    assert len(args) >= 1
    assert isinstance(args[0],str)
    name_func = args[0] #same
    values = [do(a,env) for a in args[1:]] #[3]

    func = env[name_func] # ["func",["num"],["get","num"]]
    assert isinstance(func,list) and (func[0] == "func")
    params = func[1]
    body = func[2]
    assert len(values) == len(params), f"You passed {len(values)} parameters instead of {len(params)}"

    result = do(body,env)

    return result

OPS = {
    name.replace("do_","", 1): func
    for (name,func) in globals().items()
    if name.startswith("do_")
}

#### STEP 01 - ADD ####
for operator, name in OPERATORS.items():
    if name in OPS:
        OPS[operator] = OPS[name]
#### STEP 01 - ADD_END ####        

def do(program,env):  # ["addieren",1,2]
    if isinstance(program,int):
        return program
    print(program[0])
    assert program[0] in OPS, f"Unkown operation {program[0]}"
    func = OPS[program[0]]
    return func(program[1:],env)



def main():
    filename = sys.argv[1]
    with open(filename,'r') as f:
        program = json.load(f)
        env = dict() # {}
        result = do(program,env)
    print(">>>" , result)
    pprint.pprint(env)

if __name__ == '__main__':
    main()