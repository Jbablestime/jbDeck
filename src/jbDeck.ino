#include <SPI.h>
#include <TFT_eSPI.h>

TFT_eSPI tft = TFT_eSPI();

#define ROWS 3
#define COLS 4
#define CELL_WIDTH  (320 / COLS)
#define CELL_HEIGHT (240 / ROWS)
#define PADDING 6

struct StreamButton {
  String label;
  uint16_t color;
  bool isToggle;
  bool toggleState;
};

StreamButton buttons[12];
bool isConfigured = false;

void setup() {
  Serial.begin(115200);
  delay(1000); 

  tft.init();
  tft.setRotation(3);
  tft.invertDisplay(true);
  tft.fillScreen(TFT_BLACK);

  uint16_t calData[5] = { 300, 3600, 300, 3600, 1 }; 
  tft.setTouch(calData);

  tft.setTextColor(TFT_WHITE);
  tft.setTextDatum(MC_DATUM);
  tft.drawString("Waiting for PC...", 160, 120, 4);

  Serial.println("READY");
}

void loop() {
  if (Serial.available()) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();
    
    // CFG:ID:LABEL:COLOR:TOGGLE
    if (msg.startsWith("CFG:")) {
      int split1 = msg.indexOf(':', 4);
      int split2 = msg.indexOf(':', split1 + 1);
      int split3 = msg.indexOf(':', split2 + 1);

      if (split1 > 0 && split2 > 0 && split3 > 0) {
        int id = msg.substring(4, split1).toInt();
        String label = msg.substring(split1 + 1, split2);
        uint16_t color = msg.substring(split2 + 1, split3).toInt();
        bool isToggle = msg.substring(split3 + 1).toInt() == 1;

        if (id >= 0 && id < 12) {
          buttons[id] = {label, color, isToggle, false};
        }
      }
    } 

    else if (msg == "CFG_DONE") {
      tft.fillScreen(TFT_BLACK);
      drawAllButtons();
      isConfigured = true;
    }
  }

  if (isConfigured) {
    uint16_t x, y;
    if (tft.getTouch(&x, &y)) {
      x = 320 - x;
      y = 240 - y;

      int col = x / CELL_WIDTH;
      int row = y / CELL_HEIGHT;

      if (col >= 0 && col < COLS && row >= 0 && row < ROWS) {
        int btnIndex = (row * COLS) + col;

        if (buttons[btnIndex].isToggle) {
          buttons[btnIndex].toggleState = !buttons[btnIndex].toggleState;
        }

        drawButton(btnIndex, true);

        Serial.print("BTN_DOWN:");
        Serial.println(btnIndex);

        while (tft.getTouch(&x, &y)) { delay(10); }

        Serial.print("BTN_UP:");
        Serial.println(btnIndex);

        drawButton(btnIndex, false);
        delay(150); 
      }
    }
  }
}

void drawAllButtons() {
  for (int i = 0; i < 12; i++) {
    drawButton(i, false);
  }
}

void drawButton(int index, bool isPressed) {
  int col = index % COLS;
  int row = index / COLS;

  int xPos = (col * CELL_WIDTH) + PADDING;
  int yPos = (row * CELL_HEIGHT) + PADDING;
  int bWidth = CELL_WIDTH - (PADDING * 2);
  int bHeight = CELL_HEIGHT - (PADDING * 2);

  bool showOutline = isPressed || (buttons[index].isToggle && buttons[index].toggleState);

  uint16_t bgColor = buttons[index].color;
  uint16_t outlineColor = showOutline ? TFT_WHITE : bgColor;

  tft.fillRoundRect(xPos, yPos, bWidth, bHeight, 8, bgColor);
  
  if (showOutline) {
    tft.drawRoundRect(xPos, yPos, bWidth, bHeight, 8, outlineColor);
    tft.drawRoundRect(xPos+1, yPos+1, bWidth-2, bHeight-2, 7, outlineColor);
  }

  tft.setTextColor(TFT_WHITE);
  tft.setTextDatum(MC_DATUM);
  tft.drawString(buttons[index].label, xPos + (bWidth / 2), yPos + (bHeight / 2), 2);
}