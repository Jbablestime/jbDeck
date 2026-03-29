# jbDeck
A Stream Deck alternative for the ESP32 SoC MCU.


# Setup
> [!IMPORTANT]
> Ensure you have the `esp32` boards by **Espressif Systems** in your Board Manager. 


## Setting up your ESP32
1. Open [Arduino IDE](https://www.arduino.cc/en/software/), and open up the `jbDeck.ino` sketch. 
2. Plug in your ESP32 with a compatible SPI TFT screen. (Required by the TFT_eSPI library).
3. Press the **Upload** button near the top-left of the screen, and wait for it to be done flashing.

You can keep the ESP32 plugged in, it will not damage anything while you do the next steps.

You're complete! Continue onto [**Setting up your Computer and Prepping your jbDeck**](https://github.com/Jbablestime/jbDeck?tab=readme-ov-file#setting-up-your-computer-and-prepping-your-jbdeck).


## Setting up your Computer and Prepping your jbDeck
> [!NOTE]
> You can compile the script into an executable using the Pyinstaller python library, or you could run the script without compilation. There is no difference except packaging libraries.

- Ensure you've installed, and extracted the zip before continuing on.
- Ensure you've installed the `requirements.txt` beforehand to ensure a smooth experience.


### Preconfiguration
- Open the `config.json` file

You will see buttons structured like this:
```json
{
  "id": 0,
  "label": "Mute Mic",
  "color": "DARKGRAY",
  "isToggle": true,
  "action_type": "hotkey",
  "action": "f13"
}
```

**ID**: The position of your buttons depend on which ID it holds. The example above shows the button in the ID `0`, this is the first position of the grid. The last position of the grid is ID `11`, 12 total configurable buttons.

**LABEL**: This is the text which appears on top of your button, it helps represent what the button does for you in your jbDeck.

**COLOR**: Setting the color key value will change the background color of your button, currently it supports 15 colors, but you can add support for further colors simply by changing the `main.py`.

**isTOGGLE**: `isToggle` is for buttons you connect to toggle functions, like muting a microphone. A white outline will appear around your button, marking it as active, pressing the button again will mark it as inactive, like unmuting your microphone.

<details>
  <summary>
    <b>ACTION_TYPE</b>: The <code>action_type</code> key value is for 1 of the 3 actions jbDeck currently supports. <code>hotkey</code>, <code>command</code>, and <code>hold_command</code>.
  </summary>

  
  <br>
  <code>hotkey</code>: Simulates a keyboard button press, in the example above that key is <code>F13</code>.<br>
  <br>
  <code>command</code>: Runs a console command in your terminal, this can be used to open applications, lock or shutdown your computer, and other things.<br>
  <br>
  <code>hold_command</code>: This functions primarily the same way as command does, except in order to accutuate the button, you're required to hold it in for 5 seconds. This is better used for shutting down your computer.<br>
  <br>
</details>

**ACTION**: This is the command or keyboard hotkey you want to be executed/pressed. Hotkeys should follow the [Keyboard Library for Python](https://pypi.org/project/keyboard/).

### Configuring the COM port
- Open the `main.py`, edit line 9 to mirror the COM port your ESP32 is plugged into. (Ex. COM1, COM2, COM8, etc.)
- Save the file before closing it

### Starting the Script
- Open your command prompt and `cd` into the project directory.

1. Run `pip install -r requirements.txt` and wait for it to finish
2. Open the `main.py`, it should detect your ESP32 plugged in, and within a few seconds should render your configured buttons.


