import sys
import json
import pprint
import time


TRACE_ENABLED = False
stack_traces = []
stack_root = []

##### STEP 01 - START ######
## Arithmetic Ops
def do_multiply(args, envs):
    assert len(args) == 2
    left = do(args[0], envs)
    right = do(args[1], envs)
    return left * right

def do_divide(args, envs):
    assert len(args) == 2
    left = do(args[0], envs)
    right = do(args[1], envs)
    return left / right

def do_power(args, envs):
    assert len(args) == 2
    base = do(args[0], envs)
    exp = do(args[1], envs)
    return base ** exp

def do_modulo(args, envs):
    assert len(args) == 2
    left = do(args[0], envs)
    right = do(args[1], envs)
    return left % right

## Comparison Ops
def do_less_than(args, envs):
    assert len(args) == 2
    return 1 if do(args[0], envs) <  do(args[1], envs) else 0

def do_greater_than(args, envs):
    assert len(args) == 2
    return 1 if do(args[0], envs) >  do(args[1], envs) else 0

def do_less_than_or_equal_to(args, envs):
    assert len(args) == 2
    return 1 if do(args[0], envs) <= do(args[1], envs) else 0

def do_greater_than_or_equal_to(args, envs):
    assert len(args) == 2
    return 1 if do(args[0], envs) >= do(args[1], envs) else 0

def do_equal(args, envs):
    assert len(args) == 2
    return 1 if do(args[0], envs) == do(args[1], envs) else 0

def do_not_equal(args, envs):
    assert len(args) == 2
    return 1 if do(args[0], envs) != do(args[1], envs) else 0

## Boolean Ops
def do_and(args, envs):
    assert len(args) == 2
    a = do(args[0], envs)
    b = do(args[1], envs)
    return 1 if (a== 1 and b ==1) else 0

def do_or(args, envs):
    assert len(args) == 2
    a = do(args[0], envs)
    b = do(args[1], envs)
    return 1 if (a==1 or b==1) else 0

def do_not(args, envs):
    assert len(args) == 1
    a = do(args[0], envs)
    return 0 if (a==1) else 1

def do_do_until(args, envs):
    assert len(args) == 2
    body, cond = args[0], args[1]
    result = None
    while True:
        result = do(body, envs)
        if do(cond, envs): 
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

def env_set(name,value,envs):
    assert isinstance(name,str)
    envs[-1][name] = value

def do_set(args,envs):
    assert len(args) == 2
    assert isinstance(args[0],str)
    var_name = args[0]
    var_value = do(args[1],envs)
    env_set(var_name,var_value,envs)
    return var_value
    
def do_get(args,envs):
    assert len(args) == 1
    assert isinstance(args[0],str)
    var_name = args[0]
    return env_get(var_name,envs)

def do_seq(args,envs):
    # ["addieren", 2, 3], ["addieren", 4, 5]
    for each_ops in args:
        res = do(each_ops,envs)
    return res

def do_addieren(args,envs):
    assert len(args) == 2
    left = do(args[0],envs)
    right = do(args[1],envs)
    return left + right

def do_absolutewert(args,envs):
    assert len(args) == 1
    value = do(args[0],envs)
    if value >= 0:
        return value
    return -value

def do_subtrahieren(args,envs):
    assert len(args) == 2
    left = do(args[0],envs)
    right = do(args[1],envs)
    return left - right

def do_print(args, envs):
    args = [do(a, envs) for a in args]
    print(*args)
    return None

def do_func(args, envs):
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["func",params,body]


def env_get(name,envs):
    assert isinstance(name,str)
    # envs = [{"same":["func",...]},{"num":3}]
    # we do dynamic scoping
    for env in reversed(envs):
        if name in env:
            return env[name]
    assert False, f"Unknown variable {name}"


def do_call(args,envs):
    assert len(args) >= 1
    assert isinstance(args[0],str)
    name_func = args[0] #same
    values = [do(a,envs) for a in args[1:]] #[3]

    func = env_get(name_func,envs) # ["func",["num"],["get","num"]]
    assert isinstance(func,list) and (func[0] == "func")
    params = func[1]
    body = func[2]
    assert len(values) == len(params), f"You passed {len(values)} parameters instead of {len(params)}"

    local_env = dict()
    # params = ["num","num2"]
    # values = [3,4]
    # {"num":3, "num2":4}
    for index,param_name in enumerate(params):
        local_env[param_name] = values[index]
    envs.append(local_env)
    if TRACE_ENABLED:
        _trace_push(name_func)
    result = do(body,envs)
    if TRACE_ENABLED:
        _trace_pop()
    envs.pop()

    return result

#### STEP 01 - ADD_END ####

##### STEP 02 - START ######

# Arrays
def do_create_array(args, envs):
    assert len(args) == 1
    size = do(args[0], envs)
    return [0] * size

def do_get_array(args, envs):
    assert len(args) == 2
    array = do(args[0], envs)
    index = do(args[1], envs)
    assert isinstance(array, list), "First argument must be an array"
    assert isinstance(index, int), "Array index must be an integer"
    assert index >= 0, "Array index must be non-negative"
    assert index < len(array), f"Array index out of bounds"
    return array[index]

