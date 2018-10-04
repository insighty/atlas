import foundations
from model import incr_by_10, mult

# input to model
x = 20

# build step1 of model
incr_value = foundations.create_stage(incr_by_10(x))

# build step2 of model
result = foundations.create_stage(mult(x, incr_value))

# run the model
result.run()
