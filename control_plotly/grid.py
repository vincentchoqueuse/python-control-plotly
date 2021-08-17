import numpy as np

def nichols_grid(gmin,pmin,pmax,cm=None,cp=None):
    
    # Round Gmin from below to nearest multiple of -20dB,
    # and Pmin,Pmax to nearest multiple of 360

    gmin = min(-20,20*np.floor(gmin/20))
    pmax = 360*np.ceil(pmax/360);
    pmin = min(pmax-360,360*np.floor(pmin/360));
    
    if cp is None:
        p1 = np.array([1,5,10,20,30,50,90,120,150,180])
    else:
        p1 = cp

    g1_part1 = np.array([6,3,2,1,.75,.5,.4,.3,.25,.2,.15,.1,.05,0,-.05,-.1,-.15,-.2,-.25,-.3,-.4,-.5,-.75,-1,-2,-3,-4,-5,-6,-9,-12,-16])
    g1_part2 =np.arange(-20,max(-40,gmin)-1,-10)
    
    if gmin >-40:
        g1 = np.hstack([g1_part1,g1_part2])
    else:
        g1 = np.hstack([g1_part1,g1_part2,gmin])
    
    # Compute gains GH and phases PH in H plane
    [p,g] = np.meshgrid((np.pi/180)*p1,10**(g1/20))
    z = g* np.exp(1j*p)
    H = z/(1-z)
    gH = 20*np.log10(np.abs(H))
    pH = np.remainder((180/np.pi)*np.angle(H)+360,360)
    
    # Add phase lines for angle between 180 and 360 (using symmetry)
    p_name = ["%.2f deg" % p1_temp for p1_temp in np.hstack([-360+p1,-p1])]
    gH = np.hstack([gH,gH])
    pH = np.hstack([pH,360-pH])
    phase_lines = []
    for indice in range(gH.shape[1]):
        phase_lines.append({"y": gH[:,indice],"x": pH[:,indice]-360,"name":p_name[indice]})

    # (2) Generate isogain lines for following gain values:
    if cm is None:
        g2_part1 = np.array([6,3,1,.5,.25,0,-1,-3,-6,-12,-20])
        g2_part2 = np.arange(-40,-20,gmin-1)
        g2 = np.hstack([g2_part1,g2_part2])
    else:
        g2 = cm

    #% Phase points
    p2 = np.array([1,2,3,4,5,7.5,10,15,20,25,30,45,60,75,90,105,120,135,150,175,180]);
    p2 = np.hstack([p2,np.flip(360-p2[:-1])])
    
    [g,p] = np.meshgrid(10**(g2/20),(np.pi/180)*p2)  # mesh in H/(1+H) plane
    z = g* np.exp(1j*p)
    H = z/(1-z)
    gH = 20*np.log10(np.abs(H))
    pH = np.remainder((180/np.pi)*np.angle(H)+360,360)
    
    # add gain line using symmetry
    g_name = ["%.2f dB" % g2_temp for g2_temp in g2]
    pH = pH-360
    
    mag_lines = []
    for indice in range(pH.shape[1]):
        mag_lines.append({"y": gH[:,indice],"x": pH[:,indice],"name":g_name[indice]})
    
    return mag_lines,phase_lines

def rlocus_grid(rad_max):
    
    data = []    
   
    # add frequency line
    wn_vect = np.linspace(0,rad_max,10)
    theta_vect = np.linspace(np.pi/2,3*np.pi/2,30)
    for index in range(len(wn_vect)):
        wn = wn_vect[index]
        name = "{:.3f} rad/s".format(wn)
        x = np.ravel(wn*np.cos(theta_vect))
        y = np.ravel(wn*np.sin(theta_vect))
        data_temp = {"x": x,"y":y,"name":name}
        data.append(data_temp)
    
    #add damping line
    wn_vect = np.linspace(0,rad_max,30)
    theta_vect = (np.pi/2)+np.pi*np.arange(20)/20
    for index in range(len(theta_vect)):
        theta = theta_vect[index]
        m = np.abs(np.cos(-theta))
        name = "m={:.3f}".format(m)
        x = np.ravel(wn_vect*np.cos(theta))
        y = np.ravel(wn_vect*np.sin(theta))
        data_temp = {"x": x,"y":y,"name":name}
        data.append(data_temp)
    
    return data

def drlocus_grid(angle_list=np.arange(0.1,1.1,0.1),m_list=np.arange(0,1,0.1)):
    
    data = []

    # add angular frequency line
    for index in range(len(angle_list)):
        wn = angle_list[index]*np.pi
        m_vect = np.linspace(0,1,25)
        dpole = np.exp(-m_vect*wn)*np.exp(1j*np.sqrt(1-m_vect**2)*wn)
        dpole = np.hstack([dpole,np.flip(np.conj(dpole))])
        name = "{:.1f} pi /dt".format(angle_list[index])
        x = np.real(dpole)
        y = np.imag(dpole)
        data_temp = {"x": x,"y":y,"name":name}
        data.append(data_temp)
    
    #add damping line
    for index in range(len(m_list)):
        m = m_list[index]
        wn_vect = np.linspace(0,np.pi/np.sqrt(1-m**2),25)
        dpole = np.exp(-m*wn_vect)*np.exp(1j*np.sqrt(1-m**2)*wn_vect)
        dpole = np.hstack([dpole,np.flip(np.conj(dpole))])
        name = "m={:.3f}".format(m)
        x = np.real(dpole)
        y = np.imag(dpole)
        data_temp = {"x": x,"y":y,"name":name}
        data.append(data_temp)
    
    return data


