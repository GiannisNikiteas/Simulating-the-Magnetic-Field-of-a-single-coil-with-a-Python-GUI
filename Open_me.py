# -*- coding: utf-8 -*-
# Ioannis Nikiteas, 2015, Royal Holloway University of London 
# 3D Simulation of an EM field
import subprocess
from Tkinter import *
import numpy as np
from mayavi import mlab
from scipy import special
import tkFileDialog
import tkMessageBox as msg
from PIL import ImageTk, Image
import tkFont
# Externally sourced functionality for TkInter Widgets
from TkInterToolTip import ToolTip

#####################################################
# Menu Externally sourced, supplied by: Bryan Oakley
# link:http://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application
####################################################


TITLE_FONT = ("Times New Roman", 18, "bold")


class Menu(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both",expand=True )
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Visualisation, Report):
            framee = F(container, self)
            self.frames[F] = framee
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            framee.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, c):
        """ Show a frame for the given class """
        framee = self.frames[c]
        framee.tkraise()
    # def quit(self):
    #     self.root.quit()
    #     self.root.destroy()


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Home Page", font=TITLE_FONT)
        # img = PhotoImage(file="1.gif")             # Image in the background
        # container_lbl = Label(self, image = img)    # not working for some reason
        container_lbl = Label(self, bg='orange')
        container_lbl.pack(side="bottom", fill="both", expand=True)
        label.pack(side="top", fill="x", pady=10)

        button1 = Button(self, text="Go to Magnetic Field Simulation",
                         command=lambda: controller.show_frame(Visualisation))
        button2 = Button(self, text="Go to Lab Report", command=lambda: controller.show_frame(Report))
        button1.pack()
        button2.pack()

        
class Report(Frame):

    def __init__(self, parent, controller):  
        """ Opens the lab report """
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Lab Report Tab", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Go to Home Page",
                        command=lambda: controller.show_frame(StartPage))
        button.pack()
        frame = Frame(self) 
        frame.pack()
        self.inputs(frame)
        container_lbl = Label(self, bg='orange')
        container_lbl.pack(side="bottom", fill="both", expand=True)

    def inputs(self, frame):
        input_frame = Frame(frame)
        input_frame.grid(column=0, row=0)
        
        # Open Report Button
        open_report = Button(input_frame, text='Open Lab Report\n in pdf viewer', height=2,
                             fg='red', command=self.open_file)
        open_report.grid(column=0, row=6)

    @staticmethod
    def open_file():
        return subprocess.Popen('./Final_Project.pdf', shell=True)
        
        
