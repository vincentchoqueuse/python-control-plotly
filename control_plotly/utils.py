import control as ctl
import numpy as np

def damp(sys,display=False):
    pole_list = []
    m_list = []
    wn_list = []

    for pole in sys.pole():
        pole = pole.astype(complex) # WTF: the python control "damp" function is buggy due to this missing cast !

        if ctl.isctime(sys):
            pole_continuous = pole
        else:
            pole_continuous = np.log(pole)/sys.dt
        
        wn = np.abs(pole_continuous)
        m = -np.real(pole_continuous)/wn

        pole_list.append(pole)
        wn_list.append(wn)
        m_list.append(m)

        if display:
            print("pole {:.3f} : wn={:.3f} rad/s, m= {:.3f}".format(pole, wn, m))

    return wn_list, m_list, pole_list
       
