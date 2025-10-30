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

#TODO: implement the algorithms 2.29 and 2.31 and an own creative one from https://math-sites.uncg.edu/sites/pauli/112/HTML/secalgrepeat.html#algevo

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
    args = [do(a, env) for a in args]
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

#### STEP 01 - ADD_END ####

##### STEP 02 - START ######

# Create an array
def do_create_array(args, env):
    assert len(args) == 1
    size = do(args[0], env)
    return [0] * size

# Get array element
def do_get_array(args, env):
    assert len(args) == 2
    array = do(args[0], env)
    index = do(args[1], env)
    assert isinstance(array, list), "First argument must be an array"
    assert isinstance(index, int), "Array index must be an integer"
    assert index >= 0, "Array index must be non-negative"
    assert index < len(array), f"Array index out of bounds"
    return array[index]

# Set array element
def do_set_array(args, env):
    assert len(args) == 3
    array = do(args[0], env)
    index = do(args[1], env)
    value = do(args[2], env)
    assert isinstance(array, list), "First argument must be an array"
    assert isinstance(index, int), "Array index must be an integer"
    assert index >= 0, "Array index must be non-negative"
    assert index < len(array), f"Array index out of bounds"
    array[index] = value
    return value

def do_get_size_array(args, env):
    assert len(args) == 1
    array = do(args[0], env)
    assert isinstance(array, list), "Argument must be an array"
    return len(array)

def do_concatenate_arrays(args, env):
    assert len(args) == 2
    array1 = do(args[0], env)
    array2 = do(args[1], env)
    assert isinstance(array1, list), "First argument must be an array"
    assert isinstance(array2, list), "Second argument must be an array"
    return array1 + array2


# Info regarding sets: Sets are an unordered collection of unique elements
# Create a set
def do_create_set(args, env):
    assert len(args) == 0
    return set()

# Add set element
def do_add_set(args, env):
    assert len(args) == 2
    arg_set = do(args[0], env)
    value = do(args[1], env)
    assert isinstance(arg_set, set), "First argument must be an set"
    if value not in arg_set:
        arg_set.add(value)
    else:
        pass
    return value

# Remove set element
def do_remove_set(args, env):
    assert len(args) == 2
    arg_set = do(args[0], env)
    value = do(args[1], env)
    assert isinstance(arg_set, set), "First argument must be an set"
    if value in arg_set:
        arg_set.remove(value)
    else:
        pass
    return value

def do_element_in_set(args, env):
    assert len(args) == 2
    arg_set = do(args[0], env)
    value = do(args[1], env)
    assert isinstance(arg_set, set), "First argument must be an set"
    for element in arg_set:
        if element in arg_set:
            return True
        else:
            return False

def do_get_size_set(args, env):
    assert len(args) == 1
    arg_set = do(args[0], env)
    assert isinstance(arg_set, set), "Argument must be an set"
    return len(arg_set)

def do_merge_sets(args, env):
    assert len(args) == 2
    set_a = do(args[0], env)
    set_b = do(args[1], env)
    return set_a.union(set_b)    #TODO The result is correct, nevertheless,
                                 # I don't get it how .union() gets to that specific order...


#### OPERATIONS START ####
OPS = {
    name.replace("do_","", 1): func
    for (name,func) in globals().items()
    if name.startswith("do_")
}


for operator, name in OPERATORS.items():
    if name in OPS:
        OPS[operator] = OPS[name]

#### OPERATIONS END ####

def do(program,env):  # ["addieren",1,2]
    if isinstance(program,int):
        return program
    #print(program[0]) # comment out to reduce debugging output
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