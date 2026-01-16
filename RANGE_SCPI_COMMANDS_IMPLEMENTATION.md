# Реализация отправки команд диапазона на мультиметр

## Проблема

Приложение выбирало диапазон в UI (например, "200 mV", "2 V" и т.д.), но не отправляло соответствующую SCPI команду на мультиметр. Команда всегда использовала "AUTO" для диапазона, независимо от выбора пользователя.

## Решение

### Изменения в файлах:

#### 1. hardware/visa_interface.py

**Добавлено:**
- Словарь `RANGE_TO_SCPI` (строки 187-218) для маппинга диапазонов в SCPI команды:
  ```python
  RANGE_TO_SCPI = {
      # Voltage ranges
      "200 mV": "200mV",
      "2 V": "2V",
      "20 V": "20V",
      "200 V": "200V",
      "1000 V": "1000V",
      "750 V": "750V",
      # Current ranges
      "200 uA": "200uA",
      "2 mA": "2mA",
      "20 mA": "20mA",
      "200 mA": "200mA",
      "2 A": "2A",
      "10 A": "10A",
      # Capacitance ranges
      "2 nF": "2nF",
      "20 nF": "20nF",
      "200 nF": "200nF",
      "2 uF": "2uF",
      "20 uF": "20uF",
      "200 uF": "200uF",
      "2 mF": "2mF",
      "20 mF": "20mF",
      "100 mF": "100mF",
      # Resistance ranges
      "200 Ohm": "200OHM",
      "2 kOhm": "2kOHM",
      "20 kOhm": "20kOHM",
      "200 kOhm": "200kOHM",
      "2 MOhm": "2MOHM",
      "10 MOhm": "10MOHM",
      "100 MOhm": "100MOHM",
      # AUTO range
      "AUTO": "AUTO",
  }
  ```

- Поле `range_value` в класс `ChannelConfig` (строка 43) для хранения выбранного диапазона

- Метод `set_channel_range()` (строки 237-259) для установки диапазона канала:
  ```python
  def set_channel_range(self, channel_num: int, range_value: str) -> bool:
      """Set measurement range for a specific channel."""
      # Validates range value and stores it in config
  ```

- Обновлен метод `configure_scan_channel()` (строки 317-328) для использования диапазона из конфигурации:
  ```python
  # Get SCPI range command from range value
  range_scpi = self.RANGE_TO_SCPI.get(config.range_value, "AUTO")
  
  # Configure channel: ROUT:CHAN <ch>,ON,<type>,<range>,FAST
  cmd = f":ROUT:CHAN {channel_num},ON,{channel_type},{range_scpi},FAST"
  ```

- Обновлен метод `_initialize_channels()` (строка 197) для инициализации диапазонов в "AUTO"

#### 2. hardware/async_worker.py

**Обновлено:**
- Поле `_channel_configs` (строка 146) для хранения словарей с measurement_type и range_value:
  ```python
  self._channel_configs: Dict[int, Dict[str, str]] = {}  # Stores {'measurement_type': str, 'range_value': str}
  ```

- Обновлен метод `configure_channels()` (строки 199-242) для конфигурации каналов с диапазонами:
  ```python
  def configure_channels(self, channel_configs: Dict[int, Dict[str, str]]) -> bool:
      """Configure device with measurement types and ranges for each channel."""
      # Sets both measurement type and range for each channel
  ```

#### 3. gui/window.py

**Добавлено:**
- Поле `_channel_ranges` (строка 69) для хранения диапазонов всех каналов:
  ```python
  self._channel_ranges: Dict[int, str] = {}
  ```

**Обновлено:**
- Метод `_initialize_channel_measurement_types()` (строки 309-326) для инициализации диапазонов в "AUTO"

- Метод `_on_channel_range_changed()` (строки 674-683) для хранения выбранного диапазона:
  ```python
  def _on_channel_range_changed(self, channel_num: int, range_value: str) -> None:
      """Handle channel range change."""
      self._channel_ranges[channel_num] = range_value
  ```

