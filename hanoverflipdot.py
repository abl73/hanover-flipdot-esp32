esphome:
  name: hanover
  friendly_name: Hanover

esp32:
  board: esp32dev
  framework:
    type: arduino

logger:
#  level: DEBUG  # Enable debug logging to capture potential issues

ota:
  platform: esphome
  password: <"..."> #will get updated when an esp32 is added to esphome

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  manual_ip:
    static_ip: <replace by ip address esp32>
    gateway: <replace by gateway>
    subnet: <replace by subnet>

font:
  - file: "hanover6x8.ttf"
    id: hanover_font
    size: 8
  - file: "pixel8.ttf"
    id: pixel8_font
    size: 8

external_components:
  - source:
      type: local
      path: custom_components

uart:
  - id: uart_0
    tx_pin: GPIO2 #replace by pin on esp32 that connects to data-in of hanover display
    baud_rate: 4800

display:
  - platform: hanover_flipdot
    id: flipdot1
    uart_id: uart_0
    width: 84 #width of the hanover display
    height: 8 #height of the hanover display
    address: 0x02 #replace by dial number flipdot + 1
    offset: 0

    pages:
      - id: mqtt_text
        lambda: |-
          if (id(mqtt_text_sensor).has_state()) {
            std::string text = id(mqtt_text_sensor).state;
            ESP_LOGD("mqtt_text", "Received message: '%s'", text.c_str());
            
            int x = 0;  // Starting x-coordinate for text rendering

            while (!text.empty()) {
              size_t start_bracket = text.find('[');
              size_t end_bracket = text.find(']');

              // If there's no bracket, just render the remaining text
              if (start_bracket == std::string::npos) {
                ESP_LOGD("mqtt_text", "Rendering remaining text: '%s'", text.c_str());
                it.printf(x, 0, id(hanover_font), text.c_str());
                break;  // Exit loop after rendering the rest of the text
              }

              // Handle text before the first bracket
              if (start_bracket > 0) {
                std::string before_bracket = text.substr(0, start_bracket);
                ESP_LOGD("mqtt_text", "Rendering before bracket: '%s'", before_bracket.c_str());
                it.printf(x, 0, id(hanover_font), before_bracket.c_str());
                x += before_bracket.length() * 6;  // Move x-coordinate forward
                text = text.substr(start_bracket);  // Update text to start from the bracket
              }

              // Now handle text inside the bracket
              if (start_bracket != std::string::npos && end_bracket != std::string::npos && end_bracket > start_bracket) {
                std::string in_bracket = text.substr(start_bracket + 1, end_bracket - start_bracket - 1);
                ESP_LOGD("mqtt_text", "Rendering inside bracket: '%s'", in_bracket.c_str());
                it.printf(x, 0, id(pixel8_font), in_bracket.c_str());
                x += in_bracket.length() * 6;  // Move x-coordinate forward
                text = text.substr(end_bracket + 1);  // Remove the processed part
              } else {
                // In case there are no valid brackets, render the remaining text normally
                ESP_LOGD("mqtt_text", "Rendering remaining text without brackets: '%s'", text.c_str());
                it.printf(x, 0, id(hanover_font), text.c_str());
                break;  // Exit loop after rendering the rest of the text
              }
            }
          } else {
            ESP_LOGD("mqtt_text", "No message received, displaying default text");
            it.printf(0, 0, id(hanover_font), "Default Text");
          }

mqtt:
  broker: <ip-address mqtt broker>
  port: 1883
  username: <username mqtt>
  password: <password mqtt>
  on_message:
    - topic: "<mqtt topic>"
      then:
        - text_sensor.template.publish:
            id: mqtt_text_sensor
            state: !lambda |-
              return x;
        - component.update: flipdot1

text_sensor:
  - platform: template
    id: mqtt_text_sensor
    name: "MQTT Text"
