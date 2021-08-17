import numpy as np
from .figures import PZmap_Figure, Step_Figure,Impulse_Figure,Bode_Figure, Nichols_Figure, Rlocus_Figure

def generic_layout(fig,x_lim=None,y_lim=None,x_title=None,y_title=None):
    if x_title is not None:
        fig.set_x_title(x_title)
    
    if y_title is not None:
        fig.set_y_title(y_title)

    if x_lim is not None:
        fig.set_x_lim(x_lim)
    
    if y_lim is not None:
        fig.set_y_lim(y_lim)

    return fig

def pzmap(sys_list,x_lim=None,y_lim=None,x_title=None,y_title=None):
    """
    Returns a pole-zero plot of the continuous or discrete-time systems `sys_list`.
    
    Parameters
    ----------
    sys_list : system or list of systems
        A single system or a list of systems to analyse
    x_lim : list (optional)
        A list of two element that defines the min and max value for the x axis
    y_lim : list (optional)
        A list of two element  that defines the min and max value for the y axis
    x_title : str (optional)
        The x axis name
    y_title : str (optional)
        The y axis name

    Returns
    -------
    fig : plotly figure
        A plotly figure
    
    Example
    -------

    .. code ::

        import control as ctl
        from control_plotly import pzmap

        sys1 = ctl.tf([1],[2,1,1])
        sys2 = ctl.tf([1],[1,0.5,1])
        pzmap([sys1,sys2])

    .. image:: img/pzmap.png
        :alt: alternate text
        :align: center
    """

    fig = PZmap_Figure()
    if type(sys_list) is not list:
        sys_list = [sys_list]

    for index,sys in enumerate(sys_list):
        label = "sys{}".format(index+1)
        fig.add_plot(sys,label=label)

    fig = generic_layout(fig,x_lim=x_lim,y_lim=y_lim,x_title=x_title,y_title=y_title)

    return fig.show()


def generic_time_fig(fig,sys_list,t=None):

    if type(sys_list) is not list:
        sys_list = [sys_list]

    for index,sys in enumerate(sys_list):
        label = "sys{}".format(index+1)
        fig.add_plot(sys,T=t,label=label)

    return fig

def step(sys_list,t=None,x_lim=None,y_lim=None,x_title=None,y_title=None):
    """
    Returns the step response plot of the continuous or discrete-time systems `sys_list`.
    
    Parameters
    ----------
    sys_list : system or list of systems
        A single system or a list of systems to analyse
    t : numpy vector (optional)
        The base time vector
    x_lim : list (optional)
        A list of two element that defines the min and max value for the x axis
    y_lim : list (optional)
        A list of two element  that defines the min and max value for the y axis
    x_title : str (optional)
        The x axis name
    y_title : str (optional)
        The y axis name

    Returns
    -------
    fig : plotly figure
        A plotly figure
    
    Example
    -------

    .. code ::

        import control as ctl
        from control_plotly import step

        sys1 = ctl.tf([1],[2,1,1])
        sys2 = ctl.tf([1],[1,0.5,1])
        t = np.arange(0,20,0.01)

        step([sys1,sys2],t=t)

    .. image:: img/step.png
        :alt: alternate text
        :align: center

    """

    fig = Step_Figure()
    fig = generic_time_fig(fig,sys_list,t=t)
    fig = generic_layout(fig,x_lim=x_lim,y_lim=y_lim,x_title=x_title,y_title=y_title)

    return fig.show()

def impulse(sys_list,t=None,x_lim=None,y_lim=None,x_title=None,y_title=None):
    """
    Returns the impulse response of the continuous or discrete-time systems `sys_list`.
    
    Parameters
    ----------
    sys_list : system or list of systems
        A single system or a list of systems to analyse
    t : numpy vector (optional)
        The base time vector
    x_lim : list (optional)
        A list of two element that defines the min and max value for the x axis
    y_lim : list (optional)
        A list of two element  that defines the min and max value for the y axis
    x_title : str (optional)
        The x axis name
    y_title : str (optional)
        The y axis name

    Returns
    -------
    fig : plotly figure
        A plotly figure
    
    Example
    -------

    .. code ::

        import control as ctl
        from control_plotly import impulse

        sys1 = ctl.tf([1],[2,1,1])
        sys2 = ctl.tf([1],[1,0.5,1])
        t = np.arange(0,20,0.01)

        impulse([sys1,sys2],t=t)

    .. image:: img/impulse.png
        :alt: alternate text
        :align: center
    """

    fig = Impulse_Figure()
    fig = generic_time_fig(fig,sys_list,t=t)
    fig = generic_layout(fig,x_lim=x_lim,y_lim=y_lim,x_title=x_title,y_title=y_title)

    return fig.show()

def generic_frequency_fig(fig,sys_list,w=None):

    if type(sys_list) is not list:
        sys_list = [sys_list]

    for index,sys in enumerate(sys_list):
        label = "sys{}".format(index+1)
        fig.add_plot(sys,w=w,label=label)

    return fig

