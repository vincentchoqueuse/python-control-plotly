import plotly.graph_objects as go
import numpy as np
import control as ctl
import plotly
import json
from plotly.subplots import make_subplots
from .grid import nichols_grid,drlocus_grid

class Figure():

    color_list = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#EF553B", "brown"]
    x_title = ""
    y_title = ""
    x_scaleanchor = None
    x_scaleratio = 1
    y_scaleanchor = None
    y_scaleratio = 1
    
    def __init__(self,log_x=False,log_y=False):
        self.plot_data = []
        self.grid_data = []
        self.extra_data = []
        self.type = None
        self.x_range = None
        self.y_range = None
        self.index = 0
        self.log_x = log_x 
        self.log_y = log_y

    def get_x_title(self):
        return self.x_title

    def set_x_title(self,title):
        self.x_title = title

    def get_y_title(self):
        return self.y_title

    def set_y_title(self,title):
        self.y_title = title    

    def get_x_type(self):
        "Returns the type for the xaxis (log or linear)"
        if self.log_x == True:
            type = "log"
        else:
            type = "linear"
        return type 

    def get_y_type(self):
        "Returns the type for the yaxis (log or linear)"
        if self.log_y == True:
            type = "log"
        else:
            type = "linear"
        return type 

    def get_next_color(self):
        "Returns the next curve color"
        nb_colors = len(self.color_list)
        color = self.color_list[self.index]
        self.index += 1
        self.index = self.index%nb_colors
        return color
    
    def get_grid_line(self):
        "Returns the plotly grid line"
        return dict(color="#555", width=1, dash="dot")
    
    def get_line_shape(self,tf):
        "Returns the line shape for a particular transfer function (linear for continuous systems and hv for discrete systems)"
        if ctl.isctime(tf):
            line_shape = "linear"
        else:
            line_shape = "hv"
        
        return line_shape 
    
    def set_x_lim(self,range):
        "Specify the xlim range"
        self.x_range = range
    
    def set_y_lim(self,range):
        "Specify the ylim range"
        self.y_range = range

    def clear(self):
        self.clear_plot()
        self.clear_grid()
        self.clear_extra()

    def clear_plot(self):
        self.plot_data = []

    def clear_grid(self):
        self.grid_data = []

    def clear_extra(self):
        self.extra_data = []

    @property
    def data(self):
        data = self.plot_data
        data = data + self.grid_data
        data = data + self.extra_data
        return data

    @property
    def layout(self):
        "Returns the plotly figure layout"

        # create xaxis dict
        xaxis = {"title": {"text": self.get_x_title()},
                 "type": self.get_x_type() 
                }   
        if self.x_range is not None:
            xaxis["range"] = self.x_range

        if self.x_scaleanchor is not None:
            xaxis["scaleanchor"] = self.x_scaleanchor
            xaxis["scaleratio"] = self.x_scaleratio
        
        # create yaxis dict
        yaxis = {"title": {"text": self.get_y_title()},
                "type": self.get_y_type() 
                }
        if self.y_range is not None:
            yaxis["range"] = self.y_range

        if self.x_scaleanchor is not None:
            yaxis["scaleanchor"] = self.y_scaleanchor
            yaxis["scaleratio"] = self.y_scaleratio


        layout =  { "xaxis": xaxis,"yaxis": yaxis}
        return layout


    def show(self,show_data=True,show_grid=True,show_extra=True):
        "Constructs the figure and return the plotly figure instance"

        data = self.data
        layout = self.layout

        fig = go.Figure(data, layout=layout)
        return fig

    def json(self):
        "Returns a json representation of the plotly data"
        fig = self.show()
        return json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)


class Time_Figure(Figure):

    x_title = "time (s)"
    y_title = "amplitude"

    def get_response(self,tf,type="step",T=None):
        "Return the response of the system `tf`. The type attribute specifies the reponse type (`step` or `impulse`)"
        
        if type == "step":
            T, yout = ctl.step_response(tf,T=T)
        if type == "impulse":
            T, yout = ctl.impulse_response(tf,T=T)

        return T,yout

    def add_plot(self,tf,type=None,T=None,label="sys"):
        "Add a new plot for the system `tf`."
        line_shape = self.get_line_shape(tf)
        line = dict(color=self.get_next_color())
        T, yout = self.get_response(tf,type=type,T=T)
        data = {"x":T,"y":yout,"line": line,"name":label,"mode":"lines","line_shape":line_shape}
        self.plot_data.append(data)

class Step_Figure(Time_Figure):

    def get_response(self,tf,type=None,T=None):
        "Return the step response" 
        return ctl.step_response(tf,T=T)

class Impulse_Figure(Time_Figure):

    def get_response(self,tf,type=None,T=None):
        "Return the impulse response" 
        return ctl.impulse_response(tf,T=T)

