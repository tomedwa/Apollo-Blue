import tkinter
import tkinter.messagebox
import customtkinter
import threading

customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "dark-blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Apollo Blue")
        self.geometry(f"{950}x{580}")
        self.minsize(950, 580)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Apollo Blue",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event, text="Option 1"
        )
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event, text="Option 2"
        )
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame, command=self.sidebar_button_event, text="Option 3"
        )
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w"
        )
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w"
        )
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
        )
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(
            row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew"
        )

        self.main_button_1 = customtkinter.CTkButton(
            master=self,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
        )
        self.main_button_1.grid(
            row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )

        # Frame for keybinding
        self.frame_keybinding = customtkinter.CTkFrame(self)
        self.frame_keybinding.grid(
            row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )

        self.label_binding_gesture_title = customtkinter.CTkLabel(
            master=self.frame_keybinding, padx=20, pady=20, text="Gesture"
        )
        self.label_binding_gesture_title.grid(row=0, column=0, sticky="")

        self.label_binding_current_title = customtkinter.CTkLabel(
            master=self.frame_keybinding, padx=20, pady=20, text="Curent Binding"
        )
        self.label_binding_current_title.grid(row=0, column=1, sticky="")

        self.label_binding_set_title = customtkinter.CTkLabel(
            master=self.frame_keybinding, padx=20, pady=20, text="Set Binding"
        )
        self.label_binding_set_title.grid(row=0, column=2, sticky="")

        self.label_left_bind = customtkinter.CTkLabel(
            master=self.frame_keybinding, padx=20, pady=20, text="Left Swipe"
        )
        self.label_left_bind.grid(row=1, column=0, sticky="")

        self.label_left_current = customtkinter.CTkLabel(
            master=self.frame_keybinding, padx=20, pady=20, text="none"
        )
        self.label_left_current.grid(row=1, column=1, sticky="")
        self.label_left_current.configure(text="none")

        self.entry_left_set_binding = customtkinter.CTkEntry(
            self.frame_keybinding, placeholder_text="Enter new binding"
        )
        self.entry_left_set_binding.grid(row=1, column=2, sticky="")

        self.button_confirm_left = customtkinter.CTkButton(
            master=self.frame_keybinding,
            text="Set",
            command=lambda: self.set_new_keybinding(
                "left", self.entry_left_set_binding.get()
            ),
        )
        self.button_confirm_left.grid(row=1, column=3, padx=20, pady=20, sticky="")

        self.label_right_bind = customtkinter.CTkLabel(
            master=self.frame_keybinding, padx=20, pady=20, text="Right Swipe"
        )
        self.label_right_bind.grid(row=2, column=0, sticky="")

        self.label_right_current = customtkinter.CTkLabel(
            master=self.frame_keybinding, padx=20, pady=20, text="none"
        )
        self.label_right_current.grid(row=2, column=1, sticky="")

        self.entry_right_set_binding = customtkinter.CTkEntry(
            self.frame_keybinding, placeholder_text="Enter new binding"
        )
        self.entry_right_set_binding.grid(row=2, column=2, sticky="")

        self.button_confirm_right = customtkinter.CTkButton(
            master=self.frame_keybinding,
            text="Set",
            command=lambda: self.set_new_keybinding(
                "right", self.entry_right_set_binding.get()
            ),
        )
        self.button_confirm_right.grid(row=2, column=3, padx=20, pady=20, sticky="")

        self.label_up_bind = customtkinter.CTkLabel(
            master=self.frame_keybinding, padx=20, pady=20, text="Up Swipe"
        )
        self.label_up_bind.grid(row=3, column=0, sticky="")

        self.label_up_current = customtkinter.CTkLabel(
            master=self.frame_keybinding, padx=20, pady=20, text="none"
        )
        self.label_up_current.grid(row=3, column=1, sticky="")

        self.entry_up_set_binding = customtkinter.CTkEntry(
            self.frame_keybinding, placeholder_text="Enter new binding"
        )
        self.entry_up_set_binding.grid(row=3, column=2, sticky="")

        self.button_confirm_up = customtkinter.CTkButton(
            master=self.frame_keybinding,
            text="Set",
            command=lambda: self.set_new_keybinding(
                "up", self.entry_up_set_binding.get()
            ),
        )
        self.button_confirm_up.grid(row=3, column=3, padx=20, pady=20, sticky="")

        self.label_down_bind = customtkinter.CTkLabel(
            master=self.frame_keybinding, padx=20, pady=20, text="Down Swipe"
        )
        self.label_down_bind.grid(row=4, column=0, sticky="")

        self.label_down_current = customtkinter.CTkLabel(
            master=self.frame_keybinding, padx=20, pady=20, text="none"
        )
        self.label_down_current.grid(row=4, column=1, sticky="")

        self.entry_down_set_binding = customtkinter.CTkEntry(
            self.frame_keybinding, placeholder_text="Enter new binding"
        )
        self.entry_down_set_binding.grid(row=4, column=2, sticky="")

        self.button_confirm_down = customtkinter.CTkButton(
            master=self.frame_keybinding,
            text="Set",
            command=lambda: self.set_new_keybinding(
                "down", self.entry_down_set_binding.get()
            ),
        )
        self.button_confirm_down.grid(row=4, column=3, padx=20, pady=20, sticky="")

        self.label_r_left_bind = customtkinter.CTkLabel(
            master=self.frame_keybinding, padx=20, pady=20, text="Rotate Left"
        )
        self.label_r_left_bind.grid(row=5, column=0, sticky="")

        self.label_r_left_current = customtkinter.CTkLabel(
            master=self.frame_keybinding, padx=20, pady=20, text="none"
        )
        self.label_r_left_current.grid(row=5, column=1, sticky="")

        self.entry_r_left_set_binding = customtkinter.CTkEntry(
            self.frame_keybinding, placeholder_text="Enter new binding"
        )
        self.entry_r_left_set_binding.grid(row=5, column=2, sticky="")

        self.button_confirm_r_left = customtkinter.CTkButton(
            master=self.frame_keybinding,
            text="Set",
            command=lambda: self.set_new_keybinding(
                "r_left", self.entry_r_left_set_binding.get()
            ),
        )
        self.button_confirm_r_left.grid(row=5, column=3, padx=20, pady=20, sticky="")

        self.label_r_right_bind = customtkinter.CTkLabel(
            master=self.frame_keybinding, padx=20, pady=20, text="Rotate Right"
        )
        self.label_r_right_bind.grid(row=6, column=0, sticky="")

        self.label_r_right_current = customtkinter.CTkLabel(
            master=self.frame_keybinding, padx=20, pady=20, text="none"
        )
        self.label_r_right_current.grid(row=6, column=1, sticky="")

        self.entry_r_right_set_binding = customtkinter.CTkEntry(
            self.frame_keybinding, placeholder_text="Enter new binding"
        )
        self.entry_r_right_set_binding.grid(row=6, column=2, sticky="")

        self.button_confirm_r_right = customtkinter.CTkButton(
            master=self.frame_keybinding,
            text="Set",
            command=lambda: self.set_new_keybinding(
                "r_right", self.entry_r_right_set_binding.get()
            ),
        )
        self.button_confirm_r_right.grid(row=6, column=3, padx=20, pady=20, sticky="")

        # Toggle Gestures Frame
        self.frame_toggle_gestures = customtkinter.CTkFrame(self)
        self.frame_toggle_gestures.grid(
            row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew"
        )
        self.label_test_group = customtkinter.CTkLabel(
            master=self.frame_toggle_gestures, text="Toggle Gestures"
        )
        self.label_test_group.grid(
            row=0, column=0, columnspan=1, padx=10, pady=10, sticky=""
        )

        switch_swipe_left = customtkinter.CTkSwitch(
            master=self.frame_toggle_gestures, text="Swipe Left"
        )
        switch_swipe_left.grid(row=1, column=0, padx=10, pady=(0, 20), sticky="w")

        switch_swipe_right = customtkinter.CTkSwitch(
            master=self.frame_toggle_gestures, text="Swipe Right"
        )
        switch_swipe_right.grid(row=2, column=0, padx=10, pady=(0, 20), sticky="w")

        switch_swipe_up = customtkinter.CTkSwitch(
            master=self.frame_toggle_gestures, text="Swipe Up"
        )
        switch_swipe_up.grid(row=3, column=0, padx=10, pady=(0, 20), sticky="w")

        switch_swipe_down = customtkinter.CTkSwitch(
            master=self.frame_toggle_gestures, text="Swipe Down"
        )
        switch_swipe_down.grid(row=4, column=0, padx=10, pady=(0, 20), sticky="w")

        switch_r_left = customtkinter.CTkSwitch(
            master=self.frame_toggle_gestures, text="Rotate Left"
        )
        switch_r_left.grid(row=5, column=0, padx=10, pady=(0, 20), sticky="w")

        switch_r_right = customtkinter.CTkSwitch(
            master=self.frame_toggle_gestures, text="Rotate Right"
        )
        switch_r_right.grid(row=6, column=0, padx=10, pady=(0, 20), sticky="w")

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(
            text="Type in a number:", title="CTkInputDialog"
        )
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def keypress(self, keyname: str):
        print(keyname)

    def set_new_keybinding(self, gesture: str, binding: str):
        if gesture == "left":
            self.label_left_current.configure(text=binding)
        elif gesture == "right":
            self.label_right_current.configure(text=binding)
        elif gesture == "up":
            self.label_up_current.configure(text=binding)
        elif gesture == "down":
            self.label_down_current.configure(text=binding)
        elif gesture == "r_left":
            self.label_r_left_current.configure(text=binding)
        elif gesture == "r_right":
            self.label_r_right_current.configure(text=binding)


def thread_test():
    import time

    while True:
        print("test")
        time.sleep(1)


if __name__ == "__main__":
    app = App()

    test_thread = threading.Thread(target=thread_test)
    test_thread.daemon = True
    test_thread.start()

    app.mainloop()
