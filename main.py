from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
import re
from kivymd.uix.button import MDFillRoundFlatButton  # Correct import
from plyer import filechooser


import mysql.connector


from kivy.clock import Clock
from kivymd.uix.card import MDCard

# KV layout definition
kv = '''
# Login screen layout
<MaterialTextInput>:
    name: "login"
    FloatLayout:
        Image:
            source: "green2.jpg"  # Image file for the background
            allow_stretch: True
            keep_ratio: False
        

        Image:
           
            id: profile_picture
            source: "42797457-removebg-preview.png"
            size_hint: None, None
            size: "80dp", "80dp"
            pos_hint: {"center_x":.5, "center_y": .93}
            allow_stretch: True
            radius: [60]
        MDTextButton:
            text: "User Login"
            size_hint: None, None
            size: "100dp", "50dp"
            pos_hint: {"center_x": .5, "center_y": .85}
        
 
        MDTextField:
            id: username_input
            hint_text: "Email or Phone Number"
            font_size: "20dp"
            icon_right: "email"
            size_hint_x: .85
            pos_hint: {"center_x": .5, "center_y": .65}
            mode: "round"
           
            error: False  # To control error highlighting
            hint_text_color_normal:0, 0, 0, 1
            hint_text_color_focus:0, 0, 0, 1
           
            helper_text_color: 0, 0, 0, 1
            error: False
            line_color_normal:  0, 0, 0, 1# White color for the line (RGBA format)
            line_color_focus:0, 0, 0, 1 # White color when focused (RGBA format)
 
 
        MDTextField:
            id: password_input
            hint_text: "Password"
            font_size: "20dp"
            icon_right: "lock"
            size_hint_x: .85
            pos_hint: {"center_x": .5, "center_y": .5}
            mode: "round"
            password: True
            hint_text_color_normal:0, 0, 0, 1
            hint_text_color_focus:0, 0, 0, 1
           
            
            line_color_normal:  0, 0, 0, 1# White color for the line (RGBA format)
            line_color_focus:0, 0, 0, 1 # White color when focused (RGBA format)
        BoxLayout:
            spacing: dp(-20)
            size_hint: .85, None
            pos_hint: {"center_x": .5, "center_y": .6}
            height: "30dp"
            MDLabel:
               
                size_hint: None, None
                size: dp(30), dp(30)
             
                 
            MDLabel:
                id:login_validation
                text: ""
 
                size_hint_y: None
                height: dp(30)
                theme_text_color: 'Custom'
                text_color:1,1,1,1
        BoxLayout:
            spacing: dp(-20)
            size_hint: .85, None
            pos_hint: {"center_x": .5, "center_y": .5}
            height: "30dp"
            MDLabel:
               
                size_hint: None, None
                size: dp(30), dp(30)
             
                 
            MDLabel:
                id:password_validation
                text: ""
 
                size_hint_y: None
                height: dp(30)
                theme_text_color: 'Custom'
                text_color:1,1,1,1
        BoxLayout:
            spacing: dp(-20)
            size_hint: .85, None
            pos_hint: {"center_x": .5, "center_y": .45}
            height: "30dp"
            MDLabel:
               
                size_hint: None, None
                size: dp(30), dp(30)
             
                 
            MDLabel:
                id:password_validation
                text: ""
 
                size_hint_y: None
                height: dp(30)
                theme_text_color: 'Custom'
                text_color:1,1,1,1
       
        BoxLayout:
            spacing: dp(5)
            size_hint: .85, None
            pos_hint: {"center_x": .5, "center_y": .38}
            height: "30dp"
            MDCheckbox:
                id: my_checkbox
                size_hint: None, None
                size: dp(30), dp(30)
                theme_text_color: "Custom"  # Allows custom color usage
                text_color: 1, 1, 1, 1      # Red color in RGBA format
                on_press:
                    password_input.password = not password_input.password
               
 
               
               
                 
            MDLabel:
                text: "Show password"
 
                size_hint_y: None
                height: dp(30)
                theme_text_color: 'Custom'
                text_color:1,1,1,1
               
 
        # Sign in and Sign up buttons
        BoxLayout:
            orientation: "horizontal"
            size_hint: .85, None
            height: "50dp"
            pos_hint: {"center_x": .5, "center_y": .3}
            spacing: dp(10)
 
            MDFlatButton:
                text: "SIGN IN"
                font_size: "22dp"
                on_release:
                    app.validation1()
                    app.password()
                    app.switch_to_dashboard()
                    app.dashboard()
                    app.switch_to_admin()
                md_bg_color:0.722, 0.525, 0.043, 1
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint: 0.45, None
                height: dp(50)
                line_color:0,0,0,1  
 
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "130dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.15}
 
            MDRaisedButton:
                text: "Create account"
                size_hint: None, None
                size: "100dp", "50dp"
                md_bg_color: 0, 0, 0, 0  # Transparent background for outlined button
                theme_text_color: "Custom"  # Ensure the text color is not overridden by the theme
                text_color: 1, 1, 1, 1  # White text color
                on_release: app.switch_to_registred()  # Action to perform on button press
                line_color:1,1,1,1  
        MDCard:
            id:login_error_card
            size_hint: None, None
            size: "250dp", "60dp" 
            pos_hint: {"center_x": 0.5, "center_y": .77}
           
            padding: "25dp"
            opacity:0
            
            MDLabel:
                id: login_error_input
                text: " "
                size_hint_y: None
                size_hint_x: None  # Disable the horizontal size hint to set a specific width
                width: dp(210)  # Set the width to 300 dp (adjust to your desired width)
                height: dp(30)
                theme_text_color: "Secondary"
                pos_hint: {"center_x": .5, "center_y": .77}
                color: 1, 0, 0, 1  # Red color for error messages
                halign: "center"  # Horizontal center alignment
                font_size: "16dp"

        
        
            
        MDLabel:
            id: login_
            text: "Not a member "
            size_hint_y: None
            size_hint_x: None  # Disable the horizontal size hint to set a specific width
            width: dp(210)  # Set the width to 300 dp (adjust to your desired width)
            height: dp(30)
            theme_text_color: "Secondary"
            pos_hint: {"center_x": .5, "center_y": .2}
            color: 1, 0, 0, 1  # Red color for error messages
            halign: "center"  # Horizontal center alignment
            font_size: "16dp"
 
        MDLabel:
            id: login_error_data
            text: " "
            size_hint_y: None
            height: dp(30)
            theme_text_color: "Secondary"
            pos_hint: {"center_x": .5, "center_y": .75}
            color: 1, 0, 0, 1  # Red color for error messages
            halign: "center"  # Horizontal center alignment
            valign: "middle"  # Vertical center alignment  
            font_size: "19dp"    
 
# Dashboard screen layout
<Dashboard>:
    name: "dashboard"
    FloatLayout:
    BoxLayout:
        canvas:
            Color:
                rgba: 1,1, 1, 1  # Blue color
            Rectangle:
                pos: self.pos
                size: self.size
    
    # Set the background color for the entire layout
    
        
    MDLabel:
        id: dashboard_id
        text: ""
        size_hint_y: None
        height: dp(30)
        font_size: "19dp"
        theme_text_color: "Secondary"
        color: 1, 0, 0, 1  # Red color for error messages
        halign: "center"  # Horizontal center alignment
        valign: "middle"  # Vertical center alignment
        pos_hint: {"center_x":.5, "center_y": .95}

    Image:
           
        id: profile_picture
        source: "home-icon-removebg-preview.png"
        size_hint: None, None
        size: "90dp", "90dp"
        pos_hint: {"center_x":.5, "center_y": .85}
        allow_stretch: True
        radius: [60]
    
    MDTopAppBar:
        size_hint_y: None
        height: "100dp"
        pos_hint: {"bottom": 1}
        md_bg_color:0.0, 0.392, 0.0 # A calm turquoise color for the navbar

    BoxLayout:
        orientation: "horizontal"
        size_hint: None, None
        size: "45dp", "90dp"
        pos_hint: {"right": 1, "bottom": 1}
        spacing: dp(25)
        MDCard:
            size_hint: None, None
            size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            radius: [50]
            padding: "5dp"
            md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
            line_color: 0, 0, 1, 1  # Black line color

            Image:
                id: profile_picture
                source: "gear-removebg-preview.png"
                size_hint: None, None
                size: "25dp", "45dp"
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                allow_stretch: True
                radius: [60]
                on_touch_down:app.switch_to_setting()

    BoxLayout:
        orientation: "horizontal"
        size_hint: None, None
        size: "110dp", "90dp"
        pos_hint: {"right": 1, "bottom": 1}
        spacing: dp(25)
        MDCard:
            size_hint: None, None
            size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            radius: [50]
            padding: "5dp"
            md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
            line_color: 0, 0, 1, 1

            Image:
                id: profile_picture
                source: "images-removebg-preview (1).png"
                size_hint: None, None
                size: "25dp", "35dp"  # Set the image size to match the card size
                pos_hint: {"center_x": 0.5, "center_y": 0.5} 
            
                on_touch_down: app.switch_to_withdraw(*args)

    BoxLayout:
        orientation: "horizontal"
        size_hint: None, None
        size: "175dp", "90dp"
        pos_hint: {"right": 1, "bottom": 1}
        spacing: dp(25)
        MDCard:
            size_hint: None, None
            size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            radius: [50]
            padding: "7dp"
            md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
            line_color: 0, 0, 1, 1 
            
            
            Image:
                source: "wallet.png"
                size_hint: None, None
                size: "20dp", "20dp"  # Set the image size to match the card size
                pos_hint: {"center_x": 0.5, "center_y": 0.5}  # Center the image within the card
                on_touch_down: app.switch_to_Wallet(*args)
    BoxLayout:
        orientation: "horizontal"
        size_hint: None, None
        size: "55dp", "25dp"
        pos_hint: {"right": 1, "bottom": 1}
        spacing: dp(25)

        MDLabel:
            text: "Settings"
            size_hint_y: None
            height: dp(20)
            font_size:"14sp"
            pos_hint: {"center_x": 0.65, "top": 1}
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

    BoxLayout:
        orientation: "horizontal"
        size_hint: None, None
        size: "120dp", "25dp"
        pos_hint: {"right": 1, "bottom": 1}
        

        MDLabel:
            text: "Withdraw"
            size_hint_y: None
            height: dp(20)
            font_size: "14sp"
            pos_hint: {"center_x": 0.65, "top": 1}
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

    BoxLayout:
        orientation: "horizontal"
        size_hint: None, None
        size: "175dp", "25dp"
        pos_hint: {"right": 1, "bottom": 1}

        MDLabel:
            text: "Wallet"
            size_hint_y: None
            height: dp(20)
            font_size: "14sp"
            pos_hint: {"center_x": 0.65, "top": 1}
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
    BoxLayout:
        orientation: "horizontal"
        size_hint: None, None
        size: "190dp", "90dp"  # Set the overall size of the BoxLayout container
        pos_hint: {"x": 0, "bottom": 1}  # Position BoxLayout at top-left corner
        spacing: dp(5)  # Set spacing between images
        MDCard:
            size_hint: None, None
            size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            radius: [50]
            padding: "5dp"
            md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
            line_color: 0, 0, 1, 1 

        # Second Image (Positioned beside the first image)
            Image:
                id: profile_picture_2
                source: "download__2_-removebg-preview.png"  # Path to your initial image (can be placeholder)
                size_hint: None, None
                size: "25dp", "25dp"  # Adjust size as needed
                pos_hint: {"center_x": 0.5, "center_y": 0.5}  # Center the image
                allow_stretch: True
                radius: [50]  # Rounded corners
                on_touch_down: app.on_image_touch_up(*args)   # On touch event, call the function

    BoxLayout:
        orientation: "horizontal"
        size_hint: None, None
        size: "175dp", "25dp"
        pos_hint: {"left": 1, "bottom": 1}

        MDLabel:
            text: "Profile"
            size_hint_y: None
            height: dp(20)
            font_size: "14sp"
            pos_hint: {"center_x": 0.65, "top": 1}
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1


            
    MDRaisedButton:
        text: "PHENOMENAL"
        size_hint: None, None
        size: "150dp", "100dp"
        pos_hint: {"center_x": 0.5, "center_y": 0.65}
        md_bg_color:0.5, 0.0, 0.5
        text_color:1.0, 0.8431, 0.0
        font_size: "24sp"

    BoxLayout:
        orientation: "horizontal"
        size_hint: None, None
        size: "150dp", "40dp"
        pos_hint: {"center_x": 0.5, "center_y": 0.4}
        spacing: dp(4)

        MDRaisedButton:
            text: "Invest"
            size_hint: None, None
            size: "100dp", "50dp"
            md_bg_color: 0.2, 0.6, 1, 1
            on_release:app.switch_to_invest()

        MDRaisedButton:
            text: "Referral"
            size_hint: None, None
            size: "100dp", "50dp"



            md_bg_color: 0.8, 0.3, 0.3, 1
            line_color: 0, 0, 0, 1  # Black line color

    MDRaisedButton:
        text: "ENTER TO THE GAME"
        size_hint: None, None
        size: "100dp", "50dp"
        md_bg_color:0,0,1,1
        on_release:app.switch_to_Game()
        pos_hint: {"center_x": 0.5, "center_y": 0.2}
        text_color: 1.0, 1.0, 1.0
# Registered screen layout
<registred>:
    name: "registred"
    FloatLayout:
        BoxLayout:
            orientation: "horizontal"
            spacing: dp(5)
            size_hint: None, None
            size: "180dp", "0dp"
            pos_hint: {"center_x": .5, "center_y": .9}
            height: "30dp"
            MDLabel:
                id: registred_error_input
                text: " "
                size_hint_y: None
                height: dp(30)
                theme_text_color: "Secondary"
                pos_hint: {"center_x": .95, "center_y": .92}
                color: 1, 0, 0, 1  # Red color for error messages

        MDTextField:
            id: registred_email_input
            hint_text: "Email"
            font_size: "20dp"
            icon_right: "email"
            size_hint_x: .85
            pos_hint: {"center_x": .5, "center_y": .85}
            mode: "line"
            helper_text: "Enter a valid email"
            helper_text_mode: "on_focus"
            error: False

        MDTextField:
            id: registred_firstname_input
            hint_text: "First Name"
            font_size: "20dp"
            icon_right: "account"
            size_hint_x: .85
            pos_hint: {"center_x": .5, "center_y": .71}
            mode: "line"
            helper_text: "Enter a valid first name"
            helper_text_mode: "on_focus"
            error: False

        MDTextField:
            id: registred_lastname_input
            hint_text: "Last Name"
            font_size: "20dp"
            icon_right: "account"
            size_hint_x: .85
            pos_hint: {"center_x": .5, "center_y": .57}
            mode: "line"
            helper_text: "Enter a valid last name"
            helper_text_mode: "on_focus"
            error: False

        MDTextField:
            id: registred_username_input
            hint_text: "Username"
            font_size: "20dp"
            icon_right: "account"
            size_hint_x: .85
            pos_hint: {"center_x": .5, "center_y": .43}
            mode: "line"
            helper_text: "Enter a valid username"
            helper_text_mode: "on_focus"
            error: False

        MDTextField:
            id: registred_password_input
            hint_text: "Password"
            font_size: "20dp"
            icon_right: "eye-off"
            size_hint_x: .85
            pos_hint: {"center_x": .5, "center_y": .29}
            mode: "line"
            password: True
            hint_text_color: (1, 1, 1, 1)
            helper_text: "Password required"
            helper_text_mode: "on_focus"
            error: False

        # Checkbox to toggle password visibility
        BoxLayout:
            spacing: dp(5)
            size_hint: .85, None
            pos_hint: {"center_x": .5, "center_y": .18}
            height: "30dp"
            MDCheckbox:
                id: my_checkbox
                size_hint: None, None
                size: dp(30), dp(30)
                on_press:
                    registred_password_input.password = not registred_password_input.password
        
                    registred_password_input.icon_right = "eye" if registred_password_input.password else "eye-off"
            MDLabel     
                text: "Show password"
                size_hint_y: None
                height: dp(30)
                theme_text_color: "Secondary"

        # Sign up and Sign in buttons
        BoxLayout:
            orientation: "horizontal"
            size_hint: .85, None
            height: "50dp"
            pos_hint: {"center_x": .5, "center_y": .09}
            spacing: dp(10)
            MDFlatButton:
                text: "BACK TO LOGIN"
                font_size: "22dp"
                on_release:
                    app.login()
                    
                    
                md_bg_color: 1,0,1,1
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint: 0.45, None
                height: dp(50)

            MDFlatButton:
                text: "SIGN UP"
                font_size: "22dp"
                on_release:
                    app.validation(); app.signup()  # Using a semicolon inside the lambda
                    
                    
                md_bg_color: 0.1, 0.7, 0.3, 1
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint: 0.45, None
                height: dp(50)
<Wallet>:
    name: "wallet"
    FloatLayout:
        MDTopAppBar:
            size_hint_y: None
            height: "100dp"
            pos_hint: {"bottom": 1}
            md_bg_color:0.0, 0.392, 0.0 # A calm turquoise color for the navbar

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "45dp", "90dp"
            pos_hint: {"right": 1, "bottom": 1}
            spacing: dp(25)
            MDCard:
                size_hint: None, None
                size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
                line_color: 0, 0, 1, 1  # Black line color

                Image:
                    id: profile_picture
                    source: "gear-removebg-preview.png"
                    size_hint: None, None
                    size: "25dp", "45dp"
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    allow_stretch: True
                    radius: [60]
                    on_touch_down:app.switch_to_setting()

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "110dp", "90dp"
            pos_hint: {"right": 1, "bottom": 1}
            spacing: dp(25)
            MDCard:
                size_hint: None, None
                size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
                line_color: 0, 0, 1, 1

                Image:
                    id: profile_picture
                    source: "images-removebg-preview (1).png"
                    size_hint: None, None
                    size: "25dp", "35dp"  # Set the image size to match the card size
                    pos_hint: {"center_x": 0.5, "center_y": 0.5} 
                
                    on_touch_down: app.switch_to_withdraw(*args)

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "175dp", "90dp"
            pos_hint: {"right": 1, "bottom": 1}
            spacing: dp(25)
            MDCard:
                size_hint: None, None
                size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "7dp"
                md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
                line_color: 0, 0, 1, 1 
                
                
                Image:
                    source: "wallet.png"
                    size_hint: None, None
                    size: "20dp", "20dp"  # Set the image size to match the card size
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}  # Center the image within the card
                    on_touch_down: app.switch_to_Wallet(*args)
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "55dp", "25dp"
            pos_hint: {"right": 1, "bottom": 1}
            spacing: dp(25)

            MDLabel:
                text: "Settings"
                size_hint_y: None
                height: dp(20)
                font_size:"14sp"
                pos_hint: {"center_x": 0.65, "top": 1}
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "120dp", "25dp"
            pos_hint: {"right": 1, "bottom": 1}
            

            MDLabel:
                text: "Withdraw"
                size_hint_y: None
                height: dp(20)
                font_size: "14sp"
                pos_hint: {"center_x": 0.65, "top": 1}
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "175dp", "25dp"
            pos_hint: {"right": 1, "bottom": 1}

            MDLabel:
                text: "Wallet"
                size_hint_y: None
                height: dp(20)
                font_size: "14sp"
                pos_hint: {"center_x": 0.65, "top": 1}
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "190dp", "90dp"  # Set the overall size of the BoxLayout container
            pos_hint: {"x": 0, "bottom": 1}  # Position BoxLayout at top-left corner
            spacing: dp(5)  # Set spacing between images
            MDCard:
                size_hint: None, None
                size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
                line_color: 0, 0, 1, 1 

            # Second Image (Positioned beside the first image)
                Image:
                    id: profile_picture_2
                    source: "download__2_-removebg-preview.png"  # Path to your initial image (can be placeholder)
                    size_hint: None, None
                    size: "25dp", "25dp"  # Adjust size as needed
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}  # Center the image
                    allow_stretch: True
                    radius: [50]  # Rounded corners
                    on_touch_down: app.on_image_touch_up(*args)   # On touch event, call the function

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "175dp", "25dp"
            pos_hint: {"left": 1, "bottom": 1}

            MDLabel:
                text: "Profile"
                size_hint_y: None
                height: dp(20)
                font_size: "14sp"
                pos_hint: {"center_x": 0.65, "top": 1}
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1


        # Profile Image
        Image:
            id: profile_picture
            source: "images/image.jpg"
            size_hint: None, None
            size: "200dp", "75dp"
            pos_hint: {"center_x": .5, "center_y": .8}
            allow_stretch: True

        # Wallet Title
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "85dp", "20dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.7}
            

            MDLabel:
                text: "wallet"
                font_size: "30dp"
                pos_hint: {"center_x": 0.5, "center_y": .7}
                theme_text_color: "Custom"
                text_color: 1, 0.0784, 0.5765, 1    

        # Amount Input Field
        MDTextField:
            id: wallet_amount
            hint_text: "Amount"
            font_size: "20dp"
            icon_right: "currency-usd"  # Currency USD icon on the right
            size_hint_x: .75
            pos_hint: {"center_x": .5, "center_y": .5}
            mode: "fill"
            readonly: True  # Make the field readonly (no user input)
            text: "100.00"  # You can set a default value if needed
        MDRaisedButton:
            text: "Back"
            size_hint: None, None  # Disable automatic scaling, set fixed size
            size: "75dp", "30dp"  # Define the fixed size for the button
            md_bg_color: 0.0, 0.0, 0.0  # Background color: Black
            text_color: 1.0, 1.0, 1.0  # Text color: White
            pos_hint: {"x": 0, "top": 1}  # Position the button at the top-left corner
            on_release: app.switch_to_dashboard1()  # Call the method when the button is pressed
        

            
<Withdraw>:
    name: "withdraw"
    FloatLayout:

        # Profile Image
        MDTopAppBar:
            size_hint_y: None
            height: "100dp"
            pos_hint: {"bottom": 1}
            md_bg_color:0.0, 0.392, 0.0 # A calm turquoise color for the navbar

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "45dp", "90dp"
            pos_hint: {"right": 1, "bottom": 1}
            spacing: dp(25)
            MDCard:
                size_hint: None, None
                size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
                line_color: 0, 0, 1, 1  # Black line color

                Image:
                    id: profile_picture
                    source: "gear-removebg-preview.png"
                    size_hint: None, None
                    size: "25dp", "45dp"
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    allow_stretch: True
                    radius: [60]
                    on_touch_down:app.switch_to_setting()

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "110dp", "90dp"
            pos_hint: {"right": 1, "bottom": 1}
            spacing: dp(25)
            MDCard:
                size_hint: None, None
                size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
                line_color: 0, 0, 1, 1

                Image:
                    id: profile_picture
                    source: "images-removebg-preview (1).png"
                    size_hint: None, None
                    size: "25dp", "35dp"  # Set the image size to match the card size
                    pos_hint: {"center_x": 0.5, "center_y": 0.5} 
                
                    on_touch_down: app.switch_to_withdraw(*args)

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "175dp", "90dp"
            pos_hint: {"right": 1, "bottom": 1}
            spacing: dp(25)
            MDCard:
                size_hint: None, None
                size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "7dp"
                md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
                line_color: 0, 0, 1, 1 
                
                
                Image:
                    source: "wallet.png"
                    size_hint: None, None
                    size: "20dp", "20dp"  # Set the image size to match the card size
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}  # Center the image within the card
                    on_touch_down: app.switch_to_Wallet(*args)
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "55dp", "25dp"
            pos_hint: {"right": 1, "bottom": 1}
            spacing: dp(25)

            MDLabel:
                text: "Settings"
                size_hint_y: None
                height: dp(20)
                font_size:"14sp"
                pos_hint: {"center_x": 0.65, "top": 1}
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "120dp", "25dp"
            pos_hint: {"right": 1, "bottom": 1}
            

            MDLabel:
                text: "Withdraw"
                size_hint_y: None
                height: dp(20)
                font_size: "14sp"
                pos_hint: {"center_x": 0.65, "top": 1}
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "175dp", "25dp"
            pos_hint: {"right": 1, "bottom": 1}

            MDLabel:
                text: "Wallet"
                size_hint_y: None
                height: dp(20)
                font_size: "14sp"
                pos_hint: {"center_x": 0.65, "top": 1}
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "190dp", "90dp"  # Set the overall size of the BoxLayout container
            pos_hint: {"x": 0, "bottom": 1}  # Position BoxLayout at top-left corner
            spacing: dp(5)  # Set spacing between images
            MDCard:
                size_hint: None, None
                size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
                line_color: 0, 0, 1, 1 

            # Second Image (Positioned beside the first image)
                Image:
                    id: profile_picture_2
                    source: "download__2_-removebg-preview.png"  # Path to your initial image (can be placeholder)
                    size_hint: None, None
                    size: "25dp", "25dp"  # Adjust size as needed
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}  # Center the image
                    allow_stretch: True
                    radius: [50]  # Rounded corners
                    on_touch_down: app.on_image_touch_up(*args)   # On touch event, call the function

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "175dp", "25dp"
            pos_hint: {"left": 1, "bottom": 1}

            MDLabel:
                text: "Profile"
                size_hint_y: None
                height: dp(20)
                font_size: "14sp"
                pos_hint: {"center_x": 0.65, "top": 1}
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1

        Image:
            id: profile_picture
            source: "images/withdraw.png"
            size_hint: None, None
            size: "200dp", "75dp"
            pos_hint: {"center_x": .5, "center_y": .8}
            allow_stretch: True
            
            # Wallet Title
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "85dp", "20dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.7}
            

            MDLabel:
                text: "withdraw"
                font_size: "20dp"
                pos_hint: {"center_x": 0.5, "center_y": .7}
                theme_text_color: "Custom"
                text_color: 1, 0.0784, 0.5765, 1    

        # Amount Input Field
        MDTextField:
            id: withdraw_amount
            hint_text: "amount to withdraw"
            font_size: "20dp"
            icon_right: "currency-usd"  # Changed to a valid icon
            size_hint_x: .75
            pos_hint: {"center_x": .5, "center_y": .6}
            mode: "round"
            helper_text: "Enter a valid amount"
            helper_text_mode: "on_focus"
            error: False
        MDTextField:
            id: withdraw_account_number
            hint_text: "Bank account number"
            font_size: "20dp"
           
            size_hint_x: .75
            pos_hint: {"center_x": .5, "center_y": .5}
            mode: "round"
            helper_text: "Enter a valid amount"
            helper_text_mode: "on_focus"
            error: False
        MDTextField:
            id: withdraw_name
            hint_text: "account holder name"
            font_size: "20dp"
           
            size_hint_x: .75
            pos_hint: {"center_x": .5, "center_y": .4}
            mode: "round"
            helper_text: "Enter a valid Name"
            helper_text_mode: "on_focus"
            error: False
       
        MDRaisedButton:
            text: "SUBMIT"
            size_hint: None, None
            size: "100dp", "50dp"
            md_bg_color:0.0, 0.0, 1.0
            on_press: app.on_referral_button_press
            pos_hint: {"center_x": 0.5, "center_y": 0.3}
            text_color: 1.0, 1.0, 1.0
        MDRaisedButton:
            text: "Back"
            size_hint: None, None  # Disable automatic scaling, set fixed size
            size: "75dp", "30dp"  # Define the fixed size for the button
            md_bg_color: 0.0, 0.0, 0.0  # Background color: Black
            text_color: 1.0, 1.0, 1.0  # Text color: White
            pos_hint: {"x": 0, "top": 1}  # Position the button at the top-left corner
            on_release: app.switch_to_dashboard1()  # Call the method when the button is pressed

<invest>:
    name: "invest"
    FloatLayout:
        MDTopAppBar:
            size_hint_y: None
            height: "100dp"
            pos_hint: {"bottom": 1}
            md_bg_color:0.0, 0.392, 0.0 # A calm turquoise color for the navbar

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "45dp", "90dp"
            pos_hint: {"right": 1, "bottom": 1}
            spacing: dp(25)
            MDCard:
                size_hint: None, None
                size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
                line_color: 0, 0, 1, 1  # Black line color

                Image:
                    id: profile_picture
                    source: "gear-removebg-preview.png"
                    size_hint: None, None
                    size: "25dp", "45dp"
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    allow_stretch: True
                    radius: [60]
                    on_touch_down:app.switch_to_setting()

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "110dp", "90dp"
            pos_hint: {"right": 1, "bottom": 1}
            spacing: dp(25)
            MDCard:
                size_hint: None, None
                size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
                line_color: 0, 0, 1, 1

                Image:
                    id: profile_picture
                    source: "images-removebg-preview (1).png"
                    size_hint: None, None
                    size: "25dp", "35dp"  # Set the image size to match the card size
                    pos_hint: {"center_x": 0.5, "center_y": 0.5} 
                
                    on_touch_down: app.switch_to_withdraw(*args)

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "175dp", "90dp"
            pos_hint: {"right": 1, "bottom": 1}
            spacing: dp(25)
            MDCard:
                size_hint: None, None
                size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "7dp"
                md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
                line_color: 0, 0, 1, 1 
                
                
                Image:
                    source: "wallet.png"
                    size_hint: None, None
                    size: "20dp", "20dp"  # Set the image size to match the card size
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}  # Center the image within the card
                    on_touch_down: app.switch_to_Wallet(*args)
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "55dp", "25dp"
            pos_hint: {"right": 1, "bottom": 1}
            spacing: dp(25)

            MDLabel:
                text: "Settings"
                size_hint_y: None
                height: dp(20)
                font_size:"14sp"
                pos_hint: {"center_x": 0.65, "top": 1}
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "120dp", "25dp"
            pos_hint: {"right": 1, "bottom": 1}
            

            MDLabel:
                text: "Withdraw"
                size_hint_y: None
                height: dp(20)
                font_size: "14sp"
                pos_hint: {"center_x": 0.65, "top": 1}
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "175dp", "25dp"
            pos_hint: {"right": 1, "bottom": 1}

            MDLabel:
                text: "Wallet"
                size_hint_y: None
                height: dp(20)
                font_size: "14sp"
                pos_hint: {"center_x": 0.65, "top": 1}
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "190dp", "90dp"  # Set the overall size of the BoxLayout container
            pos_hint: {"x": 0, "bottom": 1}  # Position BoxLayout at top-left corner
            spacing: dp(5)  # Set spacing between images
            MDCard:
                size_hint: None, None
                size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
                line_color: 0, 0, 1, 1 

            # Second Image (Positioned beside the first image)
                Image:
                    id: profile_picture_2
                    source: "download__2_-removebg-preview.png"  # Path to your initial image (can be placeholder)
                    size_hint: None, None
                    size: "25dp", "25dp"  # Adjust size as needed
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}  # Center the image
                    allow_stretch: True
                    radius: [50]  # Rounded corners
                    on_touch_down: app.on_image_touch_up(*args)   # On touch event, call the function

        BoxLayout:
            padding:"5dp"
           
            BoxLayout:
                orientation: "vertical"
                size_hint: None, None
                size: "425dp", "100dp"
                pos_hint: {"left": 1, "bottom": 1}

                MDLabel:
                    text: "Profile"
                    size_hint_y: None
                    height: dp(20)
                    font_size: "14sp"
                    pos_hint: {"center_x": 0.65, "top": 1}
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1


        # Profile Image
        Image:
            id: profile_picture
            source: "images/invest-removebg-preview.png"
            size_hint: None, None
            size: "250dp", "80dp"
            pos_hint: {"center_x": .5, "center_y": .8}
            allow_stretch: True
        MDTextField:
            id: Invest_amount_input
            hint_text: "Enter your amount"
            font_size: "20dp"
           
            size_hint_x: .75
            pos_hint: {"center_x": .5, "center_y": .6}
            mode: "fill"
            input_filter: "float" 
            
        MDRaisedButton:
            text: "invest"
            size_hint: None, None
            size: "100dp", "50dp"
            md_bg_color:0.5, 0.0, 0.5
            on_press: app.on_referral_button_press
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            text_color: 1.0, 1.0, 1.0       
            
        MDRaisedButton:
            text: "Back"
            size_hint: None, None  # Disable automatic scaling, set fixed size
            size: "75dp", "30dp"  # Define the fixed size for the button
            md_bg_color: 0.0, 0.0, 0.0  # Background color: Black
            text_color: 1.0, 1.0, 1.0  # Text color: White
            pos_hint: {"x": 0, "top": 1}  # Position the button at the top-left corner
            on_release: app.switch_to_dashboard1()  # Call the method when the button is pressed
<Admin>:
    name:"admin"
    MDLabel:
        text:"Admin"
        
        pos_hint: {"center_x": 0.5, "center_y": 0.65}
           

<game>:
    name: "game"
    FloatLayout:
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "210dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.75}
            spacing: dp(4)
            MDCard:
                orientation: "vertical"
                size_hint: None, None
                size: "45dp", "45dp"
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 0.1, 0.5, 0.1, 1
                MDLabel:
                    text: "1"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    halign: "center"
                    valign: "middle"
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "235dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.67}
            MDTextField:
                id: one
                hint_text: ""
            
                width:"75dp"
                height: self.minimum_height
                size_hint_x: None  # Width is fixed
                size_hint_y: None  # Height is fixed

                
                
                pos_hint: {"center_x": .5, "center_y": .5}
                mode: "round"
                input_filter: "int"

                

        # Second BoxLayout with MDCard and label '2'
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "50dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.75}
            spacing: dp(4)
            MDCard:
                orientation: "vertical"
                size_hint: None, None
                size: "45dp", "45dp"
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 0, 0, 1, 1
                MDLabel:
                    text: "2"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    halign: "center"
                    valign: "middle"
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "75dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.67}
            MDTextField:
                id: one
                hint_text: ""
                
                width:"75dp"
                size_hint_x: None  # Width is fixed
                size_hint_y: None  # Height is fixed

                
                
                pos_hint: {"center_x": .5, "center_y": .5}
                mode: "round"
                input_filter: "int"


        # Third BoxLayout with MDCard and label '3'
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "-110dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.75}
            spacing: dp(4)
            MDCard:
                orientation: "vertical"
                size_hint: None, None
                size: "45dp", "45dp"
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 0.7, 0.1, 0.1, 1
                MDLabel:
                    text: "3"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    halign: "center"
                    valign: "middle"
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "-85dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.67}
            MDTextField:
                id: one
                hint_text: ""
                
                width:"75dp"
                size_hint_x: None  # Width is fixed
                size_hint_y: None  # Height is fixed

                
                
                pos_hint: {"center_x": .5, "center_y": .5}
                mode: "round"
                input_filter: "int"
                
                
    

        # Fourth BoxLayout with MDCard and label '4'
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "200dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.60}
            spacing: dp(4)
            MDCard:
                orientation: "vertical"
                size_hint: None, None
                size: "45dp", "45dp"
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 0.1, 0.5, 0.1, 1
                MDLabel:
                    text: "4"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    halign: "center"
                    valign: "middle"
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "235dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.52}
            MDTextField:
                id: one
                hint_text: ""
            
                width:"75dp"
                height: self.minimum_height
                size_hint_x: None  # Width is fixed
                size_hint_y: None  # Height is fixed

                
                
                pos_hint: {"center_x": .5, "center_y": .5}
                mode: "round"
                input_filter: "int"

                


        # Fifth BoxLayout with MDCard and label '5'
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "50dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.60}
            spacing: dp(4)
            MDCard:
                orientation: "vertical"
                size_hint: None, None
                size: "45dp", "45dp"
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 0, 0, 1, 1
                MDLabel:
                    text: "5"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    halign: "center"
                    valign: "middle"


        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "75dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.52}
            MDTextField:
                id: one
                hint_text: ""
                
                width:"75dp"
                size_hint_x: None  # Width is fixed
                size_hint_y: None  # Height is fixed

                
                
                pos_hint: {"center_x": .5, "center_y": .5}
                mode: "round"
                input_filter: "int"


        # Sixth BoxLayout with MDCard and label '6'
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "-110dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.60}
            spacing: dp(4)
            MDCard:
                orientation: "vertical"
                size_hint: None, None
                size: "45dp", "45dp"
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 0.7, 0.1, 0.1, 1
                MDLabel:
                    text: "6"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    halign: "center"
                    valign: "middle"
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "-85dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.52}
            MDTextField:
                id: one
                hint_text: ""
                
                width:"75dp"
                size_hint_x: None  # Width is fixed
                size_hint_y: None  # Height is fixed

                
                
                pos_hint: {"center_x": .5, "center_y": .5}
                mode: "round"
                input_filter: "int"
                

        # Seventh BoxLayout with MDCard and label '7'
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "200dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.45}
            spacing: dp(4)
            MDCard:
                orientation: "vertical"
                size_hint: None, None
                size: "45dp", "45dp"
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 0.1, 0.5, 0.1, 1
                MDLabel:
                    text: "7"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    halign: "center"
                    valign: "middle"
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "235dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.37}
            MDTextField:
                id: one
                hint_text: ""
            
                width:"75dp"
                height: self.minimum_height
                size_hint_x: None  # Width is fixed
                size_hint_y: None  # Height is fixed

                
                
                pos_hint: {"center_x": .5, "center_y": .5}
                mode: "round"
                input_filter: "int"

                


        # Eighth BoxLayout with MDCard and label '8'
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "50dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.45}
            spacing: dp(4)
            MDCard:
                orientation: "vertical"
                size_hint: None, None
                size: "45dp", "45dp"
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 0, 0, 1, 1
                MDLabel:
                    text: "8"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    halign: "center"
                    valign: "middle"
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "75dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.37}
            MDTextField:
                id: one
                hint_text: ""
                
                width:"75dp"
                size_hint_x: None  # Width is fixed
                size_hint_y: None  # Height is fixed

                
                
                pos_hint: {"center_x": .5, "center_y": .5}
                mode: "round"
                input_filter: "int"

        # Ninth BoxLayout with MDCard and label '9'
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "-110dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.45}
            spacing: dp(4)
            MDCard:
                orientation: "vertical"
                size_hint: None, None
                size: "45dp", "45dp"
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 0.7, 0.1, 0.1, 1
                MDLabel:
                    text: "9"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    halign: "center"
                    valign: "middle"
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "-85dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.37}
            MDTextField:
                id: one
                hint_text: ""
                
                width:"75dp"
                size_hint_x: None  # Width is fixed
                size_hint_y: None  # Height is fixed

                
                
                pos_hint: {"center_x": .5, "center_y": .5}
                mode: "round"
                input_filter: "int"
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "50dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.3}
            spacing: dp(4)
            MDCard:
                orientation: "vertical"
                size_hint: None, None
                size: "45dp", "45dp"
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 0, 0, 1, 1
                MDLabel:
                    text: "0"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    halign: "center"
                    valign: "middle"
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "75dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.22}
            MDTextField:
                id: one
                hint_text: ""
                
                width:"75dp"
                size_hint_x: None  # Width is fixed
                size_hint_y: None  # Height is fixed

                
                
                pos_hint: {"center_x": .5, "center_y": .5}
                mode: "round"
                input_filter: "int"


        # Button to go back
        MDRaisedButton:
            text: "Back"
            size_hint: None, None
            size: "75dp", "30dp"
            md_bg_color: 0.0, 0.0, 0.0
            text_color: 1.0, 1.0, 1.0
            pos_hint: {"x": 0, "top": 1}
            on_release: app.switch_to_dashboard1()

        
<Settings>:
    name:"settings"
    FloatLayout:
            # Adding MDCard with a logout button inside
        canvas.before:
            Color:
                rgba: 0.678, 0.847, 0.902, 1     # White Smoke color
            Rectangle:
                pos: self.pos
                size: self.size

        # MDCard with both Image and Logout Button inside
        MDTopAppBar:
            size_hint_y: None
            height: "100dp"
            pos_hint: {"bottom": 1}
            md_bg_color:0.0, 0.392, 0.0 # A calm turquoise color for the navbar

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "45dp", "90dp"
            pos_hint: {"right": 1, "bottom": 1}
            spacing: dp(25)
            MDCard:
                size_hint: None, None
                size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
                line_color: 0, 0, 1, 1  # Black line color

                Image:
                    id: profile_picture
                    source: "gear-removebg-preview.png"
                    size_hint: None, None
                    size: "25dp", "45dp"
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    allow_stretch: True
                    radius: [60]
                    on_touch_down:app.switch_to_setting()

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "110dp", "90dp"
            pos_hint: {"right": 1, "bottom": 1}
            spacing: dp(25)
            MDCard:
                size_hint: None, None
                size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                radius: [50]
                padding: "5dp"
                md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
                line_color: 0, 0, 1, 1

                Image:
                    id: profile_picture
                    source: "images-removebg-preview (1).png"
                    size_hint: None, None
                    size: "25dp", "35dp"  # Set the image size to match the card size
                    pos_hint: {"center_x": 0.5, "center_y": 0.5} 
                
                    on_touch_down: app.switch_to_withdraw(*args)

        
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "55dp", "25dp"
            pos_hint: {"right": 1, "bottom": 1}
            spacing: dp(25)

            MDLabel:
                text: "Settings"
                size_hint_y: None
                height: dp(20)
                font_size:"14sp"
                pos_hint: {"center_x": 0.65, "top": 1}
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
       
        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "120dp", "25dp"
            pos_hint: {"right": 1, "bottom": 1}
            

            MDLabel:
                text: "Withdraw"
                size_hint_y: None
                height: dp(20)
                font_size: "14sp"
                pos_hint: {"center_x": 0.65, "top": 1}
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
        BoxLayout:
            padding:"5dp"
           
            BoxLayout:
                orientation: "vertical"
                size_hint: None, None
                size: "425dp", "100dp"
                pos_hint: {"left": 1, "bottom": 1}

                MDLabel:
                    text: "Wallet"
                    size_hint_y: None
                    height: dp(20)
                    font_size: "14sp"
                    pos_hint: {"center_x": 0.65, "top": 1}
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1

        BoxLayout:
            padding:"5dp"
            
            BoxLayout:
                orientation: "vertical"
                size_hint: None, None
                size: "40dp", "-45dp"  # Adjust the size of the container to fit both images and cards
                pos_hint: {"left": 0.1, "center_y":0.0001}  # Position BoxLayout on the left, adjust if needed
                spacing: dp(10)  # Set spacing between images/cards

                MDCard:
                    size_hint: None, None
                    size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    radius: [50]
                    padding: "5dp"
                    md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
                    line_color: 0, 0, 1, 1  # Set card border color

                    Image:
                        id: profile_picture_1  # Unique ID for the first image
                        source: "download__2_-removebg-preview.png"  # Placeholder image
                        size_hint: None, None
                        size: "25dp", "25dp"  # Adjust size as needed
                        pos_hint: {"center_x": 0.5, "center_y": 0.5}  # Center the image inside its container
                        allow_stretch: True
                        radius: [50]  # Rounded corners
                        on_touch_down: app.on_image_touch_up(*args)  # On touch event, call the function
        BoxLayout:
            padding:"5dp"
            
            BoxLayout:
                orientation: "vertical"
                size_hint: None, None
                size: "170dp", "-45dp"  # Adjust the size of the container to fit both images and cards
                pos_hint: {"left": 0.1, "center_y":0.0001}  # Position BoxLayout on the left, adjust if needed
                spacing: dp(10)  # Set spacing between images/cards

                MDCard:
                    size_hint: None, None
                    size: "35dp", "35dp"  # Set the card size to match the desired card dimensions
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    radius: [50]
                    padding: "5dp"
                    md_bg_color: 1, 1, 1, 1  # Set the background color of the card to white (RGBA format)
                    line_color: 0, 0, 1, 1  # Set card border color

                    Image:
                        id: profile_picture_1  # Unique ID for the first image
                        source: "wallet.png"  # Placeholder image
                        size_hint: None, None
                        size: "25dp", "25dp"  # Adjust size as needed
                        pos_hint: {"center_x": 0.5, "center_y": 0.5}  # Center the image inside its container
                        allow_stretch: True
                        radius: [50]  # Rounded corners
                        on_touch_down: app.on_image_touch_up(*args)  # On touch event, call the function

        BoxLayout:
            orientation: "horizontal"
            size_hint: None, None
            size: "175dp", "25dp"
            pos_hint: {"left": 1, "bottom": 1}

            MDLabel:
                text: "Profile"
                size_hint_y: None
                height: dp(20)
                font_size: "14sp"
                pos_hint: {"center_x": 0.65, "top": 1}
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1

            
        MDCard:
            size_hint: None, None
            size: "250dp", "50dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.4}
            
            radius: [15,]
            padding: "7dp"
            orientation: "vertical"
            md_bg_color: 0.96, 0.96, 0.96, 1  

            # BoxLayout for Image
            BoxLayout:
                orientation: "horizontal"
                size_hint: None, None
                size: "130dp", "-300dp"
                pos_hint: {"center_x": 0.5}
                padding: "-45dp"

                Image:
                    source:"switch.png"
                    size_hint: None, None
                    size: "30dp", "30dp"
                    allow_stretch: True
                    radius: [60]  # Makes the image round
                    
            # BoxLayout for Button
            BoxLayout:
                orientation: "horizontal"
                size_hint: None, None
                size: "150dp", "50dp"
                pos_hint: {"center_x": 0.5}

                MDFlatButton:
                    text: "Logout"
                    size_hint: None, None
                    size: "150dp", "50dp"
                    font_size:"18dp"
                    md_bg_color: 0,0,0,0
                    text_color: 1.0, 1.0, 1.0
                    pos_hint: {"center_x": 0.5}
                    on_release: app.create_logout_card()
        
        MDCard:
            size_hint: None, None
            size: "250dp", "50dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.7}
            
            radius: [15,]
            padding: "7dp"
            orientation: "vertical"
            md_bg_color: 0.96, 0.96, 0.96, 1  

            # BoxLayout for Image
            BoxLayout:
                orientation: "horizontal"
                size_hint: None, None
                size: "130dp", "-300dp"
                pos_hint: {"center_x": 0.5}
                padding: "-45dp"

                Image:
                    source:"help1-removebg-preview.png"
                    size_hint: None, None
                    size: "30dp", "30dp"
                    allow_stretch: True
                    radius: [60]  # Makes the image round
                    
            # BoxLayout for Button
            BoxLayout:
                orientation: "horizontal"
                size_hint: None, None
                size: "150dp", "50dp"
                pos_hint: {"center_x": 0.5}

                MDFlatButton:
                    text: "Help"
                    size_hint: None, None
                    size: "150dp", "50dp"
                    font_size:"18dp"
                    md_bg_color: 0,0,0,0
                    text_color: 1.0, 1.0, 1.0
                    pos_hint: {"center_x": 0.5}
                    # on_release: app.switch_to_login()
        MDCard:
            size_hint: None, None
            size: "250dp", "50dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            radius: [15,]
            padding: "7dp"
            orientation: "vertical"
           
            md_bg_color: 0.96, 0.96, 0.96, 1  

            # BoxLayout for Image
            BoxLayout:
                orientation: "horizontal"
                size_hint: None, None
                size: "130dp", "130dp"  # Adjusted to give more space for the image
                pos_hint: {"center_x": 0.5}
                padding: "-45dp"

                Image:
                    source: "images__2_-removebg-preview.png"
                    size_hint: None, None
                    size: "30dp", "30dp"  # Size of the image
                    allow_stretch: True
                    radius: [60]  # Makes the image round

            # BoxLayout for Button
            BoxLayout:
                orientation: "horizontal"
                size_hint: None, None
                size: "150dp", "50dp"
                pos_hint: {"center_x": 0.5}

                MDFlatButton:
                    text: "Change your Password"
                    size_hint: None, None
                    size: "150dp", "50dp"
                    font_size: "18dp"
                    md_bg_color: 0, 0, 0, 0
                    text_color: 1.0, 1.0, 1.0
                    pos_hint: {"center_x": 0.5}
                    disabled:False
                    on_release: app.switch_to_changepassword()# Call this function when the button is clicked
        MDCard:
            size_hint: None, None
            size: "250dp", "50dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.6}
            radius: [15,]
            padding: "7dp"
            orientation: "vertical"
           
            md_bg_color: 0.96, 0.96, 0.96, 1  

            # BoxLayout for Image
            BoxLayout:
                orientation: "horizontal"
                size_hint: None, None
                size: "130dp", "130dp"  # Adjusted to give more space for the image
                pos_hint: {"center_x": 0.5}
                padding: "-45dp"

                Image:
                    source: "images__1_-removebg-preview.png"
                    size_hint: None, None
                    size: "30dp", "30dp"  # Size of the image
                    allow_stretch: True
                    radius: [60]  # Makes the image round

            # BoxLayout for Button
            BoxLayout:
                orientation: "horizontal"
                size_hint: None, None
                size: "150dp", "50dp"
                pos_hint: {"center_x": 0.5}

                MDFlatButton:
                    id:change_email
                    text: "Change your Email"
                    size_hint: None, None
                    size: "150dp", "50dp"
                    font_size: "18dp"
                    md_bg_color: 0, 0, 0, 0
                    text_color: 1.0, 1.0, 1.0
                    pos_hint: {"center_x": 0.5}
                    on_release: app.switch_to_changepassword()# Call this function when the button is clicked
        
                    
<Changepassword>:
    name:"update_password"
    FloatLayout:
        MDTextField:
            id: old_password
            hint_text: "Old Password"
            size_hint_x: .85
            pos_hint: {"center_x": 0.5, "center_y": 0.7}
            password: True

        MDTextField:
            id: new_password
            hint_text: "New Password"
            
            size_hint_x: .85
            pos_hint: {"center_x": 0.5, "center_y": 0.55}
            password: True

        MDTextField:
            id: confirm_password
            hint_text: "Confirm New Password"
            size_hint_x: .85
            pos_hint: {"center_x": 0.5, "center_y": 0.4}
            password: True

        MDRaisedButton:
            text: "Update Password"
            size_hint_x: .85
            pos_hint: {"center_x": 0.5, "center_y": 0.25}
            on_release: app.update_password()

        Label:
            text: "Please fill in the fields"
            size_hint: None, None
            size: "200dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.1}
        
<ChangeEmail>:
    name:"update_Email"
    FloatLayout:
        MDTextField:
            id: old_password
            hint_text: "Old Password"
            size_hint_x: .85
            pos_hint: {"center_x": 0.5, "center_y": 0.7}
            password: True

        MDTextField:
            id: new_password
            hint_text: "New Password"
            
            size_hint_x: .85
            pos_hint: {"center_x": 0.5, "center_y": 0.55}
            password: True

        MDTextField:
            id: confirm_password
            hint_text: "Confirm New Password"
            size_hint_x: .85
            pos_hint: {"center_x": 0.5, "center_y": 0.4}
            password: True

        MDRaisedButton:
            text: "Update Password"
            size_hint_x: .85
            pos_hint: {"center_x": 0.5, "center_y": 0.25}
            on_release: app.update_password()

        Label:
            text: "Please fill in the fields"
            size_hint: None, None
            size: "200dp", "40dp"
            pos_hint: {"center_x": 0.5, "center_y": 0.1}
        
                       
            
    
            


'''