class PZmap_Figure(Figure):

    x_title = "Real Axis"
    y_title = "Imag Axis"
    x_scaleanchor = "x"

    def add_plot(self,tf,label="sys"):
        line = dict(color=self.get_next_color())
        data  = []

        poles = tf.pole()
        data_poles =  {
                    "x": np.real(poles),
                    "y": np.imag(poles),
                    "name": label,
                    "line": line,
                    "hovertemplate": "<b>Pole<b><br><b>real</b>: %{x:.3f}<br><b>imag</b>: %{y:.3f}<br>",
                    "mode": "markers",
                    "marker": {"symbol": "x", "size": 8},
                }

        zeros = tf.zero()
        data_zeros =  {
            "x": np.real(zeros),
            "y": np.imag(zeros),
            "name": label,
            "line": line,
            "hovertemplate": "<b>Zero<b><br><b>real</b>: %{x:.3f}<br><b>imag</b>: %{y:.3f}<br>",
            "mode": "markers",
            "marker": {"symbol": "circle", "size": 8},
        }

        self.plot_data.append(data_poles)
        self.plot_data.append(data_zeros)

class Bode_Figure(Figure):

    def __init__(self,dB=False,Hz=False,deg=True,log_x=True):
        self.plot_data_mag = []
        self.plot_data_phase = []
        self.type = None
        self.x_range = None
        self.y_range = None
        self.deg = deg
        self.dB = dB
        self.Hz = Hz 
        self.log_x = log_x
        self.index = 0

    def get_x_title(self):
        if self.Hz: 
            x_title = "f (Hz)"
        else:
            x_title = "w (rad/s)"
        return x_title

    def get_y1_title(self):
        if self.dB:
            y_title = "Magnitude (dB)"
        else:
            y_title = "Magnitude"
        return y_title

    def get_y2_title(self):
        if self.deg:
            y_title = "Phase (deg)"
        else:
            y_title = "Phase (rad)"
        return y_title


    def add_plot(self,tf,w=None,label="sys"):
        mag_list, phase_list, w = ctl.bode_plot(tf, omega=w, plot=False, omega_limits=None, omega_num=None, margins=None)

        units = ["","rad/s","rad"]

        if self.dB:
            mag_list = 20*np.log10(mag_list)
            units[0] = "dB"
        if self.deg :
            phase_list = phase_list*180/(np.pi)
            units[2] = "deg"
        if self.Hz :
            w_str = "f"
            w = w/(2*np.pi)
            units[1] = "Hz"
        else:
            w_str = "w"

        line = dict(color=self.get_next_color())

        data_mag = {
            "x": w,
            "y": mag_list,
            "line": line,
            "name": label,
            "hovertemplate": "<b>{}</b>: %{{x:.3f}} {}<br><b>mag</b>: %{{y:.3f}} {}<br><b>phase</b>: %{{text:.3f}} {}<br>".format(w_str,units[1],units[0],units[2]),
            "text": phase_list,
            "showlegend": False
            }
        
        data_phase = {
            "x": w,
            "y": phase_list,
            "line": line,
            "name": label,
            "hovertemplate": "<b>{}</b>: %{{x:.3f}} {}<br><b>mag</b>: %{{text:.3f}} {}<br><b>phase</b>: %{{y:.3f}} {}<br>".format(w_str,units[1],units[0],units[2]),
            "text": mag_list,
            "showlegend": False
            }
            
        self.plot_data_mag.append(data_mag)
        self.plot_data_phase.append(data_phase)

    def show(self):

        x_type = self.get_x_type()

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
        fig.add_traces(self.plot_data_mag, rows=1, cols=1)
        fig.add_traces(self.plot_data_phase, rows=2, cols=1)

        if self.x_range is not None:
            fig.update_xaxes(range=self.x_range, row=1, col=1)
            fig.update_xaxes(range=self.x_range, row=2, col=1)

        fig.update_yaxes(title_text=self.get_y1_title(), row=1, col=1)
        fig.update_xaxes(title_text=self.get_x_title(), type=x_type, row=1, col=1)
        fig.update_yaxes(title_text=self.get_y2_title(), row=2, col=1)
        fig.update_xaxes(title_text=self.get_x_title(), type=x_type, row=2, col=1)

        return fig


