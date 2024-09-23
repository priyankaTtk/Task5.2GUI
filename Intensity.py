import tkinter as tk
import RPi.GPIO as GPIO

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define GPIO pins for LEDs
LED_PINS = {'red': 17, 'green': 27, 'blue': 22}

# Setup pins
for pin in LED_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def turn_on_led(color):
    """ Turn on the selected LED and turn off others. """
    for led_color, pin in LED_PINS.items():
        GPIO.output(pin, GPIO.HIGH if led_color == color else GPIO.LOW)

def cleanup():
    """ Clean up GPIO settings and quit the application. """
    GPIO.cleanup()
    root.destroy()

class LEDControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LED Control")
        self.root.geometry("300x250")  # Adjusted size for better spacing
        self.root.configure(bg='#ecf0f1')  # Light gray background

        self.selected_led = tk.StringVar()
        self.selected_led.set(None)

        font = ('Helvetica', 12)
        button_font = ('Helvetica', 12, 'bold')

        # Create a main frame
        main_frame = tk.Frame(root, bg='#2c3e50', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Title
        title_label = tk.Label(main_frame, text="LED Control Panel", font=('Helvetica', 18, 'bold'), bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=10)

        # Create radio buttons for each LED
        radio_frame = tk.Frame(main_frame, bg='#2c3e50')
        radio_frame.pack(pady=10)

        self.red_radio = tk.Radiobutton(
            radio_frame,
            text="Red LED",
            variable=self.selected_led,
            value='red',
            bg='#ecf0f1',
            fg='red',
            command=self.update_led,
            font=font
        )
        self.red_radio.pack(side=tk.LEFT, padx=5)

        self.green_radio = tk.Radiobutton(
            radio_frame,
            text="Green LED",
            variable=self.selected_led,
            value='green',
            bg='#ecf0f1',
            fg='green',
            command=self.update_led,
            font=font
        )
        self.green_radio.pack(side=tk.LEFT, padx=5)

        self.blue_radio = tk.Radiobutton(
            radio_frame,
            text="Blue LED",
            variable=self.selected_led,
            value='blue',
            bg='#ecf0f1',
            fg='blue',
            command=self.update_led,
            font=font
        )
        self.blue_radio.pack(side=tk.LEFT, padx=5)
	
        #Createintensity sliders for each LED
        slider_frame = tk.Frame(main_frame,bg='#2c3e50')
        slider_frame.pack(pady=10)
        
        self.red_slider = tk.Scale(
            slider_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            label="Red Intensity",
            bg='#ecf0f1',
            fg='red',
            font=font,
            command=self.update_intensity
        )
        self.red_slider.pack(side=tk.LEFT, padx=5)
        
        self.green_slider = tk.Scale(
            slider_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            label="Green Intensity",
            bg='#ecf0f1',
            fg='green',
            font=font,
            command=self.update_intensity
        )
        self.green_slider.pack(side=tk.LEFT, padx=5)
        
        self.blue_slider = tk.Scale(
            slider_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            label="Blue Intensity",
            bg='#ecf0f1',
            fg='blue',
            font=font,
            command=self.update_intensity
        )
        self.blue_slider.pack(side=tk.LEFT, padx=5)

        # Create Exit button
        tk.Button(
            main_frame,
            text="Exit",
            command=self.exit_app,
            font=button_font,
            bg='#e74c3c',
            fg='white',
            padx=10,
            pady=5,
            relief='raised'
        ).pack(pady=20)

        # Handle window close event
        root.protocol("WM_DELETE_WINDOW", self.exit_app)
        
        #Initialize PWM objects
        self.red_pwm = GPIO.PWM(LED_PINS['red'],50)
        self.green_pwm = GPIO.PWM(LED_PINS['green'],50)
        self.blue_pwm = GPIO.PWM(LED_PINS['blue'],50)
        
        self.red_pwm.start(0)
        self.green_pwm.start(0)
        self.blue_pwm.start(0)
    
    def turn_off_all_leds(self):
        self.red_pwm.ChangeDutyCycle(0)
        self.green_pwm.ChangeDutyCycle(0)
        self.blue_pwm.ChangeDutyCycle(0)

    def update_led(self):
        color = self.selected_led.get()
        if color:
            intensity = self.get_intensity(color)
            self.set_led_intensity(color, intensity)
        else:
            self.turn_off_all_leds()
    
    def get_intensity(self, color):
        if color == 'red':
            return self.red_slider.get()
        elif color == 'green':
            return self.green_slider.get()
        elif color == 'blue':
            return self.blue_slider.get()
    
    def set_led_intensity(self, color, intensity):
        if color == 'red':
            self.red_pwm.ChangeDutyCycle(intensity)
        elif color == 'green':
            self.green_pwm.ChangeDutyCycle(intensity)
        elif color == 'blue':
            self.blue_pwm.ChangeDutyCycle(intensity)
    
    def update_intensity(self, value):
        color = self.selected_led.get()
        if color:
            self.set_led_intensity(color, int(value))
            
    def exit_app(self):
        GPIO.cleanup()
        self.root.destroy()

# Main code
if __name__ == "__main__":
    root = tk.Tk()
    app = LEDControlApp(root)
    root.mainloop()
