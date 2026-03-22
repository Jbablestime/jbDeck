# jbDeck
A Stream Deck alternative for the ESP32 SoC MCU.

# Setup
> [!IMPORTANT]
> Ensure you have the `esp32` boards by **Espressif Systems** in your Board Manager. 

## Setting up your ESP32
1. Open [Arduino IDE](https://www.arduino.cc/en/software/), and open up the `jbDeck.ino` sketch. 
2. Plug in your ESP32 with a compatible SPI TFT screen. (Required by the TFT_eSPI library).
3. Press the **Upload** button near the top-left of the screen, and wait for it to be done flashing.

You're complete! Continue onto Setting up your Computer.

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

**Pre-supported Colors**
```ts
BLACK
BLUE
CYAN
DARKCYAN
DARKGRAY
DARKGREEN
GREEN
MAGENTA
MAROON
NAVY
ORANGE
PURPLE
RED
WHITE
YELLOW
```