def bode(sys_list,w=None,x_lim=None,y_lim=None,dB=True,Hz=False,deg=True,log_x=True):
    """
    Returns the impulse response of the continuous or discrete-time systems `sys_list`.
    
    Parameters
    ----------
    sys_list : system or list of systems
        A single system or a list of systems to analyse
    w : numpy vector (optional)
        The base angular frequency vector (in rad/s)
    x_lim : list (optional)
        A list of two element that defines the min and max value for the x axis
    y_lim : list (optional)
        A list of two element  that defines the min and max value for the y axis
    dB : boolean (optional)
        Use a logarithmic scale for the magnitude plot
    Hz : boolean (optional)
        Use frequency in Hz for the x axis
    deg: boolean (optional)
        Use angle in degree for the phase plot.

    Returns
    -------
    fig : plotly figure
        A plotly figure
    
    Example
    -------

    .. code ::

        import control as ctl
        from control_plotly import bode

        sys1 = ctl.tf([1],[2,1,1])
        sys2 = ctl.tf([1],[1,0.5,1])
        w = np.logspace(-1,1,100)

        bode([sys1,sys2],w=w)

    .. image:: img/bode.png
        :alt: alternate text
        :align: center
    """

    fig = Bode_Figure(dB=dB,Hz=Hz,deg=deg,log_x=log_x)
    fig = generic_frequency_fig(fig,sys_list,w=w)
    fig = generic_layout(fig,x_lim=x_lim,y_lim=y_lim)

    return fig.show()

def nichols(sys_list,w=None,x_lim=None,y_lim=None,cm=np.array([6,3,1,.5,.25,0,-1,-3,-6,-12,-20,-40]),cp=np.array([1,5,10,20,30,50,90,120,150,180]),show_grid=True,show_mag=True,show_phase=True):

    """
    Returns the nichols chart of the continuous or discrete-time systems `sys_list`.
    
    Parameters
    ----------
    sys_list : system or list of systems
        A single system or a list of systems to analyse
    w : numpy vector (optional)
        The base angular frequency vector (in rad/s)
    x_lim : list (optional)
        A list of two element that defines the min and max value for the x axis
    y_lim : list (optional)
        A list of two element  that defines the min and max value for the y axis
    cm : numpy vector (optional)
        A numpy vector containing the list of contour gain (in dB)
    cp : numpy vector (optional)
        A numpy vector containing the list of contour phase (in deg)
    show_grid: boolean (optional)
        Add the nichols grid
    show_mag: boolean (optional)
        Show the nichols magnitude grid
    show_phase: boolean (optional)
        Show the nichols phase grid
    
    Returns
    -------
    fig : plotly figure
        A plotly figure
    
    Example
    -------

    .. code ::

        import control as ctl
        from control_plotly import nichols

        sys1 = ctl.tf([1],[2,1,1])
        sys2 = ctl.tf([1],[1,0.5,1])

        nichols([sys1,sys2])

    .. image:: img/nichols.png
        :alt: alternate text
        :align: center

    .. code ::

        import control as ctl
        import numpy as np
        from control_plotly import nichols

        sys = ctl.tf([1],[2,1,1])

        nichols(sys,show_phase=False,cm=np.array([0.5,-6]),x_lim=[-200,0],y_lim=[-40,10])

    .. image:: img/nichols2.png
        :alt: alternate text
        :align: center

    """

    if type(cm) is list:
        cm = np.array(cm)

    if type(cp) is list:
        cp = np.array(cp)

    fig =  Nichols_Figure(show_mag=show_mag,show_phase=show_phase)
    fig = generic_frequency_fig(fig,sys_list,w=w)

    if show_grid:
        fig.add_grid(cm=cm,cp=cp)

    fig = generic_layout(fig,x_lim=x_lim,y_lim=y_lim)

    return fig.show()


def rlocus(sys,k=None,x_lim=None,y_lim=None,show_grid=False,wn=np.arange(0.1,1.1,0.1),m=np.arange(0,1,0.1),):
    """
    Returns the root locus chart of the continuous or discrete-time systems `sys_list`.
    
    Parameters
    ----------
    sys : system 
        A single system
    k : numpy vector (optional)
        The vector of feedback gains 
    x_lim : list (optional)
        A list of two element that defines the min and max value for the x axis
    y_lim : list (optional)
        A list of two element  that defines the min and max value for the y axis
    show_grid: boolean (optional)
        Add the discrete to continuous pole grid
    
    Returns
    -------
    fig : plotly figure
        A plotly figure
    
    Example
    -------

    .. code ::

        import control as ctl
        from control_plotly import rlocus

        sys = ctl.tf([2,5,1],[1,2,3])
        rlocus(sys)

    .. image:: img/rlocus.png
        :alt: alternate text
        :align: center

    """

    if k is None:
        k = np.logspace(-2,1.2,200)

    if type(k) is list:
        k = np.array(k)

    if type(wn) is list:
        wn = np.array(wn)

    if type(m) is list:
        m = np.array(m)

    if type(sys) is list:
        raise ValueError("The rlocus function can only plot one system (not a list of systems)")



    fig =  Rlocus_Figure()
    fig.add_plot(sys,k)

    if show_grid:
        fig.add_grid(angle_list=wn,m_list=m)

    fig = generic_layout(fig,x_lim=x_lim,y_lim=y_lim)

    return fig.show()

