namespace differential {

const double a2 = 1.0/4.0,		b2 = 1.0/4.0;
const double a3 = 3.0/8.0,		b3 = 3.0/32.0,			c3 = 9.0/32.0; 
const double a4 = 12.0/13.0,	b4 = 1932.0/2197.0,		c4 = -7200.0/2197.0,    d4 = 7296.0/2197.0; 
const double a5 = 1.0,			b5 = 439.0/216.0,		c5 = -8.0,				d5 = 3680.0/513.0,		e5 = -845.0/4104.0; 
const double a6 = 1.0/2.0,		b6 = -8.0/27.0,			c6 = 2.0,				d6 = -3544.0/2565.0,	e6 = 1859.0/4104.0,		f6 = -11.0/40.0;   
const double n1 = 25.0/216.0,	n3 = 1408.0/2565.0,		n4 = 2197.0/4104.0,		n5 = -1.0/5.0;
    
/* Coef. for error that are defined from equation (y[k + 1] - z[k + 1]). It reduces time for solving value of Runge-Kutta 5. */
const double r1 = 1.0/360.0,	r3 = -128.0/4275.0,		r4 = -2197.0/75240.0,	r5 = 1.0/50.0,			r6 = 2.0/55.0;

}