class Visualisation(Frame):   
        
    def __init__(self, parent, controller):  
        """
        Visualise the magnetic field generated from a loop of wire with
        the help of a GUI.
        """  
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Magnetic Field Simulation of a Single Coil", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Go to Home Page",
                        command=lambda: controller.show_frame(StartPage))
        button.pack()
        frame = Frame(self)  # Define main frame for the Mayavi GUI
        frame.pack()
        self.inputs(frame)

    def inputs(self, frame):
        """
        Child to: Tk
        ________________________________________________        
        
        inputs method structures the GUI.
        It contains all the Buttons, Labels and Text boxes 
        """
        # Define child frame for the master
        input_frame = Frame(frame)
        input_frame.grid(column=0, row=0)
        
        # Add Sliders
        slider_r = Scale(input_frame, from_=1.0, to=5.0, orient=HORIZONTAL)
        slider_r.set(1.0)
        slider_r.grid(column=1, row=1)
        slider_i = Scale(input_frame, from_=-5.0, to=5.0, orient=HORIZONTAL)
        slider_i.set(1.0)
        slider_i.grid(column=1, row=2)
        
        # Plot sphere element Button
        seed_sphere = Button(input_frame, text='PLOT with \nSphere element',
                             command=self.sphere_projection)
        seed_sphere.grid(column=2, row=6)
        
        # Plot plane element Button
        seed_plane = Button(input_frame, text='PLOT with \nPlane element',
                            command=self.plane_projection)
        seed_plane.grid(column=1, row=6)
        
        # Plot line element Button
        plot_button = Button(input_frame, text=' PLOT with \nLine element', height=2,
                             fg='red', command=self.line_projection)
        plot_button.grid(column=0, row=6)
        
        # Text for Mayavi Scenes Controls
        text_size = tkFont.Font(family='Times New Roman', size=12)
        text = Text(input_frame, width=58, height=6, font=text_size)
        text.config(state=NORMAL)
        text.config(bg='orange', fg='black')
        text.insert(INSERT, 'Mayavi Visualasation Controls:\n \n'
                            '-Left-click: On the visualisation element to show more field lines\n'
                            '-Right-click and Drag: On the visualisation element to adjust its size\n'
                            '-Left-click and Drag: On the visualisation element to move it inside the field\n'
                            '-Scroll-up\down: To zoom in\out respectively')
        text.config(state=DISABLED)
        text.grid(column=0, row=8, columnspan=4)

        # Labels
        labelR = Label(input_frame, text='Radius R [m]:', justify=LEFT, anchor=W, relief=RIDGE)
        labelR.grid(column=0, row=1)
        labelI = Label(input_frame, text='Current I [A]:', justify=LEFT, anchor=W, relief=RIDGE)
        labelI.grid(column=0, row=2)
        labelbuttons = Label(input_frame, text='Volume Elements to Visualise the Field :', justify=LEFT, relief=RIDGE)
        labelbuttons.grid(column=0, row=4, columnspan=1, sticky=W)
        
        # Blank Lines
        emptylabel0 = Label(input_frame, text=' ', justify=LEFT)
        emptylabel0.grid(column=0, row=3)
        emptylabel1 = Label(input_frame, text=' ', justify=LEFT)
        emptylabel1.grid(column=0, row=5)
        emptylabel3 = Label(input_frame, text=' ', justify=LEFT)
        emptylabel3.grid(column=0, row=7, columnspan=4)
        
        # Information Buttons
        info1_text = StringVar()
        info1_text.set("  i  ")
        info1 = Label(input_frame, textvariable=info1_text, relief=RIDGE)
        info1.grid(column=2, row=4)

        # PLEASE SEE TkInterToolTip.py
        self.infoToolTip = ToolTip(info1,
                                   msg="+Using different geometric structures as unit elements\n "
                                       "of the magnetic field. Click and Drag the element to visualise the field.\n"
                                       "+The magnetic fields generated in this GUI are independent of the medium.\n"
                                       " and hence μ/μ0, see Section 3 from the report.\n"
                                       "+Change the background-foreground from the settings button in Mayavi sc\n"
                                       "+Feel free to save Mayavi scenes from the save icon!", delay=0)
        
        info2_text = StringVar()
        info2_text.set("  i  ")
        info2 = Label(input_frame, textvariable=info2_text, relief=RIDGE)
        info2.grid(column=2, row=2)

        self.infoToolTip = ToolTip(info2,
                                   msg="+The DC current in Amperes flowing through the circular loop.\n"
                                       "+When the current increases (absolute value),\n"
                                       " the magnetic field strength increases too.\n"
                                       "+I<0: the direction which the current flows changes,\n "
                                       "intended for AC simulation but Tkinter only produces static Mayavi scenes.\n"
                                       "+For I=0 you get a WARNING.", delay=0)
        info4_text = StringVar()
        info4_text.set("  i  ")
        info4 = Label(input_frame, textvariable=info4_text, relief=RIDGE)
        info4.grid(column=2, row=1)

        self.infoToolTip = ToolTip(info4,
                                   msg="+The radius R from the center of the circular loop in meters.\n"
                                       "+As R increases the magnetic field strength increases too.", delay=0)
        self._R, self._I = float(slider_r.get()), float(slider_i.get())

    def gen_field_lines(self, seed):
        """
        Visualising the magnetic field and using as a sphere as a volume
        element to analyse the field and its magnetic field lines
        """
        _R, _I = self._R, self._I

        # Generating the 3D space
        x, y, z = [i.astype(np.float32) for i in
                   np.ogrid[-20:20:200j, -20:20:200j, -20:20:200j]]

        r = np.sqrt(x ** 2 + y ** 2)
        x_trans = x / r  # cos(a)
        y_trans = y / r  # sin(a)

        E = special.ellipe((4 * _R * r) / ((_R + r) ** 2 + z ** 2))  # special ellipse E
        K = special.ellipk((4 * _R * r) / ((_R + r) ** 2 + z ** 2))  # special ellipse K
        Bz = _I / (2 * np.pi * np.sqrt((_R + r) ** 2 + z ** 2)) * (
                    K + E * (_R ** 2 - r ** 2 - z ** 2) / ((_R - r) ** 2 + z ** 2))

        # When r=0 there is a ZeroDivisionError for Br
        try:
            Br = (_I / (2 * np.pi * r)) * (z / (np.sqrt((_R + r) ** 2 + z ** 2))) * (
                        -K + E * ((_R ** 2 + r ** 2 + z ** 2) / ((_R - r) ** 2 + z ** 2)))
        except ZeroDivisionError:
            Br = 0
        # When the current I equals 0 there is no magnetic field
        if _I == 0:
            return msg.showwarning('WARNING:', 'When I=0, \n There is no magnetic field generated')

        else:
            mlab.close(all=True)
            Bx, By = x_trans * Br, y_trans * Br
            fig = mlab.figure(1, size=(700, 700), bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
            field = mlab.pipeline.vector_field(Bx, By, Bz)
            magnitude = mlab.pipeline.extract_vector_norm(field)
            contours = mlab.pipeline.iso_surface(magnitude,
                                                 contours=[0.001, 0.8, 3.8, 4.0],
                                                 transparent=True,
                                                 opacity=0.6,
                                                 colormap='YlGnBu',
                                                 vmin=0, vmax=0.5)

            field_lines = mlab.pipeline.streamline(magnitude, seedtype=seed,
                                                   integration_direction='both',
                                                   transparent=True,
                                                   opacity=0.3,
                                                   colormap='jet',
                                                   vmin=0, vmax=0.5)
            return field_lines

    def sphere_projection(self):
        """ Projects the magnetic field lines onto a sphere of adjustable radius and position """
        field_lines = self.gen_field_lines('sphere')
        field_lines.stream_tracer.maximum_propagation = 150.
        field_lines.seed.widget.radius = 5.5
        mlab.view(azimuth=42, elevation=73, distance=104)
        mlab.title('Visualisation of the magnetic field\n generated by a current loop')
        sc = mlab.scalarbar(field_lines, title='Field Strength [T]', orientation='vertical', nb_labels=4)
        sc.scalar_bar_representation.position2 = np.array([0.1,  0.8])
        sc.scalar_bar_representation.position = np.array([0.88374749,  0.14342105])
        mlab.show()

    def plane_projection(self):
        """ Projects the magnetic field lines on to a 2D surface """
        field_lines = self.gen_field_lines('plane')

        # Adjusting the camera and the seed location manually
        field_lines.stream_tracer.maximum_propagation = 40.
        field_lines.seed.widget.resolution = 10
        mlab.view(azimuth=42, elevation=73, distance=104)
        mlab.title('Visualisation of the magnetic field\n generated by a current loop')
        sc = mlab.scalarbar(field_lines, title='Field Strength [T]', orientation='vertical', nb_labels=4)
        sc.scalar_bar_representation.position2 = np.array([0.1,  0.8])
        sc.scalar_bar_representation.position = np.array([0.88374749,  0.14342105])
        mlab.show()

    def line_projection(self):
        field_lines = self.gen_field_lines('line')
        _R, _I = self._R, self._I
        # The following lines of code are not important
        # Camera adjustments, with numerical values for each case
        # Improve using lists and for-loop or a dictionary and if statements
        if _R == 1:
            field_lines.stream_tracer.maximum_propagation = 150.
            field_lines.seed.widget.point1 = [95, 100.5, 100]  # placing seed
            field_lines.seed.widget.point2 = [105, 100.5, 100]
            field_lines.seed.widget.resolution = 30
            # Setting the Default view
            mlab.view(azimuth=45, elevation=70, distance=105)
            mlab.title('Visualisation of the magnetic field\n generated by a current loop, with radius R=1m')
            sc = mlab.scalarbar(field_lines, title='Field Strength [T]', orientation='vertical', nb_labels=4)
            sc.scalar_bar_representation.position2 = np.array([0.1,  0.8])
            sc.scalar_bar_representation.position = np.array([0.88374749,  0.14342105])

        elif _R == 2:
            field_lines.stream_tracer.maximum_propagation = 150.
            field_lines.seed.widget.point1 = [90, 100.5, 100]
            field_lines.seed.widget.point2 = [110, 100.5, 100]
            field_lines.seed.widget.resolution = 30
            # Setting the Default view
            mlab.view(azimuth=60, elevation=70, distance=105)
            mlab.title('Visualisation of the magnetic field\n generated by a current loop, with radius R=2m')
            sc = mlab.scalarbar(field_lines, title='Field Strength [T]', orientation='vertical', nb_labels=4)
            sc.scalar_bar_representation.position2 = np.array([0.1,  0.8])
            sc.scalar_bar_representation.position = np.array([0.88374749,  0.14342105])

        elif _R == 3:
            field_lines.stream_tracer.maximum_propagation = 150.
            field_lines.seed.widget.point1 = [85, 100.5, 100]
            field_lines.seed.widget.point2 = [115, 100.5, 100]
            field_lines.seed.widget.resolution = 30
            mlab.view(azimuth=42, elevation=73, distance=104)
            mlab.title('Visualisation of the magnetic field\n generated by a current loop, with radius R=3m')
            sc = mlab.scalarbar(field_lines,title='Field Strength [T]', orientation='vertical', nb_labels=4)
            sc.scalar_bar_representation.position2 = np.array([0.1,  0.8])
            sc.scalar_bar_representation.position = np.array([0.88374749,  0.14342105])

        elif _R == 4:
            field_lines.stream_tracer.maximum_propagation = 150.
            field_lines.seed.widget.point1 = [80, 100.5, 100]
            field_lines.seed.widget.point2 = [120, 100.5, 100]
            field_lines.seed.widget.resolution = 30
            mlab.view(azimuth=42, elevation=73, distance=104)
            mlab.title('Visualisation of the magnetic field\n generated by a current loop, with radius R=4m')
            sc = mlab.scalarbar(field_lines, title='Field Strength [T]', orientation='vertical', nb_labels=4)
            sc.scalar_bar_representation.position2 = np.array([0.1,  0.8])
            sc.scalar_bar_representation.position = np.array([0.88374749,  0.14342105])

        elif _R == 5:
            field_lines.stream_tracer.maximum_propagation = 150.
            field_lines.seed.widget.point1 = [75, 100.5, 100]  # Position of
            field_lines.seed.widget.point2 = [125, 100.5, 100]  # the seed
            field_lines.seed.widget.resolution = 30
            mlab.view(azimuth=42, elevation=73, distance=104)
            mlab.title('Visualisation of the magnetic field\n generated by a current loop, with radius R=5m')
            sc = mlab.scalarbar(field_lines, title='Field Strength [T]', orientation='vertical', nb_labels=4)
            sc.scalar_bar_representation.position2 = np.array([0.1,  0.8])
            sc.scalar_bar_representation.position = np.array([0.88374749,  0.14342105])
        mlab.show()


app = Menu()
app.mainloop()