class MaterialTextInput(Screen):
    """Login screen logic"""
    pass

class Dashboard(Screen):
    """Dashboard screen logic"""
    pass
class Admin(Screen):
    """Dashboard screen logic"""
    pass
class registred(Screen):
    """Registered screen logic"""
    pass
class Wallet(Screen):
    """wallet screen logic"""
    pass
class Withdraw(Screen):
    """withdraw screen logic"""
    pass
class Invest(Screen):
    """invest screen logic"""
    pass
class Game(Screen):
    """invest screen logic"""
    pass
class Settings(Screen):
    """setting screen logic"""
    pass
class Changepassword(Screen):
    """changepassword"""
    pass
class ChangeEmail(Screen):
    """changeEmail"""
    pass

class Ram(MDApp):
    def build(self):
        """Build and return the ScreenManager with all screens"""
        self.theme_cls.theme_style = "Light"  # Set the theme style
       
        
       
        # Create ScreenManager
        sm = ScreenManager()

        # Add screens to the manager
        sm.add_widget(MaterialTextInput(name="login"))
        sm.add_widget(Dashboard(name="dashboard"))
        sm.add_widget(registred(name="registred"))
        sm.add_widget(Wallet(name="wallet"))
        sm.add_widget(Withdraw(name="withdraw"))
        sm.add_widget(Invest(name="invest"))
        sm.add_widget(Game(name="game"))
        sm.add_widget(Admin(name="admin"))
        sm.add_widget(Settings(name="settings"))
        sm.add_widget(Changepassword(name="update_password"))
        sm.add_widget(ChangeEmail(name="update_Email"))
        
        self.connection = mysql.connector.connect(
            host="localhost",         # MySQL host
            user="root",              # MySQL username
            password="",              # MySQL password
            database="user"      # Database where you want to save image path
        )
        self.cursor = self.connection.cursor()
       
        return sm  # Return ScreenManager as root

    def validation(self):
        email1 = self.root.get_screen("registred").ids.registred_email_input.text
        email_regex1 = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_regex1, email1):
            self.root.get_screen("registred").ids.registred_email_input.helper_text = ""
            self.root.get_screen("registred").ids.registred_email_input.error = False
             # Switch to the login screen
            # Clear fields on login screen
            self.clear_login_fields()
            print("Valid email")
            return True
        else:
            self.root.get_screen("registred").ids.registred_email_input.helper_text = "Invalid email"
            self.root.get_screen("registred").ids.registred_email_input.error = True
            print("Invalid email")
            return False
    def signup(self):
    # Get input values from the registration screen
        email = self.root.get_screen("registred").ids.registred_email_input.text
        firstname = self.root.get_screen("registred").ids.registred_firstname_input.text
        lastname = self.root.get_screen("registred").ids.registred_lastname_input.text
        username = self.root.get_screen("registred").ids.registred_username_input.text
        password = self.root.get_screen("registred").ids.registred_password_input.text
        self.connection = mysql.connector.connect(
            host="localhost",         # MySQL host
            user="root",              # MySQL username
            password="",              # MySQL password
            database="user"      # Database where you want to save image path
        )
        self.cursor = self.connection.cursor()

        # Check if any fields are empty
        if not email or not firstname or not lastname or not username or not password:
            error = self.root.get_screen("registred").ids.registred_error_input.text="Please fill all the fields"
           
            print("Please fill all the fields.")
            return

        # Insert into MySQL database
        try:
           
            self.cursor.execute("""INSERT INTO user (email, firstname, lastname, username, password)
                VALUES (%s, %s, %s, %s, %s)""", (email, firstname, lastname, username, password))
            self.conn.commit()  # Commit the transaction to the database

            print(f"User {email} successfully registered!")
            
            # Reset the form fields after successful registration
            self.root.get_screen("registred").ids.registred_email_input.text = ""
            self.root.get_screen("registred").ids.registred_firstname_input.text = ""
            self.root.get_screen("registred").ids.registred_lastname_input.text = ""
            self.root.get_screen("registred").ids.registred_username_input.text = ""
            self.root.get_screen("registred").ids.registred_password_input.text = ""
            self.root.current = "login" 
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            # You could show an error message to the user here if needed
    
      
    def open_logout_cancel(self):
       self.root.get_screen("settings").ids.settings_logout.opacity = 0
       
    def on_stop(self):
        # Close the database connection when the app stops
        self.conn.close()
    def create_logout_card(self):
        # Create MDCard container
        card = MDCard(
            size_hint=(None, None),
            size=("280dp", "100dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            
        )

        # Create a label to add inside the card
        

        # Create a BoxLayout to hold the buttons inside the card
        button_box = BoxLayout(
            orientation='horizontal',  # Arrange buttons horizontally
           
            size_hint=(None, None),
            size=("380dp", "100dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            padding="30dp"
            
        )
        label = MDLabel(
            text="Logout for your account..?",
            theme_text_color="Primary",
            size_hint=(None, None),
            size=("280dp", "50dp"),
           
        )
        button_box2 = BoxLayout(
            orientation='horizontal',  # Arrange buttons horizontally
            
            size_hint=(None, None),
            size=("380dp", "-470dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            padding="-280dp"
        )

        # Create the Cancel button
        cancel_button = MDFlatButton(
            text="Cancel",
            size_hint=(None, None),
            font_size=("16dp"),
            size=("380dp", "10dp"),
            on_release=lambda x: self.remove_card(card)  # Add functionality
        )
        button_box3 = BoxLayout(
            orientation='horizontal',  # Arrange buttons horizontally
            padding="-580dp",
            size_hint=(None, None),
            size=("280dp", "-1070dp"),
            
            pos_hint={"center_x": 0.5, "center_y": 0.6},
        )
        # Create the Logout button
        logout_button = MDFlatButton(
            text="Logout",
            size_hint=(None, None),
            size=("130dp", "40dp"),
            font_size=("16dp"),
            theme_text_color=("Custom"),
                
          
            text_color=(1,0,0,1),
            
            on_release=lambda x: self.switch_to_login(card) 
          
        )

        # Add the buttons to the BoxLayout
        button_box2.add_widget(cancel_button)
        button_box3.add_widget(logout_button)
        button_box.add_widget(label)

        # Add the label and button_box (with buttons) to the card
        
        card.add_widget(button_box)
        card.add_widget(button_box2)
        card.add_widget(button_box3)
        
        self.root.get_screen("settings").ids.change_email.disabled=True

# Disable the button
        self.root.get_screen("settings").ids.change_email.disabled_color=(0,0,0,1)

        # Set the disabled background color to white
        self.root.get_screen("settings").ids.change_email.md_bg_color_disabled = (0.96, 0.96, 0.96, 1 )

        # Set the disabled text color to a desired color (e.g., gray)
       
       
        self.root.get_screen("settings").add_widget(card)
    def remove_card(self, card):
        # Remove the card from the screen
        self.root.get_screen("settings").remove_widget(card)
        self.root.get_screen("settings").ids.change_email.disabled=False
        print("Card removed")
        
        # Add the card to the layout
        
       
       
    def validation1(self):
         email = self.root.get_screen("login").ids.username_input.text
         email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
         phone_regex = r'^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'
         
         if re.match(email_regex, email) or re.match(phone_regex, email):
            self.root.get_screen("login").ids. login_validation.text = ""
            
            print("Valid email")
            return True
            
         else:
            self.root.get_screen("login").ids.login_validation.text = "Invalid Credentials"
            self.root.get_screen("login").ids.login_validation.text_color = 1, 0, 0, 1  # Red color
            print("Invalid email")
            return False  

    def password(self):
        password = self.root.get_screen("login").ids.password_input.text
        if password == "":
            self.root.get_screen("login").ids.password_validation.text = "Invalid Password"
            self.root.get_screen("login").ids.password_validation.text_color=1,0,0,1
            
            print("Invalid password")
            return False
        else:
            self.root.get_screen("login").ids.password_input.helper_text = ""
            
            print("Valid password")
            return True
    

    def switch_to_dashboard(self):
    # Retrieve the email and password from the login screen inputs
        email = self.root.get_screen("login").ids.username_input.text
        password = self.root.get_screen("login").ids.password_input.text
        phonenumber=self.root.get_screen("login").ids.username_input.text
        if not email or not password:
            self.root.get_screen("login").ids.login_error_data.text = "Please fill the fields."

            Clock.schedule_once(self.clear_error_message, 5)
            print("it is empty fields")

        else:
        # Execute the SQL query to validate the credentials
            self.root.get_screen("login").ids.login_error_data.text = ""
            self.cursor.execute("""
            SELECT * FROM user
            WHERE (email=%s OR phonenumber=%s) AND password=%s
        """, (email, phonenumber, password))
            result = self.cursor.fetchone()

            # Check if the result is valid (i.e., user found)
            if result:
                # If valid credentials, switch to the "dashboard" screen
                self.root.current = "dashboard"
                print("sucessfully go to dashboard")
            else:
                # If invalid credentials, show the error message in the login screen
                self.root.get_screen("login").ids.login_error_input.text = "The login details you entered did not match any account..."
                self.root.get_screen("login").ids.login_error_card.opacity = 1 
                self.root.get_screen("login").ids.login_error_card.md_bg_color = 0.9, 0.9, 0.9, 1  # Set background color to light gray
               
                print("Invalid login credentials")
    
    def dashboard(self):
    # Fetch email from the dashboard text input
        email = self.root.get_screen("login").ids.username_input.text
        phonenumber = self.root.get_screen("login").ids.username_input.text
        # Debug: Check what email value you're trying to fetch
        print(f"Attempting to fetch username for email: {email}")

        # Execute query to fetch username based on email
        self.cursor.execute(""" SELECT username FROM user WHERE email=%s OR phonenumber=%s""", (email,phonenumber))
        
        # Fetch the result
        result = self.cursor.fetchone()

        # Debug: Check the result from the query
        print(f"Query result: {result}")

        if result and result[0]:
            username = result[0]
            # Debug: Print the username being set
            print(f"Fetched username: {username}")
            
            # Set the text of the dashboard to welcome the user
            self.root.get_screen("dashboard").ids.dashboard_id.text = f"Hello, {username}"
        else:
            # Handle case where no result is found
            print("No matching user found or username is empty.")
            self.root.get_screen("dashboard").ids.dashboard_id.text = "User not found"


          

    def clear_error_message(self, dt):
        # Clear the error message
        self.root.get_screen("login").ids.login_error_data.text = ""
    def switch_to_admin(self):
        email = self.root.get_screen("login").ids.username_input.text
        password = self.root.get_screen("login").ids.password_input.text
        if email=="anv@gmail.com" and password=="ram123":
            self.root.current="admin"
            self.root.get_screen("login").ids.login_error_input.text = ""
            self.root.get_screen("login").ids.login_error_card.opacity = 0
            self.root.get_screen("login").ids.login_error_card.md_bg_color = 0,0,0,0
            print("successfully login")
    def switch_to_login(self,card):
       
        self.root.current="login"
        self.root.get_screen("login").ids.username_input.text = ""
        self.root.get_screen("login").ids.password_input.text = ""
        self.root.get_screen("login").ids.login_error_input.text = ""
        self.root.get_screen("login").ids.login_error_card.opacity = 0
        self.root.get_screen("settings").remove_widget(card)
        
      
    def settingslogout(self):
      self.root.get_screen("settings").ids.settings_logout.opacity = 1 
  
    def switch_to_setting(self):
   
            self.root.current = "settings"  
            print("settings")
    def switch_to_dashboard1(self):
        self.root.current = "dashboard"
    def switch_to_registred(self):
        self.root.current = "registred"  # Switch to the registered screen
    def switch_to_changepassword(self):
        
        self.root.current="update_password"
        
        print("ramkishore")
    def switch_to_changepassword(self):
        
        self.root.current="update_Email"
    

    def clear_login_fields(self):
        # Reset login screen fields
        self.root.get_screen("login").ids.username_input.text = ""
        self.root.get_screen("login").ids.password_input.text = ""
        self.root.get_screen("login").ids.username_input.helper_text = ""
        self.root.get_screen("login").ids.username_input.error = False
        self.root.get_screen("login").ids.password_input.helper_text = ""
        self.root.get_screen("login").ids.password_input.error = False
    def clear_registred_fields(self):
         # Reset the form fields after successful registration
        self.root.get_screen("registred").ids.registred_email_input.text = ""
        self.root.get_screen("registred").ids.registred_firstname_input.text = ""
        self.root.get_screen("registred").ids.registred_lastname_input.text = ""
        self.root.get_screen("registred").ids.registred_username_input.text = ""
        self.root.get_screen("registred").ids.registred_password_input.text = ""
        self.root.get_screen("registred").ids.registred_error_input.text=""

    def on_image_touch_up(self, instance, touch):
        
      if instance.collide_point(*touch.pos):
        self.select_image()


    def select_image(self):
        # Use Plyer to open the file chooser
        filechooser.open_file(filters=["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif"],
        on_selection=self.update_image
          )
        

    def update_image(self, selection):
    # This function is called when a file is selected
        if selection:
            # Make sure we use the correct 'id' reference for the Image widget
            self.root.get_screen("dashboard").ids.profile_picture_2.source = selection[0]  # Update the image source
            print(f"Image updated to: {selection[0]}")
        else:
            print("No image selected!")
    def switch_to_Wallet(self,instance, touch):
        if instance.collide_point(*touch.pos):  # Checks if the touch occurred within the bounds of the image
            self.root.current = "wallet"  # Switch to the wallet screen
            print("Switched to Wallet Screen")
    def switch_to_withdraw(self,instance, touch):
        if instance.collide_point(*touch.pos):  # Checks if the touch occurred within the bounds of the image
            self.root.current = "withdraw"  # Switch to the wallet screen
            print("Switched to Withdraw Screen")   
    def switch_to_invest(self):
       # Checks if the touch occurred within the bounds of the image
            self.root.current = "invest"  # Switch to the wallet screen
            print("Switched to invest Screen")   
    def switch_to_Game(self):
       # Checks if the touch occurred within the bounds of the image
            self.root.current = "game"  # Switch to the wallet screen
            print("Switched to invest Screen")     
    Builder.load_string(kv)

if __name__ == "__main__":
 Ram().run()
