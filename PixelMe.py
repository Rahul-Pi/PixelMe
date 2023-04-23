import argparse
import cv2 
import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog,messagebox,ttk
import time
import threading
import webbrowser

# Video player class
class image_player(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.image_update_val = 30
        self.cur_image_index = 0

        # Read an image using opencv
        self.cur_image_path = os.path.join(".","assets","intro.png")

        imageplayer = ttk.Frame(self)

        # The video Tkinter frame
        self.imagepanel = ttk.Frame(imageplayer)
        self.imagelabel = ttk.Label(self.imagepanel)
        self.imagelabel.pack(fill=tk.BOTH,expand=1)
        self.imagepanel.pack(side=tk.BOTTOM,fill=tk.BOTH, expand=1, padx=[0,10])

        imageplayer.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

        # The side frame which include the video playback speed and the help button
        self.side_tab = ttk.Frame(self)
        
        # Help button
        self.help_btn = tk.Button(self.side_tab, text="Help", font='sans 10 bold', height=2, width=12, background="#343434", foreground="white", command = self.help_btn_browser)
        self.help_btn.pack(side=tk.BOTTOM,expand=1, padx=[10,0], pady=[10,50])
        
        # The logos
        # The logo is created using the icons from https://www.flaticon.com/free-icons/schedule and https://www.flaticon.com/free-icons/professions-and-jobs
        PixelMe_logo = ImageTk.PhotoImage(Image.open(os.path.join(".","assets","PixelMe.png")).resize((100,82), Image.Resampling.LANCZOS))
        PixelMe_logo_label = ttk.Label(self.side_tab, image=PixelMe_logo)
        PixelMe_logo_label.image = PixelMe_logo
        PixelMe_logo_label.pack(side=tk.BOTTOM,expand=1, padx=[10,0], pady=[0,20])
        
        self.side_tab.pack(side=tk.BOTTOM)

        self.frame_update()
        self.update()

        self.grid(column=2, row=0, columnspan=5, rowspan = 4, padx=5, pady=5, sticky='s')

        for i in range(1,len(app.sub_class_list)+1):
                app.bind(str(i), self.num_key_press)
        app.bind("<Right>", self.right_key_press)
        app.bind("<Left>", self.left_key_press)


    def help_btn_browser(self):
        # webbrowser.open(r"https://www.google.com",autoraise=True)
        pass

    def frame_update(self):
        try:
            self.OCV_image = cv2.imread(self.cur_image_path)
            cv2image= cv2.cvtColor(self.OCV_image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image = img.resize((720,562), Image.Resampling.LANCZOS))
            self.imagelabel.imgtk = imgtk
            self.imagelabel.configure(image=imgtk)
            self.imagepanel.after(self.image_update_val, self.frame_update)
        except:
            self.imagepanel.after(self.image_update_val, self.frame_update)

    # Setting the images to be displayed
    def set_image(self, file_path):
        self.file_path=file_path
        # list all the jpg and png images in the folder
        self.image_list = os.listdir(self.file_path)
        self.image_list = [x for x in self.image_list if x.endswith(".jpg") or x.endswith(".png")]

        self.cur_image_path = os.path.join(self.file_path,self.image_list[0])
        self.cur_image_index = 0

    # When the number keys are pressed
    def num_key_press(self, event):
        try:
            self.frame_file_name = os.path.join(".","data",controllerframe.labelling_main_class,app.sub_class_list[int(event.char)-1],self.image_list[self.cur_image_index].split(".")[0]+'.png')
            # Check if the file exists: If not save the frame
            if not os.path.isfile(self.frame_file_name):
                cv2.imwrite(self.frame_file_name, self.OCV_image)
                print("Save succesful:",self.frame_file_name)
            if self.cur_image_index < len(self.image_list)-1:
                self.cur_image_index += 1
                self.cur_image_path = os.path.join(self.file_path,self.image_list[self.cur_image_index])
        except:
             print("Select a batch of images first")
    
    # When the right arrow key is pressed: Display the next image
    def right_key_press(self, event):
        # Ensure that there are more images to be displayed
        if self.cur_image_index < len(self.image_list)-1:
            self.cur_image_index += 1
            self.cur_image_path = os.path.join(self.file_path,self.image_list[self.cur_image_index])
    
    # When the left arrow key is pressed: Display the previous image
    def left_key_press(self, event):
        # Ensure that there are more images to be displayed
        if self.cur_image_index > 0:
            self.cur_image_index -= 1
            self.cur_image_path = os.path.join(self.file_path,self.image_list[self.cur_image_index])

        
# When playing the video: The timer class (Used to exit the thread without errors)
class ttkTimer(threading.Thread):
    """a class serving same function as wxTimer... but there may be better ways to do this
    """
    def __init__(self, callback, tick):
        threading.Thread.__init__(self)
        self.callback = callback
        self.stopFlag = threading.Event()
        self.tick = tick
        self.iters = 0

    def run(self):
        while not self.stopFlag.wait(self.tick):
            self.iters += 1
            self.callback()

    def stop(self):
        self.stopFlag.set()

    def get(self):
        return self.iters

# Video player class
class video_player(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.play_pause_stop = 2
        self.def_speed = 15
        self.video_speed_val = self.def_speed
        self.OCV_video = cv2.VideoCapture(os.path.join(".","assets","myvid.mp4"))

        videoplayers = ttk.Frame(self)
        
        # The control panel 1 which includes Pause/Play/Stop buttons
        self.PPSpanel = ttk.Frame(videoplayers)
        self.pause = ttk.Button(self.PPSpanel, text="Pause", command=self.OnPause).pack(side=tk.LEFT)
        self.play = ttk.Button(self.PPSpanel, text="Play", command=self.OnPlay).pack(side=tk.LEFT)
        self.stop = ttk.Button(self.PPSpanel, text="Stop", command=self.OnStop).pack(side=tk.LEFT)
        self.PPSpanel.pack(side=tk.BOTTOM)

        # Control panel 2 which includes the slider for the video
        self.videoslider= ttk.Frame(videoplayers)
        self.scale_var = tk.DoubleVar()
        self.timeslider_last_val = ""
        self.timeslider = tk.Scale(self.videoslider, variable=self.scale_var, command=self.scale_sel,
                from_=0, to=1000, orient=tk.HORIZONTAL, length=700, showvalue=0)
        self.timeslider.pack(side=tk.BOTTOM, fill=tk.X, expand=1)
        self.timeslider_last_update = time.time()
        self.videoslider.pack(side=tk.BOTTOM, fill=tk.X)


        # The video Tkinter frame
        self.videopanel = ttk.Frame(videoplayers)
        self.videolabel = ttk.Label(self.videopanel)
        self.videolabel.pack(fill=tk.BOTH,expand=1)
        self.videopanel.pack(side=tk.BOTTOM,fill=tk.BOTH, expand=1, padx=[0,10])

        
        videoplayers.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)


        # The side frame which include the video playback speed and the help button
        self.side_tab = ttk.Frame(self)
        
        # Help button
        self.help_btn = tk.Button(self.side_tab, text="Help", font='sans 10 bold', height=2, width=12, background="#343434", foreground="white", command = self.help_btn_browser)
        self.help_btn.pack(side=tk.BOTTOM,expand=1, padx=[10,0], pady=[10,50])
        
        
        # The logos
        # The logo is created using the icons from https://www.flaticon.com/free-icons/schedule and https://www.flaticon.com/free-icons/professions-and-jobs
        PixelMe_logo = ImageTk.PhotoImage(Image.open(os.path.join(".","assets","PixelMe.png")).resize((100,82), Image.Resampling.LANCZOS))
        PixelMe_logo_label = ttk.Label(self.side_tab, image=PixelMe_logo)
        PixelMe_logo_label.image = PixelMe_logo
        PixelMe_logo_label.pack(side=tk.BOTTOM,expand=1, padx=[10,0], pady=[0,20])
        
        # Video playback speed slider
        self.video_speed = tk.Scale(self.side_tab,from_=1, to=6, orient=tk.HORIZONTAL, command=self.update_video_speed)
        self.video_speed.pack(side=tk.BOTTOM,expand=1, pady=[0,40])
        
        self.video_speed_label = ttk.Label(self.side_tab, text="Video Speed")
        self.video_speed_label.pack(side=tk.BOTTOM,expand=1)
        
        self.side_tab.pack(side=tk.BOTTOM)

        self.frame_update()
        self.timer = ttkTimer(self.OnTimer, 1.0)
        self.timer.start()
        self.update()

        self.grid(column=2, row=0, columnspan=5, rowspan = 4, padx=5, pady=5, sticky='s')

        for i in range(1,len(app.sub_class_list)+1):
                app.bind(str(i), self.num_key_press)
        app.bind("<space>", self.space_key_press)
        app.bind("<Right>", self.right_key_press)
        app.bind("<Left>", self.left_key_press)
    
    # When the pause key is pressed
    def OnPause(self):
        """Pause the player.
        """
        self.play_pause_stop = 1

    # When the play button is pressed
    def OnPlay(self):
        self.play_pause_stop = 0

    # When the stop is hit, stop the video
    def OnStop(self):
        """Stop the player.
        """
        self.play_pause_stop = 2
        self.OCV_video.set(cv2.CAP_PROP_POS_MSEC,0)
        # reset the time slider
        self.timeslider.set(0)

    # Updating the video when the slider is moved
    def scale_sel(self, evt):
        if self.OCV_video == None:
            return
        nval = self.scale_var.get()
        sval = str(nval)
        if self.timeslider_last_val != sval:
            # this is a hack. The timer updates the time slider.
            # This change causes this rtn (the 'slider has changed' rtn) to be invoked.
            # I can't tell the difference between when the user has manually moved the slider and when
            # the timer changed the slider. But when the user moves the slider tkinter only notifies
            # this rtn about once per second and when the slider has quit moving.
            # Also, the tkinter notification value has no fractional seconds.
            # The timer update rtn saves off the last update value (rounded to integer seconds) in timeslider_last_val
            # if the notification time (sval) is the same as the last saved time timeslider_last_val then
            # we know that this notification is due to the timer changing the slider.
            # otherwise the notification is due to the user changing the slider.
            # if the user is changing the slider then I have the timer routine wait for at least
            # 2 seconds before it starts updating the slider again (so the timer doesn't start fighting with the
            # user)
            self.timeslider_last_update = time.time()
            mval = "%.0f" % (nval * 1000)
            self.OCV_video.set(cv2.CAP_PROP_POS_MSEC, int(mval))

    def help_btn_browser(self):
        # webbrowser.open(r"https://www.google.com",autoraise=True)
        pass

    def update_video_speed(self, event):
        self.video_speed_val = int(self.def_speed/self.video_speed.get())

    def frame_update(self):
        try:
            if not self.play_pause_stop == 1:
                ret, self.cur_frame_img = self.OCV_video.read()
                if ret:
                    cv2image= cv2.cvtColor(self.cur_frame_img, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(cv2image)
                    imgtk = ImageTk.PhotoImage(image = img.resize((720,540), Image.Resampling.LANCZOS))
                    self.videolabel.imgtk = imgtk
                    self.videolabel.configure(image=imgtk)
                if self.play_pause_stop ==2:
                    self.play_pause_stop = 1
            self.videopanel.after(self.video_speed_val, self.frame_update)
        except:
            self.videopanel.after(self.video_speed_val, self.frame_update)
    
    # Updating the slider based on the video
    def OnTimer(self):
        """Update the time slider according to the current movie time.
        """
        if self.OCV_video == None:
             return
        # since the self.player.get_length can change while playing,
        # re-set the timeslider to the correct range.
        try:
            length = self.OCV_video.get(cv2.CAP_PROP_FRAME_COUNT)/self.OCV_video.get(cv2.CAP_PROP_FPS)
        except:
            length = self.OCV_video.get(cv2.CAP_PROP_FRAME_COUNT)/30
        
        dbl = length #* 0.001
        self.timeslider.config(to=dbl)

        # update the time on the slider
        tyme = self.OCV_video.get(cv2.CAP_PROP_POS_MSEC)
        if tyme == -1:
            tyme = 0
        dbl = tyme * 0.001
        self.timeslider_last_val = ("%.0f" % dbl) + ".0"
        # don't want to programatically change slider while user is messing with it.
        # wait 2 seconds after user lets go of slider
        if time.time() > (self.timeslider_last_update + 2.0):
            self.timeslider.set(dbl)
    
    # When the number keys are pressed
    def num_key_press(self, event):
        self.play_pause_stop = 1 #Pause video
        self.cur_frame_no = int(self.OCV_video.get(cv2.CAP_PROP_POS_MSEC)*self.OCV_video.get(cv2.CAP_PROP_FPS)/1000)
        try:
            self.frame_file_name = os.path.join(".","data",controllerframe.labelling_main_class,app.sub_class_list[int(event.char)-1],os.path.splitext(os.path.basename(self.file_path))[0]+'_f_'+str(self.cur_frame_no)+'.png')
            # Check if the file exists: If not save the frame
            if not os.path.isfile(self.frame_file_name):
                cv2.imwrite(self.frame_file_name, self.cur_frame_img)
                print("Save succesful:",self.frame_file_name)
        except:
             print("Play a video to start annotating")
        self.play_pause_stop = 0 #Play video
    
    # When the space key is pressed: Play/Pause video
    def space_key_press(self, event):
        if self.play_pause_stop == 0:
            self.play_pause_stop = 1
        else:
            self.play_pause_stop = 0
    
    # When the right arrow key is pressed: Forward 10 seconds
    def right_key_press(self, event):
        # Ensure that the video is not forwarded beyond the video length
        if ((self.OCV_video.get(cv2.CAP_PROP_FRAME_COUNT)*1000/self.OCV_video.get(cv2.CAP_PROP_FPS))-self.OCV_video.get(cv2.CAP_PROP_POS_MSEC))>10000:
            self.OCV_video.set(cv2.CAP_PROP_POS_MSEC, self.OCV_video.get(cv2.CAP_PROP_POS_MSEC)+10000)
    
    # When the left arrow key is pressed: Rewind 10 seconds
    def left_key_press(self, event):
        # Ensure that the video is not rewinded beyond the video length
        if self.OCV_video.get(cv2.CAP_PROP_POS_MSEC) > 10000:
            self.OCV_video.set(cv2.CAP_PROP_POS_MSEC, self.OCV_video.get(cv2.CAP_PROP_POS_MSEC)-10000)
    
    # Setting the video to be played
    def set_video(self, file_path):
        self.file_path=file_path
        try:
            self.OCV_video.release()
            cv2.destroyAllWindows()
        except:
            pass
        
        self.OCV_video = cv2.VideoCapture(self.file_path)
        self.play_pause_stop = 0
        self.video_speed_val = self.def_speed
        self.video_speed.set(1)

# Class for the main window
class ControlFrame(ttk.Frame):
    def __init__(self, container):
            super().__init__(container)
            # self['text'] = 'Options'
            self.labelling_main_class = app.main_class_list
            self.file_path = ""
            self.load_btn = tk.Button(self, text="Load Dataset", font='sans 10 bold', height=2, width=12, background="#343434", foreground="white",  command=self.load_data)
            self.load_btn.grid(column=0, row=0, rowspan=2, columnspan=2, padx=(30,30), pady=20, sticky='w')
            
            self.selected_variable = tk.StringVar(None, '1')

            self.sub_class_variables = [(str(i+1)+" - "+class_obj, str(i+1)) for i, class_obj in enumerate(app.sub_class_list)]

            # Add a list of the sub classes as radio buttons
            # Note: The radio buttons do not have a callback function
            radio_colnum,radio_rownum=0,2
            for data_param_variable in self.sub_class_variables:
                ttk.Radiobutton(self,
                                text=data_param_variable[0],
                                value=data_param_variable[1],
                                variable= self.selected_variable).grid(column=radio_colnum, row=radio_rownum, padx=20, pady=10, sticky='ew')
                radio_rownum+=1
            
            if args.vid:
                self.video_player_frame = video_player(container)
            else:
                self.image_player_frame = image_player(container)
            # self.video_player_frame = video_player(container)
            
            self.grid(column=0, row=0, padx=5, pady=5, sticky='ew')
    
    # Function to load the data
    def load_data(self):
        if args.vid:
            self.file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4"),("Video files", "*.avi")])
            if self.file_path:
                self.video_player_frame.set_video(self.file_path)
        else:
            self.file_path = filedialog.askdirectory()
            if self.file_path:
                if len([x for x in os.listdir(self.file_path) if x.endswith(".jpg") or x.endswith(".png")]) > 0:
                    self.image_player_frame.set_image(self.file_path)
                else:
                    print("No images found in the selected directory")

# App class
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PixelMe Labelling Tool")
        self.geometry("1120x650+10+10")
        # self.resizable(False, False)
        # The logo is created using the icons from https://www.flaticon.com/free-icons/schedule and https://www.flaticon.com/free-icons/professions-and-jobs
        self.PixelMe_icon = ImageTk.PhotoImage(Image.open(os.path.join(".","assets","PixelMe.png")).resize((80,80), Image.Resampling.LANCZOS))
        self.iconphoto(False, self.PixelMe_icon)
        self.protocol("WM_DELETE_WINDOW",self.on_closing)

        self.main_class_list = args.main_class
        if len(args.sub_class) == 1:
            self.sub_class_list = args.sub_class[0].split(",")
        else:
            self.sub_class_list = args.sub_class
        self.sub_class_list = [scl.lower() for scl in self.sub_class_list]
        
        for sub_c in self.sub_class_list:
            os.makedirs(os.path.join(".","data",args.main_class,sub_c), exist_ok=True)
    
    # Function to close the app
    def on_closing(self):
        if messagebox.askokcancel("Quit","Are you sure?"):
            #exit_event.set()
            self.quit()
            self.destroy()
            os._exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PixelMe Labelling Tool supports image and video labelling for object classification\
                        Example: python PixelMe.py -mc cars -sc toyota lexus honda -v')
    parser.add_argument('-mc', '--main_class', type=str,
                        help='The main class you want to label. Example: cars', required = True)
    parser.add_argument('-sc', '--sub_class', nargs='+',
                        help='The subclasses you want to label.\
                        Example: if you have "--main_class cars" then enter --sub_class toyota lexus honda', required = True)
    parser.add_argument('-v', '--vid', action='store_true', help='If the labelling is to be done on a video. If not set then it allows you to label images')
    

    args = parser.parse_args()
    app = App()
    controllerframe = ControlFrame(app)
    app.mainloop()