class Nichols_Figure(Figure):

    x_title = "Open-Loop Phase (deg)"
    y_title = "Open-Loop Gain (dB)"
    
    def __init__(self,show_mag,show_phase):
        self.plot_data = []
        self.grid_data = []
        self.extra_data = [{"x":[-180],"y":[0],"hoverinfo":"none",  "mode": "markers","marker": {"size": 3,"line":dict(color="#FF0000", width=1)},"showlegend": False,}]
        self.type = None
        self.index = 0
        self.gmin = 1000
        self.pmin = 1000
        self.pmax = -1000
        self.x_range = None
        self.y_range = None
        self.log_x = False
        self.log_y = False
        self.show_mag = show_mag
        self.show_phase = show_phase

    def update_min_max(self,mag,phase):
        self.gmin = min(np.min(mag),self.gmin)
        self.pmin = min(np.min(phase),self.pmin)
        self.pmax = max(np.max(phase),self.pmax)

    def add_grid(self,cm=None,cp=None):

        mag_list, phase_list = nichols_grid(self.gmin,self.pmin,self.pmax,cm=cm,cp=cp)
        line = self.get_grid_line()

        if self.show_mag == True:
            for mag in mag_list:
                data_temp ={
                    "x": mag["x"],
                    "y": mag["y"],
                    "name": mag["name"],
                    "hoverinfo": "name",
                    "line": line,
                    "showlegend": False,
                    }
                self.grid_data.append(data_temp)

        if self.show_phase == True:
            
            for phase in phase_list:
                data_temp ={
                        "x": phase["x"],
                        "y": phase["y"],
                        "name": phase["name"],
                        "hoverinfo": "name",
                        "line": line,
                        "showlegend": False,
                        }
                self.grid_data.append(data_temp)

    
    def add_plot(self,tf,w=None,label="sys"):

        mag_list, phase_list, w = ctl.bode_plot(tf, omega=w, dB=True, plot=False, omega_limits=None, omega_num=None, margins=None)
        mag_list = 20*np.log10(mag_list)
        phase_list = phase_list*180/(np.pi)

        line = dict(color=self.get_next_color())
        data ={
                "x": phase_list,
                "y": mag_list,
                "name": label,
                "line": line,
                "hovertemplate": "<b>w</b>: %{text:.3f} rad/s<br><b>mag</b>: %{y:.3f} dB<br><b>phase</b>: %{x:.3f} deg<br>",
                "text": w,  
                "showlegend": False,
                }
        
        self.update_min_max(mag_list,phase_list)
        self.plot_data.append(data)

    
class Rlocus_Figure(Figure):

    x_title = "Real Axis"
    y_title = "Imag Axis"
    x_scaleanchor = "x"
    
    def __init__(self):
        self.plot_data = []
        self.grid_data = []
        self.extra_data = []
        self.type = None
        self.index = 0
        self.x_range = None
        self.y_range = None
        self.log_x = False
        self.log_y = False
    
    def add_grid(self,angle_list=np.arange(0.1,1.1,0.1),m_list=np.arange(0,1,0.1)):
        line = self.get_grid_line()
        grid_data =  drlocus_grid(angle_list=angle_list,m_list=m_list)
        
        for grid_temp in grid_data:
            data_temp ={
                    "x": grid_temp["x"],
                    "y": grid_temp["y"],
                    "name": grid_temp["name"],
                    "hoverinfo": "name",
                    "line": line,
                    "showlegend": False,
                    }

            self.grid_data.append(data_temp)
        
    
    def add_plot(self,tf,k=np.logspace(-2,1.2,1000),label="sys"):
        
        isctime = ctl.isctime(tf)
        poles = []
        for k_temp in k :
            tf_cl = ctl.feedback(k_temp*tf,1)
            poles.append(tf_cl.pole())

        #prepare_data
        poles = np.array(poles)
        nb_poles = poles.shape[1]
        data = []
        
        hovertemplate = "<b>K</b>: %{text:.3f}<br><b>imag</b>: %{y:.3f}<br><b>real</b>: %{x:.3f}<br>m: %{customdata[0]:.3f}<br>wn: %{customdata[1]:.3f} rad/s"

        for index in range(nb_poles):
            pole = poles[:,index]
            line = dict(color=self.get_next_color())
            x = np.real(pole)
            y = np.imag(pole)
            name = "{} p{}".format(label,index+1)
            
            #get info
            custom_data = np.zeros((len(x),2))
            for index, pole_temp in enumerate(pole):
                
                if isctime:
                    pole = pole_temp
                else:
                    pole_temp = pole_temp.astype(complex) 
                    pole = np.log(pole_temp)/tf.dt

                wn = np.abs(pole)
                m = -np.real(pole)/wn
                custom_data[index,:]= [m,wn]
            
            data = {"x":x,"y":y,"text":k,"name":name,"line":line,"showlegend":False,"customdata":custom_data,"hovertemplate": hovertemplate}
            self.plot_data.append(data)
            
            data = {"x":[x[0]],"y":[y[0]],"line":line, "mode": "markers","marker":{"symbol":"x","size":8},"showlegend":False}
            self.plot_data.append(data)
