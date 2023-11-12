#AI Python assistant

import pprint
import google.generativeai as palm

import tkinter as tk
import tkinter.messagebox as tkm
import customtkinter as ctk

import config

import os

palm.configure(api_key = config.palm2_key)

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

ctk.set_appearance_mode("system")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green



class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Title and geometry
        self.title("CodebloomAI")
        self.geometry("1040x620")

        # Setting grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  CodebloomAI",
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Boom",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.history_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="History",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.history_button_event)
        self.history_button.grid(row=2, column=0, sticky="ew")

        self.tweak_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Tweak",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.tweak_button_event)
        self.tweak_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # Home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        # Command line and button
        self.entry = ctk.CTkEntry(self.home_frame, placeholder_text="Enter request here")
        self.entry.grid(row=3, column=0, columnspan=3, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = ctk.CTkButton(master=self.home_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Bloom",
                                           command=self.generate_button_event)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Input textbox and header
        self.in_textbox_label = ctk.CTkLabel(self.home_frame, text="Your code",
                                                             anchor="w", font=ctk.CTkFont(size=15, weight="bold"))
        self.in_textbox_label.grid(row=0, column=0)
        
        self.in_textbox = ctk.CTkTextbox(self.home_frame, width=400, height=500)
        self.in_textbox.grid(row=1, column=0, columnspan=2, padx=(20, 0), pady=(0, 20)) 

        # Output textbox and header
        self.out_textbox_label = ctk.CTkLabel(self.home_frame, text="Codebloom code",
                                                             anchor="w", compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.out_textbox_label.grid(row=0, column=2)
        
        self.out_textbox = ctk.CTkTextbox(self.home_frame, width=400, height=500)
        self.out_textbox.grid(row=1, column=2, columnspan=2, padx=(20, 20), pady=(0, 20))

        # create second frame
        self.history_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.tweak_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")


    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.history_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.tweak_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.history_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.history_frame.grid_forget()
        if name == "frame_3":
            self.tweak_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.tweak_frame.grid_forget()
    

    def home_button_event(self):
        self.select_frame_by_name("home")

    def history_button_event(self):
        self.select_frame_by_name("frame_2")

    def tweak_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)


    # Home AI function
    def generate_button_event(self):
        
        current_path = os.path.dirname(os.path.realpath(__file__))

        # Get default context
        context_file = open(current_path + "/ai-files/default-context.txt", "r")
        context = context_file.read().strip()
        
        # Open history file
        history_file = open(current_path + "/ai-files/history.txt", "a+")

        # Set text box
        self.out_textbox.delete("1.0","end")

        user_code = self.in_textbox.get("1.0","end")
        command = self.entry.get()
        
        # prompt
        prompt = f"{context}\n'usercode':{user_code} \n'command':{command}"
        
        # Run AI
        completion = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=0,
            # The maximum length of the response
            max_output_tokens=800,
        )
        self.out_textbox.insert(ctk.END, completion.result)
        self.out_textbox.see(ctk.END)  

        # save to history
        history_file.write(f"Command: {command}\n\n")
        history_file.write(f"In Code:\n{user_code}\n\n")
        history_file.write(f"Out Code:\n{completion.result}\n\n----------------------------------------------------------------\n\n")

        # close files
        context_file.close()
        history_file.close()
        

        



if __name__ == "__main__":
    app = App()
    app.mainloop()