def do_set_array(args, envs):
    assert len(args) == 3
    array = do(args[0], envs)
    index = do(args[1], envs)
    value = do(args[2], envs)
    assert isinstance(array, list), "First argument must be an array"
    assert isinstance(index, int), "Array index must be an integer"
    assert index >= 0, "Array index must be non-negative"
    assert index < len(array), f"Array index out of bounds"
    array[index] = value
    return value

def do_get_size_array(args, envs):
    assert len(args) == 1
    array = do(args[0], envs)
    assert isinstance(array, list), "Argument must be an array"
    return len(array)

def do_concatenate_arrays(args, envs):
    assert len(args) == 2
    array1 = do(args[0], envs)
    array2 = do(args[1], envs)
    assert isinstance(array1, list), "First argument must be an array"
    assert isinstance(array2, list), "Second argument must be an array"
    return array1 + array2


# Sets
# Info regarding sets: Sets are an unordered collection of unique elements
def do_create_set(args, envs):
    assert len(args) == 0
    return set()

def do_add_set(args, envs):
    assert len(args) == 2
    arg_set = do(args[0], envs)
    value = do(args[1], envs)
    assert isinstance(arg_set, set), "First argument must be an set"
    if value not in arg_set:
        arg_set.add(value)
    else:
        pass
    return value

def do_remove_set(args, envs):
    assert len(args) == 2
    arg_set = do(args[0], envs)
    value = do(args[1], envs)
    assert isinstance(arg_set, set), "First argument must be an set"
    if value in arg_set:
        arg_set.remove(value)
    else:
        pass
    return value

def do_element_in_set(args, envs):
    assert len(args) == 2
    arg_set = do(args[0], envs)
    value = do(args[1], envs)
    assert isinstance(arg_set, set), "First argument must be an set"
    print("argset: ", arg_set)
    return 1 if value in arg_set else 0

def do_get_size_set(args, envs):
    assert len(args) == 1
    arg_set = do(args[0], envs)
    assert isinstance(arg_set, set), "Argument must be an set"
    return len(arg_set)

def do_merge_sets(args, envs):
    assert len(args) == 2
    set_a = do(args[0], envs)
    set_b = do(args[1], envs)
    return set_a.union(set_b)

##### STEP 02 - END ######

##### STEP 03 - START ######

#NOTE: In order to initiate the map function, we need to implement dynamic scoping in order to
# get the correct variables from the function given to the map function.
def do_map(args, envs):
    assert len(args) == 2 #Accepts an array and a function
    array = do(args[0], envs)
    assert isinstance(array, list)
    function_name = args[1]
    result = []
    #print(f"Environment: {envs}")
    for item in array:
         call_expr = ["call", function_name, item]
         mapped_item = do(call_expr, envs)
         result.append(mapped_item)
    return result


def do_reduce(args, envs):
    assert len(args) == 2           #Accepts an array and a function
    array = do(args[0], envs)
    assert isinstance(array, list)
    function_name = args[1]

    help_array = array.copy()       #Copy of the original array so that the original does not get manipulated
    result = 0                      #Acts as a counter
    result += array[0]              #Take the number on the first position of the array and add it to the counter
    help_array.pop(0)               #Remove the number on the first position of the array
    while len(help_array) > 0:      #While the array contains at least 1 element
        # Use the function on the result (counter) and the first item of the array, then remove first item of the array
        call_expr = ["call", function_name, result, help_array[0]]
        result = do(call_expr, envs)
        help_array.pop(0)
    return result


def do_filter(args, envs):
    assert len(args) == 2           #Accepts an array and a function
    array = do(args[0], envs)
    assert isinstance(array, list)
    function_name = args[1]
    result = []

    for item in array:
         call_expr = ["call", function_name, item]  #Result of function call is 0 or 1
         func_bool = do(call_expr, envs)                 #Safe result as a variable
         if func_bool:                                   #If result was 1, then append the item
             result.append(item)
    return result


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

##### STEP 04 - START ######
def _trace_push(name):
    node = {"name": name, "start": time.perf_counter(), "end": None, "children": []}
    if stack_traces:
        stack_traces[-1]["children"].append(node)
    else:
        stack_root.append(node)
    stack_traces.append(node)

def _trace_pop():
    if stack_traces:
        stack_traces[-1]["end"] = time.perf_counter()
        stack_traces.pop()

def _trace_print_tree():
    def render(node, indent=""):
        # time.sleep(0.01) - to debug in local
        dur = (node["end"] - node["start"]) * 1000 if node["end"] else 0.0
        if indent:
            print(f"{indent}+-- {node['name']} ({dur:.3f}ms)")
        else:
            print(f"{node['name']} ({dur:.3f}ms)")
        for ch in node["children"]:
            render(ch, indent + "    ")

    for root in stack_root:
        render(root)
##### STEP 04 - END ######


def do(program,envs):  # ["addieren",1,2]
    if isinstance(program,int):
        return program
    assert program[0] in OPS, f"Unkown operation {program[0]}"
    func = OPS[program[0]]
    return func(program[1:],envs)


def main():
    global TRACE_ENABLED
    if "--trace" in sys.argv:
        TRACE_ENABLED = True
        sys.argv.remove("--trace")

    filename = sys.argv[1]
    with open(filename, 'r') as f:
        program = json.load(f)
        envs = [dict()]
        result = do(program, envs)

    if TRACE_ENABLED:
        _trace_print_tree()
    else: 
        print(">>>", result)
        pprint.pprint(envs)    

if __name__ == '__main__':
    main()