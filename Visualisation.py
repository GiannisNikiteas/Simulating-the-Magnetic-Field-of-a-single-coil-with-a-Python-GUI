# # -*- coding: utf-8 -*-
# from Tkinter import *
# import numpy as np
# from mayavi import mlab
# from scipy import special
# import tkFileDialog
# import tkMessageBox as msg
# from PIL import ImageTk, Image
# import tkFont
#
# # Externally sourced functionality for TkInter Widgets
# from TkInterToolTip import ToolTip
#
# #####################################################
# # Creates a GUI Simulating a single coil loop
# #####################################################
#
#
# class Visualisation(object):
#
#     def __init__(self, master):
#         """
#         Visualise the magnetic field generated from a loop of wire with
#         the help of a GUI.
#         """
#         frame = Frame(master)  # Define main frame
#         frame.pack()
#         self.inputs(frame)
#
#     def inputs(self, frame):
#         """
#         Child to: Tk
#         ________________________________________________
#
#         inputs method structures the GUI.
#         It contains all the Buttons, Labels and Text boxes
#         """
#         # Define child frame for the master
#         input_frame = Frame(frame)
#         input_frame.grid(column=0, row=0)
#
#         # Add Sliders
#         slider_r = Scale(input_frame, from_=1.0, to=5.0, orient=HORIZONTAL)
#         slider_r.set(1.0)
#         slider_r.grid(column=1, row=1)
#         slider_i = Scale(input_frame, from_=-5.0, to=5.0, orient=HORIZONTAL)
#         slider_i.set(1.0)
#         slider_i.grid(column=1, row=2)
#
#         # Plot sphere element Button
#         seed_sphere = Button(input_frame, text='PLOT with \nSphere element',
#                              command=self.sphere_projection)
#         seed_sphere.grid(column=2, row=6)
#
#         # Plot plane element Button
#         seed_plane = Button(input_frame, text='PLOT with \nPlane element',
#                             command=self.plane_projection)
#         seed_plane.grid(column=1, row=6)
#
#         # Plot line element Button
#         plot_button = Button(input_frame, text=' PLOT with \nLine element', height=2,
#                              fg='red', command=self.generate_values)
#         plot_button.grid(column=0, row=6)
#
#         # Text for Mayavi Scenes Controls
#         text_size = tkFont.Font(family='Times New Roman', size=12)
#         text = Text(input_frame, width=58, height=6, font=text_size)
#         text.config(state=NORMAL)
#         text.config(bg='orange', fg='black')
#         text.insert(INSERT, 'Mayavi Visualasation Controls:\n \n'
#                             '-Left-click: On the visualisation element to show more field lines\n'
#                             '-Right-click and Drag: On the visualisation element to adjust its size\n'
#                             '-Left-click and Drag: On the visualisation element to move it inside the field\n'
#                             '-Scroll-up\down: To zoom in\out respectively')
#         text.config(state=DISABLED)
#         text.grid(column=0, row=8, columnspan=4)
#
#         # Labels
#         labelR = Label(input_frame, text='Radius R [m]:', justify=LEFT, anchor=W, relief=RIDGE)
#         labelR.grid(column=0, row=1)
#         labelI = Label(input_frame, text='Current I [A]:', justify=LEFT, anchor=W, relief=RIDGE)
#         labelI.grid(column=0, row=2)
#         labelbuttons = Label(input_frame, text='Volume Elements to Visualise the Field :', justify=LEFT, relief=RIDGE)
#         labelbuttons.grid(column=0, row=4, columnspan=1, sticky=W)
#
#         # Blank Lines
#         emptylabel0 = Label(input_frame, text=' ', justify=LEFT)
#         emptylabel0.grid(column=0, row=3)
#         emptylabel1 = Label(input_frame, text=' ', justify=LEFT)
#         emptylabel1.grid(column=0, row=5)
#         emptylabel3 = Label(input_frame, text=' ', justify=LEFT)
#         emptylabel3.grid(column=0, row=7, columnspan=4)
#
#         # Information Buttons
#         info1_text = StringVar()
#         info1_text.set("  i  ")
#         info1 = Label(input_frame, textvariable=info1_text, relief=RIDGE)
#         info1.grid(column=2, row=4)
#
#         # PLEASE SEE TkInterToolTip.py
#         self.infoToolTip = ToolTip(info1,
#                                    msg="+Using different geometric structures as unit elements\n "
#                                        "of the magnetic field. Click and Drag the element to visualise the field.\n"
#                                        "+The magnetic fields generated in this GUI are independent of the medium.\n"
#                                        " and hence μ/μ0, see Section 3 from the report.\n"
#                                        "+Change the background-foreground from the settings button in Mayavi sc\n"
#                                        "+Feel free to save Mayavi scenes from the save icon!", delay=0)
#
#         info2_text = StringVar()
#         info2_text.set("  i  ")
#         info2 = Label(input_frame, textvariable=info2_text, relief=RIDGE)
#         info2.grid(column=2, row=2)
#
#         self.infoToolTip = ToolTip(info2,
#                                    msg="+The DC current in Amperes flowing through the circular loop.\n"
#                                        "+When the current increases (absolute value),\n"
#                                        " the magnetic field strength increases too.\n"
#                                        "+I<0: the direction which the current flows changes,\n "
#                                        "intended for AC simulation but Tkinter only produces static Mayavi scenes.\n"
#                                        "+For I=0 you get a WARNING.", delay=0)
#         info4_text = StringVar()
#         info4_text.set("  i  ")
#         info4 = Label(input_frame, textvariable=info4_text, relief=RIDGE)
#         info4.grid(column=2, row=1)
#
#         self.infoToolTip = ToolTip(info4,
#                                    msg="+The radius R from the center of the circular loop in meters.\n"
#                                        "+As R increases the magnetic field strength increases too.", delay=0)
#         self.R, self.I = float(slider_r.get()), float(slider_i.get())
#
#     def sphere_projection(self):
#         """
#         Visualising the magnetic field and using as a sphere as a volume
#         element to analyse the field and its magnetic field lines
#         """
#         R, I = self.R, self.I
#
#         # Generating the 3D space
#         x, y, z = [i.astype(np.float32) for i in
#                    np.ogrid[-20:20:200j, -20:20:200j, -20:20:200j]]
#
#         r = np.sqrt(x ** 2 + y ** 2)
#         x_trans = x / r  # cos(a)
#         y_trans = y / r  # sin(a)
#
#         E = special.ellipe((4 * R * r) / ((R + r) ** 2 + z ** 2))  # special ellipse E
#         K = special.ellipk((4 * R * r) / ((R + r) ** 2 + z ** 2))  # special ellipse K
#         Bz = I / (2 * np.pi * np.sqrt((R + r) ** 2 + z ** 2)) * (
#                     K + E * (R ** 2 - r ** 2 - z ** 2) / ((R - r) ** 2 + z ** 2))
#
#         # When r=0 there is a ZeroDivisionError for Br
#         try:
#             Br = (I / (2 * np.pi * r)) * (z / (np.sqrt((R + r) ** 2 + z ** 2))) * (
#                         -K + E * ((R ** 2 + r ** 2 + z ** 2) / ((R - r) ** 2 + z ** 2)))
#         except ZeroDivisionError:
#             Br = 0
#         # When the current I equals 0 there is no magnetic field
#         if I == 0:
#             return msg.showwarning('WARNING:', 'When I=0, \n There is no magnetic field generated')
#
#         else:
#             mlab.close(all=True)
#             Bx, By = x_trans * Br, y_trans * Br
#             fig = mlab.figure(1, size=(500, 500), bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
#             field = mlab.pipeline.vector_field(Bx, By, Bz)
#             magnitude = mlab.pipeline.extract_vector_norm(field)
#             contours = mlab.pipeline.iso_surface(magnitude,
#                                                  contours=[0.001, 0.8, 3.8, 4.0],
#                                                  transparent=True,
#                                                  opacity=0.6,
#                                                  colormap='YlGnBu',
#                                                  vmin=0, vmax=0.5)
#
#             field_lines = mlab.pipeline.streamline(magnitude, seedtype='sphere',
#                                                    integration_direction='both',
#                                                    transparent=True,
#                                                    opacity=0.3,
#                                                    colormap='jet',
#                                                    vmin=0, vmax=0.5)
#
#             field_lines.stream_tracer.maximum_propagation = 150.
#             field_lines.seed.widget.radius = 5.5
#             mlab.view(azimuth=42, elevation=73, distance=104)
#             mlab.title('Visualisation of the magnetic field\n generated by a current loop')
#             sc = mlab.scalarbar(field_lines, title='Field Strength [T]', orientation='vertical', nb_labels=4)
#             sc.scalar_bar_representation.position2 = np.array([0.1, 0.8])
#             sc.scalar_bar_representation.position = np.array([0.88374749, 0.14342105])
#             mlab.show()
#             del x, y, z, r, E, K, Br, Bx, By, Bz
#
#     def plane_projection(self):
#         R, I = self.R, self.I
#         x, y, z = [i.astype(np.float32) for i in
#                    np.ogrid[-20:20:200j, -20:20:200j, -20:20:200j]]
#
#         r = np.sqrt(x ** 2 + y ** 2)
#         x_trans = x / r  # cos(a)
#         y_trans = y / r  # sin(a)
#
#         E = special.ellipe((4 * R * r) / ((R + r) ** 2 + z ** 2))  # special ellipse E
#         K = special.ellipk((4 * R * r) / ((R + r) ** 2 + z ** 2))  # special ellipse K
#         Bz = I / (2 * np.pi * np.sqrt((R + r) ** 2 + z ** 2)) * (
#                     K + E * (R ** 2 - r ** 2 - z ** 2) / ((R - r) ** 2 + z ** 2))
#         try:
#             Br = (I / (2 * np.pi * r)) * (z / (np.sqrt((R + r) ** 2 + z ** 2))) * (
#                         -K + E * ((R ** 2 + r ** 2 + z ** 2) / ((R - r) ** 2 + z ** 2)))
#         except ZeroDivisionError:
#             Br = 0
#
#         if I == 0:
#             return msg.showwarning('WARNING:', 'When I=0, \n There is no magnetic field generated')
#
#         else:
#             mlab.close(all=True)
#             Bx, By = x_trans * Br, y_trans * Br
#             fig = mlab.figure(1, size=(500, 500), bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
#
#             field = mlab.pipeline.vector_field(Bx, By, Bz)
#             magnitude = mlab.pipeline.extract_vector_norm(field)
#             contours = mlab.pipeline.iso_surface(magnitude,
#                                                  contours=[0.8, 3.8, 4.0],
#                                                  transparent=True,
#                                                  opacity=0.6,
#                                                  colormap='YlGnBu',
#                                                  vmin=0, vmax=0.5)
#
#             field_lines = mlab.pipeline.streamline(magnitude, seedtype='plane',
#                                                    integration_direction='both',
#                                                    transparent=True,
#                                                    opacity=0.3,
#                                                    colormap='jet',
#                                                    vmin=0, vmax=0.5)
#
#             field_lines.stream_tracer.maximum_propagation = 40.
#             field_lines.seed.widget.resolution = 10
#             mlab.view(azimuth=42, elevation=73, distance=104)
#             mlab.title('Visualisation of the magnetic field\n generated by a current loop')
#             sc = mlab.scalarbar(field_lines, title='Field Strength [T]', orientation='vertical', nb_labels=4)
#             sc.scalar_bar_representation.position2 = np.array([0.1, 0.8])
#             sc.scalar_bar_representation.position = np.array([0.88374749, 0.14342105])
#             del x, y, z, r, E, K, Br, Bx, By, Bz
#
#     def generate_values(self):
#         """
#         Function that uses a line element to "look through"
#         the magnetic field
#         """
#         # Connecting the sliders to the variables
#         R, I = self.R, self.I
#
#         # Creating 3D space
#         x, y, z = [i.astype(np.float32) for i in
#                    np.ogrid[-20:20:200j, -20:20:200j, -20:20:200j]]
#
#         # Converting Cartesian coord. to Polar
#         r = np.sqrt(x ** 2 + y ** 2)
#         x_trans = x / r  # cos(a)
#         y_trans = y / r  # sin(a)
#
#         E = special.ellipe((4 * R * r) / ((R + r) ** 2 + z ** 2))  # special ellipse E
#         K = special.ellipk((4 * R * r) / ((R + r) ** 2 + z ** 2))  # special ellipse K
#         Bz = (I) / (2 * np.pi * np.sqrt((R + r) ** 2 + z ** 2)) * (
#                     K + E * (R ** 2 - r ** 2 - z ** 2) / ((R - r) ** 2 + z ** 2))
#
#         # When r=0 there is a ZeroDivisionError for Br
#         try:
#             Br = (I / (2 * np.pi * r)) * (z / (np.sqrt((R + r) ** 2 + z ** 2))) * (
#                         -K + E * ((R ** 2 + r ** 2 + z ** 2) / ((R - r) ** 2 + z ** 2)))
#         except ZeroDivisionError:
#             Br = 0
#
#         if I == 0:
#             return msg.showwarning('WARNING:', 'When I=0, \n There is no magnetic field generated')
#
#         # Adjusting the view element/seed for each value of the current
#         # All this could have been avoided if a class containg the calculations
#         # could be imported inside the Visualasation class. Inheritance did not work
#
#         else:
#             if R == 1:
#                 mlab.close(all=True)
#                 Bx, By = x_trans * Br, y_trans * Br
#                 fig = mlab.figure(1, size=(500, 500), bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
#
#                 field = mlab.pipeline.vector_field(Bx, By, Bz)
#                 magnitude = mlab.pipeline.extract_vector_norm(field)
#                 contours = mlab.pipeline.iso_surface(magnitude,
#                                                      contours=[0.001, 0.8, 3.8, 4.0, 4.5],
#                                                      transparent=True,
#                                                      opacity=0.6,
#                                                      colormap='YlGnBu',
#                                                      vmin=0, vmax=0.5)
#
#                 field_lines = mlab.pipeline.streamline(magnitude, seedtype='line',
#                                                        integration_direction='both',
#                                                        transparent=True,
#                                                        opacity=0.3,
#                                                        colormap='jet',
#                                                        vmin=0, vmax=0.3)
#
#                 field_lines.stream_tracer.maximum_propagation = 150.
#                 field_lines.seed.widget.point1 = [95, 100.5, 100]  # placing seed
#                 field_lines.seed.widget.point2 = [105, 100.5, 100]
#                 field_lines.seed.widget.resolution = 30
#                 # Setting the Default view
#                 mlab.view(azimuth=45, elevation=70, distance=105)
#                 mlab.title('Visualisation of the magnetic field\n generated by a current loop, with radius R=1m')
#                 sc = mlab.scalarbar(field_lines, title='Field Strength [T]', orientation='vertical', nb_labels=4)
#                 sc.scalar_bar_representation.position2 = np.array([0.1, 0.8])
#                 sc.scalar_bar_representation.position = np.array([0.88374749, 0.14342105])
#
#             elif R == 2:
#                 mlab.close(all=True)
#                 Bx, By = x_trans * Br, y_trans * Br
#                 fig = mlab.figure(1, size=(500, 500), bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
#
#                 field = mlab.pipeline.vector_field(Bx, By, Bz)
#                 magnitude = mlab.pipeline.extract_vector_norm(field)
#                 contours = mlab.pipeline.iso_surface(magnitude,
#                                                      contours=[0.001, 0.5, 4.0, 5.0],
#                                                      transparent=True,
#                                                      opacity=0.6,
#                                                      colormap='YlGnBu',
#                                                      vmin=0, vmax=0.5)
#
#                 field_lines = mlab.pipeline.streamline(magnitude, seedtype='line',
#                                                        integration_direction='both',
#                                                        transparent=True,
#                                                        opacity=0.3,
#                                                        colormap='jet',
#                                                        vmin=0, vmax=0.5)
#
#                 field_lines.stream_tracer.maximum_propagation = 150.
#                 field_lines.seed.widget.point1 = [90, 100.5, 100]
#                 field_lines.seed.widget.point2 = [110, 100.5, 100]
#                 field_lines.seed.widget.resolution = 30
#                 # Setting the Default view
#                 mlab.view(azimuth=60, elevation=70, distance=105)
#                 mlab.title('Visualisation of the magnetic field\n generated by a current loop, with radius R=2m')
#                 sc = mlab.scalarbar(field_lines, title='Field Strength [T]', orientation='vertical', nb_labels=4)
#                 sc.scalar_bar_representation.position2 = np.array([0.1, 0.8])
#                 sc.scalar_bar_representation.position = np.array([0.88374749, 0.14342105])
#
#             elif R == 3:
#                 mlab.close(all=True)
#                 Bx, By = x_trans * Br, y_trans * Br
#                 fig = mlab.figure(1, size=(500, 500), bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
#                 field = mlab.pipeline.vector_field(Bx, By, Bz)
#                 magnitude = mlab.pipeline.extract_vector_norm(field)
#                 contours = mlab.pipeline.iso_surface(magnitude,
#                                                      contours=[0.001, 0.5, 4.5, 5.5],
#                                                      transparent=True,
#                                                      opacity=0.6,
#                                                      colormap='YlGnBu',
#                                                      vmin=0, vmax=0.5)
#
#                 field_lines = mlab.pipeline.streamline(magnitude, seedtype='line',
#                                                        integration_direction='both',
#                                                        transparent=True,
#                                                        opacity=0.3,
#                                                        colormap='jet',
#                                                        vmin=0, vmax=0.5)
#
#                 field_lines.stream_tracer.maximum_propagation = 150.
#                 field_lines.seed.widget.point1 = [85, 100.5, 100]
#                 field_lines.seed.widget.point2 = [115, 100.5, 100]
#                 field_lines.seed.widget.resolution = 30
#                 mlab.view(azimuth=42, elevation=73, distance=104)
#                 mlab.title('Visualisation of the magnetic field\n generated by a current loop, with radius R=3m')
#                 sc = mlab.scalarbar(field_lines, title='Field Strength [T]', orientation='vertical', nb_labels=4)
#                 sc.scalar_bar_representation.position2 = np.array([0.1, 0.8])
#                 sc.scalar_bar_representation.position = np.array([0.88374749, 0.14342105])
#
#             elif R == 4:
#                 mlab.close(all=True)
#                 Bx, By = x_trans * Br, y_trans * Br
#                 fig = mlab.figure(1, size=(500, 500), bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
#                 field = mlab.pipeline.vector_field(Bx, By, Bz)
#                 magnitude = mlab.pipeline.extract_vector_norm(field)
#                 contours = mlab.pipeline.iso_surface(magnitude,
#                                                      contours=[0.001, 0.5, 4.5, 5.5],
#                                                      transparent=True,
#                                                      opacity=0.6,
#                                                      colormap='YlGnBu',
#                                                      vmin=0, vmax=0.5)
#
#                 field_lines = mlab.pipeline.streamline(magnitude, seedtype='line',
#                                                        integration_direction='both',
#                                                        transparent=True,
#                                                        opacity=0.3,
#                                                        colormap='jet',
#                                                        vmin=0, vmax=0.5)
#
#                 field_lines.stream_tracer.maximum_propagation = 150.
#                 field_lines.seed.widget.point1 = [80, 100.5, 100]
#                 field_lines.seed.widget.point2 = [120, 100.5, 100]
#                 field_lines.seed.widget.resolution = 30
#                 mlab.view(azimuth=42, elevation=73, distance=104)
#                 mlab.title('Visualisation of the magnetic field\n generated by a current loop, with radius R=4m')
#                 sc = mlab.scalarbar(field_lines, title='Field Strength [T]', orientation='vertical', nb_labels=4)
#                 sc.scalar_bar_representation.position2 = np.array([0.1, 0.8])
#                 sc.scalar_bar_representation.position = np.array([0.88374749, 0.14342105])
#
#             elif R == 5:
#                 mlab.close(all=True)
#                 Bx, By = x_trans * Br, y_trans * Br
#                 fig = mlab.figure(1, size=(500, 500), bgcolor=(1, 1, 1), fgcolor=(0, 0, 0))
#                 field = mlab.pipeline.vector_field(Bx, By, Bz)
#                 magnitude = mlab.pipeline.extract_vector_norm(field)
#
#                 contours = mlab.pipeline.iso_surface(magnitude,
#                                                      contours=[0.001, 0.8, 3.8],
#                                                      transparent=True,
#                                                      opacity=0.6,
#                                                      colormap='YlGnBu',
#                                                      vmin=0, vmax=0.5)
#
#                 field_lines = mlab.pipeline.streamline(magnitude, seedtype='line',
#                                                        integration_direction='both',
#                                                        transparent=True,
#                                                        opacity=0.3,
#                                                        colormap='jet',
#                                                        vmin=0, vmax=0.5)
#
#                 field_lines.stream_tracer.maximum_propagation = 150.
#                 field_lines.seed.widget.point1 = [75, 100.5, 100]  # Position of
#                 field_lines.seed.widget.point2 = [125, 100.5, 100]  # the seed
#                 field_lines.seed.widget.resolution = 30
#                 mlab.view(azimuth=42, elevation=73, distance=104)
#                 mlab.title('Visualisation of the magnetic field\n generated by a current loop, with radius R=5m')
#                 sc = mlab.scalarbar(field_lines, title='Field Strength [T]', orientation='vertical', nb_labels=4)
#                 sc.scalar_bar_representation.position2 = np.array([0.1, 0.8])
#                 sc.scalar_bar_representation.position = np.array([0.88374749, 0.14342105])
#             # Free memory at the end of all calculations
#             del x, y, z, r, E, K, Br
#
#         mlab.show()
#
#
# root = Tk()
# gui = Visualisation(root)
# root.mainloop()
