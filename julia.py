import time
from numba import jit, njit
from typing import List, Tuple, Callable
import numpy as np

Funkytype = Callable[[int, List[complex], List[complex]], List[int]]

def showtime(funky: Funkytype)->Funkytype:
    """decorator to show calculation time"""
    def shithead(a: int, b: List[complex], c:List[complex])->List[int]:
        start_time: float = time.time()
        output: List[int] = funky(a,b,c)
        end_time: float = time.time()
        secs: float = end_time - start_time
        print(f'{funky.__name__} took {secs} seconds.')
        return(output)
    return(shithead)

@njit
def func(m: int, z: complex, c: complex)->int:
    """julia rule"""
    n: int = 0
    while abs(z) < 2. and n < m:
        n=n+1
        z=z*z+c
    return(n)
    
@showtime
def calc_z_purepython(maxiter: int, 
                                  zs: List[complex], 
                                  cs: List[complex])->List[int]:
    """calculate outpout list using juia update rule"""
    output: List[int] = [0]*len(zs)
    for i in range(len(zs)):
        n = 0
        z: complex = zs[i]
        c: complex = cs[i]
        while abs(z) < 2. and n < maxiter:
            z = z * z + c
            n += 1
        output[i] = n
    return output
            
@showtime
def calc_z_dumpy(m: int, zs: List[complex], cs: List[complex])->List[int]:
    """calculate outpout list using juia update rule"""
    return [func(m,z,c) for z,c in zip(zs,cs)]
            
@showtime
def calc_z_frumpy(m, zs, cs):
    """calculate outpout list using juia update rule"""
    q=[]
    for z,c in zip(zs,cs):
        q.append(func(m,z,c))
    return(q)

def calc_pure_python(desired_width: float, max_iterations: int)->None:
    """build complex coordinates and julia set"""
    x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8
    c_real, c_imag = -0.62772, -.42193
    x_step: float = (x2-x1)/desired_width
    y_step: float = (y2-y1)/desired_width
    x: List[float] = []
    y: List[float] = []
    ycoord: float = y1
    while ycoord < y2:
        y.append(ycoord)
        ycoord += y_step
    xcoord:float = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step
    zs: List[complex] = []
    cs: List[complex] = []
    for ycoord in y:
        for xcoord in x:
            zs.append(complex(xcoord,ycoord))
            cs.append(complex(c_real,c_imag))
            
    calc_z_purepython(max_iterations, zs, cs)
    calc_z_frumpy(max_iterations, zs, cs)
    calc_z_dumpy(max_iterations, zs, cs)

calc_pure_python(desired_width=1000.0, max_iterations=30)


