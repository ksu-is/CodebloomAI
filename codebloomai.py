# AI Python assistant

import pprint
import google.generativeai as palm

import tkinter as tk
import tkinter.messagebox as tkm
import customtkinter as ctk

import config

import os

import datetime

import pyperclip

palm.configure(api_key = config.palm2_key)

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

ctk.set_appearance_mode("system")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green



class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # title and geometry
        self.title("CodebloomAI")
        self.geometry("1040x620")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ### navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        # nav title
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="CodebloomAI",
                                                    compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        # nav page Bloom
        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Bloom",
                                            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                            anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")
        # nav page History
        self.history_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="History",
                                            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                            anchor="w", command=self.history_button_event)
        self.history_button.grid(row=2, column=0, sticky="ew")
        # nav page Tweak
        self.tweak_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Tweak",
                                            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                            anchor="w", command=self.tweak_button_event)
        self.tweak_button.grid(row=3, column=0, sticky="ew")
        # nav page select appearence
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        ### home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        ## input heading frame
        self.in_head_frame = ctk.CTkFrame(self.home_frame, width=400, height=20, fg_color="transparent")
        self.in_head_frame.grid(row=0, column=0, padx=(20,10), pady=5)
        # in head label
        self.in_textbox_label = ctk.CTkLabel(self.in_head_frame, text="Code In",
                                                anchor="w", width=340, font=ctk.CTkFont(size=15, weight="bold"))
        self.in_textbox_label.grid(row=0, column=0)
        # in head delete button
        self.in_delete_button = ctk.CTkButton(master=self.in_head_frame, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), text="🗑",
                                                width=10, command=self.in_delete_button_event)
        self.in_delete_button.grid(row=0, column=1)
        # in head out-to-in swap button
        self.oti_swap_button = ctk.CTkButton(master=self.in_head_frame, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), text="↶",
                                                width=10, command=self.swap_button_event)
        self.oti_swap_button.grid(row=0, column=2)

        ## output heading frame
        self.out_head_frame = ctk.CTkFrame(self.home_frame, width=400, height=20, fg_color="transparent")
        self.out_head_frame.grid(row=0, column=1, padx=(10,20), pady=5)
        # out head label
        self.out_textbox_label = ctk.CTkLabel(self.out_head_frame, text="Code Out",
                                                anchor="w", width=350, font=ctk.CTkFont(size=15, weight="bold"))
        self.out_textbox_label.grid(row=0, column=0)
        # out head copy button
        self.out_copy_button = ctk.CTkButton(master=self.out_head_frame, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), text="📋",
                                                width=10, command=self.out_copy_button_event)
        self.out_copy_button.grid(row=0, column=1)

        # input textbox
        self.in_textbox = ctk.CTkTextbox(self.home_frame, width=400, height=515)
        self.in_textbox.grid(row=1, column=0, padx=(20, 10), sticky="nsew") 

        # output textbox
        self.out_textbox = ctk.CTkTextbox(self.home_frame, width=400, height=515)
        self.out_textbox.grid(row=1, column=1, padx=(10, 20), sticky="nsew")

        ## command area frame
        self.command_frame = ctk.CTkFrame(self.home_frame, width=820, fg_color="transparent")
        self.command_frame.grid(row=3, column=0, columnspan=2, padx=(20,20), pady=(20,20), sticky="nsew")
        # command line
        self.entry = ctk.CTkEntry(self.command_frame, placeholder_text="Command", width=650)
        self.entry.grid(row=0, column=0, padx=(0,10))
        # command button
        self.command_button = ctk.CTkButton(master=self.command_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Bloom",
                                           width=150, command=self.generate_button_event)
        self.command_button.grid(row=0, column=1 ,padx=(10,0))


        ### history frame    
        self.history_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        ## history header frame
        self.history_head_frame = ctk.CTkFrame(self.history_frame, width=810, height=20, fg_color="transparent")
        self.history_head_frame.grid(row=0, column=0, padx=20, pady=5, sticky="nsew")
        # history label
        self.history_label = ctk.CTkLabel(self.history_head_frame, text="History log",
                                                anchor="w", width=790, font=ctk.CTkFont(size=15, weight="bold"))
        self.history_label.grid(row=0, column=0)
        # history clear button
        self.history_clear_button = ctk.CTkButton(master=self.history_head_frame, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), text="🗑",
                                                width=10, command=self.history_clear_button_event)
        self.history_clear_button.grid(row=0, column=1)
        
        # history textbox
        self.history_log_textbox = ctk.CTkTextbox(self.history_frame, width=810, height=565)
        self.history_log_textbox.grid(row=1, column=0, padx=20, sticky="nsew")

        ### tweak frame
        self.tweak_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")


    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.history_button.configure(fg_color=("gray75", "gray25") if name == "history" else "transparent")
        self.tweak_button.configure(fg_color=("gray75", "gray25") if name == "tweak" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "history":
            self.history_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.history_frame.grid_forget()
        if name == "tweak":
            self.tweak_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.tweak_frame.grid_forget()
    
    # frame select functions
    def home_button_event(self):
        self.select_frame_by_name("home")

    def history_button_event(self):
        self.select_frame_by_name("history")
        self.show_history()

    def tweak_button_event(self):
        self.select_frame_by_name("tweak")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)


    # home AI function
    def generate_button_event(self):
        
        current_path = os.path.dirname(os.path.realpath(__file__))

        # get default context
        context_file = open(current_path + "/ai-files/default-context.txt", "r")
        context = context_file.read().strip()
        
        # open history file
        history_file = open(current_path + "/ai-files/history.txt", "a+")

        # set text box
        self.out_textbox.delete("1.0","end")

        # get data
        user_code = self.in_textbox.get("1.0","end")
        command = self.entry.get()
        
        # prompt
        prompt = f"{context}\n'usercode':{user_code} \n'command':{command}"
        
        # run AI
        completion = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=0,
            # maximum length of the response
            max_output_tokens=800,
        )
        self.out_textbox.insert(ctk.END, completion.result)
        self.out_textbox.see(ctk.END)  

        # save to history
        history_file.write(f"Command: {command}\n\n")
        history_file.write(f"In Code:\n{user_code}\n\n")
        history_file.write(f"Out Code:\n{completion.result}\n\n")
        history_file.write(f"{datetime.datetime.now()}\n")
        history_file.write("_"*128+"\n\n")
        
        # close files
        context_file.close()
        history_file.close()
    
    # home swap output to in
    def swap_button_event(self):
        data=self.out_textbox.get("1.0","end")
        if data.isspace():
            pass
        else:
            self.in_textbox.delete("1.0","end")
            self.in_textbox.insert(ctk.END,data)

    # home delete input
    def in_delete_button_event(self):
        self.in_textbox.delete("1.0","end")
    
    # home copy output 
    def out_copy_button_event(self):
        global data
        self.out_textbox.tag_add("sel", "1.0", "end")
        data=self.out_textbox.selection_get()
        pyperclip.copy(data)
    
    # show history func
    def show_history(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        
        self.history_log_textbox.delete("1.0","end")

        history_file = open(current_path + "/ai-files/history.txt", "r")
        history = history_file.read().strip()
        self.history_log_textbox.insert(ctk.END,history)
        
        history_file.close()

    # clear history func
    def history_clear_button_event(self):
        ## create confirmation pop-up
        self.confirm = ctk.CTkToplevel(self)
        self.confirm.title("Clear History")

        self.confirm.attributes("-topmost", True)

        # confirmation labels
        confirm_label = ctk.CTkLabel(self.confirm, text="Are you sure you want to clear your history?")
        confirm_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20,0))
        
        confirm_sublabel = ctk.CTkLabel(self.confirm, text="This action cannot be undone.")
        confirm_sublabel.grid(row=1, column=0, columnspan=2, padx=20, pady=(0,10))

        # buttons
        clear_decline_button = ctk.CTkButton(master=self.confirm, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"), text="Nevermind",
                                                width=10, command=self.confirm.destroy)
        clear_decline_button.grid(row=2, column=0, pady=(0,20))

        self.clear_accept_button = ctk.CTkButton(master=self.confirm, fg_color="#36719F", border_width=1, text_color=("white", "#DCE4EE"), text="Clear",
                                                width=10, command=self.clear_history)
        self.clear_accept_button.grid(row=2, column=1, pady=(0,20))
        
    def clear_history(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        open(current_path + "/ai-files/history.txt", "w").close()
        self.history_log_textbox.delete("1.0","end")
        self.history_log_textbox.insert(ctk.END,"--History Cleared--")
        self.confirm.destroy()



        
        


if __name__ == "__main__":
    app = App()
    app.mainloop()





