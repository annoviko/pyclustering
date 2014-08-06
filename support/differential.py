class diffsolver:
    DIFF_SOLVER_EULER = 0;
    DIFF_SOLVER_RK4 = 1;
    DIFF_SOLVER_RKF45 = 2;
    UNDEFINED = 3;


def rk4(function_pointer, inputs, a, b, steps, argv = None):
    "Runge-Kutta 4 function"
    
    "(in) function_pointer     - pointer to function"
    "(in) inputs               - initial values"
    "(in) a                    - left point (start time)"
    "(in) b                    - right point (end time)"
    "(in) steps                - number of steps"
    "(in) argv                 - extra arguments are required by function_pointer"
    
    "Returns (times, values)"
    
    step = (b - a) / steps;
    
    times = [0] * steps;
    values = [0] * steps;
    
    time_counter = a;
    
    values[0] = inputs;
    times[0] = a;
    
    for index in range(0, steps - 1):  
        k1 = step * function_pointer(times[index], values[index], argv);
        k2 = step * function_pointer(times[index] + step / 2, values[index] + k1 / 2, argv);
        k3 = step * function_pointer(times[index] + step / 2, values[index] + k2 / 2, argv);
        k4 = step * function_pointer(times[index] + step, values[index] + k3, argv);

        values[index + 1] = values[index] + (k1 + 2 * k2 + 2 * k3 + k4) / 6;
        time_counter += step;
        
        times[index + 1] = time_counter;
        
    
    times[steps - 1] = b;
    return (times, values);


def rkf45(function_pointer, inputs, a, b, steps = None, argv = None, tolerance = None):
    "Runge-Kutta-Felhberg (RKF45) function"
    
    "(in) function_pointer     - pointer to function"
    "(in) inputs               - initial values"
    "(in) a                    - left point (start time)"
    "(in) b                    - right point (end time)"
    "(in) steps                - [can be ingored] suggested number of steps, but it can be ignored because it step is changed during calculation"
    "(in) tolerance            - acceptable error for solving"
    "(in) argv                 - extra arguments are required by function_pointer"
    
    "Returns (times, values)"
    
    if (steps is None): steps = 50;
    if (tolerance is None): tolerance = 0.00001;
    
    # Butcher Tableau
    a2 = 1/4;       b2= 1/4; 
    a3 = 3/8;       b3 = 3/32;      c3 = 9/32; 
    a4 = 12/13;     b4 = 1932/2197; c4 = -7200/2197;    d4 = 7296/2197; 
    a5 = 1;         b5 = 439/216;   c5 = -8;            d5 = 3680/513;      e5 = -845/4104; 
    a6 = 1/2;       b6 = -8/27;     c6 = 2;             d6 = -3544/2565;    e6 = 1859/4104;     f6 = -11/40;   
    n1 = 25/216;    n3 = 1408/2565; n4 = 2197/4104;     n5 = -1/5;
    
    # Coef. for error that are defined from equation (y[k + 1] - z[k + 1]). It reduces time for solving value of Runge-Kutta 5.
    r1 = 1/360;     r3 = -128/4275; r4 = -2197/75240;   r5 = 1/50;          r6 = 2/55;      
    
    values = [];    # Values of calculation.
    times = [];     # Time.
    
    values.append(inputs);
    times.append(a);
    
    h = (b - a) / steps;    # Intial value of step.
    hmin = h / 100;         # Protection from infinite loop.
    hmax = 100 * h;         # Protection from slow solution.
    
    # Upper limit for time, helps calculate values at the last point.
    br = b - 0.00001 * abs(b);
    
    # big = 1e15;
    iteration_limit = 250;
    
    index = 0;
    while (times[index] < b):
        # function must be calculated at the last specified point
        if ((times[index] + h) > br):
            h = b - times[index];
        
        k1 = h * function_pointer(times[index], values[index], argv);
        y2 = values[index] + b2 * k1;

        
        k2 = h * function_pointer(times[index] + a2 * h, y2, argv);
        y3 = values[index] + b3 * k1 + c3 * k2;
        

        k3 = h * function_pointer(times[index] + a3 * h, y3, argv);
        y4 = values[index] + b4 * k1 + c4 * k2 + d4 * k3;

        
        k4 = h * function_pointer(times[index] + a4 * h, y4, argv);
        y5 = values[index] + b5 * k1 + c5 * k2 + d5 * k3 + e5 * k4;
        
        
        k5 = h * function_pointer(times[index] + a5 * h, y5, argv);
        y6 = values[index] + b6 * k1 + c6 * k2 + d6 * k3 + e6 * k4 + f6 * k5;
        
        
        k6 = h * function_pointer(times[index] + a6 * h, y6, argv);
        
        # Calculate error (difference between Runge-Kutta 4 and Runge-Kutta 5) and new value.
        err = abs(r1 * k1 + r3 * k3 + r4 * k4 + r5 * k5 + r6 * k6);
        
        # Calculate new value.
        ynew = values[index] + n1 * k1 + n3 * k3 + n4 * k4 + n5 * k5;
        
        if ((err < tolerance) or (h < 2 * hmin)):
            values.append(ynew);
            
            if (times[index] + h) > br:
                times.append(b);
            else:
                times.append(times[index] + h);
                
            index += 1;
            #print("t[", index, "] = ", times[index], ", y[", index, "] = ", values[index]);
        
        s = 0;

        if (err == 0): s = 0;
        else: s = 0.84 * ((tolerance * h / err) ** (0.25));
            
        if ((s < 0.75) and (h > 2.0 * hmin)):
            h = h / 2;
        
        if ((s > 1.5) and (h * 2 < hmax)):
            h = 2 * h;
        
        if (iteration_limit == index):
            print("Warning: iteration limit has been exceeded (limit:", iteration_limit);
            break;
        
        steps = index;
        if (b > times[index]):
            steps = index + 1;
        else:
            steps = index;
            
    return (times, values);
    

# def test_function(t, y, argv = None):
#     return 1 + y ** 2;
#  
# (times, values) = rk4(test_function, 0, 0, 1.4, 14);
# support.draw_dynamics(times, values);
#  
# (times, values) = rkf45(test_function, 0, 0, 1.4, 14, 0.000001);
# support.draw_dynamics(times, values);