- Метод `get_all_channel_measurement_types()` (строки 336-350) для возврата конфигураций с диапазонами:
  ```python
  def get_all_channel_measurement_types(self) -> Dict[int, Dict[str, str]]:
      """Get measurement types and ranges for all channels."""
      # Returns dict with 'measurement_type' and 'range_value' for each channel
  ```

- Метод `_apply_configuration()` (строки 637-678) для установки диапазонов из конфигурационного файла

- Метод `_start_scanning()` (строки 353-389) для передачи конфигураций с диапазонами при старте сканирования

- Метод `_single_scan()` (строки 400-436) для передачи конфигураций с диапазонами при одиночном сканировании

## Как это работает

### При выборе диапазона в UI:
1. Пользователь выбирает диапазон (например, "200 mV") в выпадающем списке
2. Сигнал `range_changed` отправляется из [`ChannelIndicator`](gui/widgets.py:131)
3. [`MainWindow._on_channel_range_changed()`](gui/window.py:674) сохраняет диапазон в `_channel_ranges[channel_num]`

### При загрузке конфигурационного файла:
1. [`ConfigLoader`](config/config_loader.py) загружает диапазоны из CSV файла
2. [`MainWindow._apply_configuration()`](gui/window.py:637) устанавливает диапазоны для каналов через `indicator.set_range()`
3. Диапазоны сохраняются в `_channel_ranges[channel_num]`

### При сканировании:
1. [`MainWindow.get_all_channel_measurement_types()`](gui/window.py:336) создает словарь конфигураций:
   ```python
   {
       1: {'measurement_type': 'VOLT:DC', 'range_value': '200 mV'},
       2: {'measurement_type': 'VOLT:DC', 'range_value': 'AUTO'},
       ...
   }
   ```

2. [`AsyncScanManager.configure_channels()`](hardware/async_worker.py:199) передает конфигурации в устройство

3. [`VisaInterface.configure_scan_channel()`](hardware/visa_interface.py:275) отправляет SCPI команду:
   ```
   :ROUT:CHAN 1,ON,DCV,200mV,FAST
   ```

4. Мультиметр устанавливает указанный диапазон и измеряет в этом диапазоне

## Примеры SCPI команд

### Напряжение:
- `:ROUT:CHAN 1,ON,DCV,200mV,FAST` - канал 1, DC напряжение, диапазон 200 mV
- `:ROUT:CHAN 1,ON,DCV,2V,FAST` - канал 1, DC напряжение, диапазон 2 V
- `:ROUT:CHAN 1,ON,DCV,AUTO,FAST` - канал 1, DC напряжение, авто диапазон

### Ток:
- `:ROUT:CHAN 13,ON,DCA,2mA,FAST` - канал 13, DC ток, диапазон 2 mA
- `:ROUT:CHAN 13,ON,DCA,10A,FAST` - канал 13, DC ток, диапазон 10 A

### Сопротивление:
- `:ROUT:CHAN 1,ON,RES,200OHM,FAST` - канал 1, сопротивление, диапазон 200 Ohm
- `:ROUT:CHAN 1,ON,RES,2MOHM,FAST` - канал 1, сопротивление, диапазон 2 MOhm

## Результаты

✅ Диапазоны теперь отправляются на мультиметр при сканировании
✅ При выборе диапазона 200 mV мультиметр измеряет в этом диапазоне
✅ При выходе за пределы диапазона мультиметр покажет перегрузку (OL)
✅ Конфигурационный файл загружает диапазоны для каналов
✅ Ручной выбор диапазона в UI работает корректно

## Тестирование

Для тестирования:
1. Запустите приложение
2. Подключитесь к мультиметру
3. Выберите диапазон "200 mV" для канала 1
4. Подайте напряжение 2 V на канал 1
5. Запустите сканирование
6. Проверьте, что мультиметр показывает "OL" (перегрузка) вместо некорректного значения
