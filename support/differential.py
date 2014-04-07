import support;
import numpy;

def rk4(function_pointer, a, b, steps, inputs, argv = None):
    "Runge-Kutta 4 function"
    
    "(in) function_pointer     - pointer to function"
    "(in) a                    - left point (start time)"
    "(in) b                    - right point (end time)"
    "(in) steps                - number of steps"
    "(in) inputs               - initial values"
    "(in) argv                 - extra arguments required by function_pointer"
    
    "Returns (times, values) calculated on whole specified segment of time (if ret_last == False) or (time, value) - values at time 'b'"
    
    step = (b - a) / steps;
    
    times = [0] * steps;
    values = [0] * steps;
    
    time_counter = a;
    
    for index in range(0, steps - 1):  
        times[index] = time_counter;
              
        k1 = step * function_pointer(times[index], values[index], argv);
        k2 = step * function_pointer(times[index] + step / 2, values[index] + k1 / 2, argv);
        k3 = step * function_pointer(times[index] + step / 2, values[index] + k2 / 2, argv);
        k4 = step * function_pointer(times[index] + step, values[index] + k3, argv);

        values[index + 1] = values[index] + (k1 + 2 * k2 + 2 * k3 + k4) / 6;
        time_counter += step;
    
    times[steps - 1] = b;
    return (times, values);


# def test_function(t, y, argv):
#     return 1 + y ** 2;
#
# (times, values) = rk4(test_function, 0, 1.4, 14, 0);
# draw_dynamics(times, values);