# Анализ эмулятора SDM4055A-SC

Документ содержит анализ соответствия поведения эмулятора [`hardware/simulator.py`](../hardware/simulator.py) реальным командам SCPI из [`doc/SCPI_Commands_Reference.md`](SCPI_Commands_Reference.md).

## Обзор

Эмулятор `VisaSimulator` предназначен для разработки без реального оборудования. Он имитирует поведение API `VisaInterface`, но не реализует реальные SCPI команды.

---

## Несоответствия и проблемы

### 1. Критическая ошибка в методе `read_measurement()`

**Файл:** [`hardware/simulator.py:90`](../hardware/simulator.py:90)

**Проблема:**
```python
# Текущий код (строки 88-92)
noise = random.uniform(-self._noise_level, self._noise_level)
value = self._base_value + noise  # ОШИБКА: self._base_value не определена
```

**Описание:** Переменная `self._base_value` не определена в классе. Это вызовет `AttributeError` при попытке чтения измерения.

**Решение:**
```python
# Исправленный код
noise = random.uniform(-self._noise_level, self._noise_level)
# Используем базовое значение для DC напряжения по умолчанию
base_value = self._base_values.get(MeasurementType.VOLTAGE_DC, 5.0)
value = base_value + noise
```

---

### 2. Отсутствие команды `*IDN?`

**Проблема:** Эмулятор не реализует метод для получения идентификационной информации устройства.

**Реальное поведение SCPI:** Команда `*IDN?` возвращает строку в формате `производитель,модель,серийный_номер,версия`.

**Текущее состояние:** Метод `get_device_address()` возвращает фиксированную строку `"USB0::0x1AB1::0x04CE::SIMULATOR::INSTR"`, но нет метода `get_device_info()` как в реальном интерфейсе.

**Рекомендация:** Добавить метод `get_device_info()` в эмулятор:

```python
def get_device_info(self) -> Dict[str, str]:
    """
    Get simulated device information.
    
    Returns:
        Dictionary with simulated device information.
    """
    if not self._connected:
        return {}
    
    return {
        'manufacturer': 'SIGLENT',
        'model': 'SDM4055A-SC',
        'serial_number': 'SIMULATOR',
        'version': '1.00',
        'address': self.resource_string,
        'idn': 'SIGLENT,SDM4055A-SC,SIMULATOR,1.00'
    }
```

---

### 3. Отсутствие команды `list_available_resources()`

**Проблема:** Эмулятор не реализует метод для списка доступных VISA ресурсов.

**Реальное поведение SCPI:** Метод `list_available_resources()` возвращает список всех доступных VISA ресурсов.

**Текущее состояние:** Метод отсутствует в эмуляторе.

**Рекомендация:** Добавить метод `list_available_resources()` в эмулятор:

```python
def list_available_resources(self) -> List[str]:
    """
    List simulated available VISA resources.
    
    Returns:
        List of simulated VISA resource strings.
    """
    with QMutexLocker(self._mutex):
        # Возвращаем фиктивный список ресурсов
        return [
            "USB0::0x1AB1::0x04CE::SIMULATOR::INSTR"
        ]
```

---

### 4. Отсутствие реализации команд сканирования (ROUTe)

**Проблема:** Эмулятор не реализует команды для управления сканирующим модулем CS1016:
- `ROUT:SCAN {ON|OFF}`
- `ROUT:FUNC {SCAN|STEP}`
- `ROUT:CHAN <ch>,ON,<type>,AUTO,FAST`
- `ROUT:LIMI:HIGH/LOW`
- `ROUT:COUN`
- `ROUT:START {ON|OFF}`
- `ROUT:START?`
- `ROUT:DATA? <value>`

**Реальное поведение SCPI:** Эти команды используются для настройки и выполнения сканирования 16 каналов.

**Текущее состояние:** Эмулятор использует упрощённый подход - просто читает все каналы последовательно через `read_all_channels()`.

**Рекомендация:** Для более точной эмуляции можно добавить состояние сканирования:

```python
# В __init__ добавить:
self._scan_mode_enabled = False
self._scan_complete = True

# Добавить методы:
def enable_scan_mode(self) -> bool:
    """Enable simulated scan mode."""
    self._scan_mode_enabled = True
    logger.info("Simulator: Scan mode enabled")
    return True

def is_scan_complete(self) -> bool:
    """Check if simulated scan is complete."""
    return self._scan_complete

def start_scan(self) -> bool:
    """Start simulated scan."""
    self._scan_complete = False
    logger.info("Simulator: Scan started")
    return True

def get_scan_data(self, channel_num: int) -> Optional[float]:
    """Get simulated scan data for channel."""
    return self.read_channel_measurement(channel_num)
```

---

### 5. Отсутствие команд инициализации и получения данных

**Проблема:** Эмулятор не реализует команды:
- `INIT` - инициализация измерения
- `FETCh?` - получение данных из памяти
- `READ?` - выполнение измерения и возврат результата

**Реальное поведение SCPI:** Эти команды используются для управления процессом измерения.

**Текущее состояние:** Эмулятор использует упрощённый подход через `read_measurement()` и `read_all_channels()`.

**Примечание:** Для текущей архитектуры проекта это допустимо, так как эмулятор имитирует поведение на уровне API, а не на уровне SCPI команд.

---

### 6. Отсутствие команд конфигурации (CONFigure)

**Проблема:** Метод `set_measurement_function()` в эмуляторе просто логирует вызов и не сохраняет состояние.

**Реальное поведение SCPI:** Команды `CONF:...` настраивают параметры измерения.

**Текущее состояние:**
```python
def set_measurement_function(self, function: str = "VOLT:DC") -> bool:
    logger.info(f"Simulator: Set function to {function}")
    return True
```

**Рекомендация:** Добавить сохранение текущей функции измерения:

```python
# В __init__ добавить:
self._current_function = "VOLT:DC"

def set_measurement_function(self, function: str = "VOLT:DC") -> bool:
    """Set simulated measurement function."""
    self._current_function = function
    logger.info(f"Simulator: Set function to {function}")
    return True

def get_measurement_function(self) -> str:
    """Get current measurement function."""
    return self._current_function
```

---

### 7. Отсутствие команды сброса `*RST`

**Проблема:** Эмулятор не реализует метод для сброса к заводским настройкам.

**Реальное поведение SCPI:** Команда `*RST` сбрасывает все параметры измерения к значениям по умолчанию.

**Текущее состояние:** Метод отсутствует.

**Рекомендация:** Добавить метод `reset()`:

```python
def reset(self) -> None:
    """Reset simulator to default settings."""
    with QMutexLocker(self._mutex):
        self._initialize_channels()
        self._current_function = "VOLT:DC"
        self._scan_mode_enabled = False
        logger.info("Simulator: Reset to defaults")
```

---

## Соответствия (что работает правильно)

### 1. Управление подключением

✅ **Методы:**
- `connect()` - симулирует подключение
- `disconnect()` - симулирует отключение
- `is_connected()` - проверяет статус подключения

**Соответствие:** Правильно имитирует поведение подключения/отключения.

---

### 2. Управление каналами

✅ **Методы:**
- `get_channel_config(channel_num)` - получает конфигурацию канала
- `set_channel_measurement_type(channel_num, measurement_type)` - устанавливает тип измерения для канала
- `switch_channel(channel_num)` - переключение канала

**Соответствие:** Правильно реализует логику:
- Каналы 1-12 поддерживают все типы измерений кроме тока
- Каналы 13-16 поддерживают только измерения тока

**Код:** [`hardware/simulator.py:149-158`](../hardware/simulator.py:149-158)

---

### 3. Чтение измерений с каналов

✅ **Методы:**
- `read_channel_measurement(channel_num)` - чтение измерения с конкретного канала
- `read_all_channels()` - чтение всех каналов

**Соответствие:** Правильно возвращает значения с учётом типа измерения для каждого канала.

**Код:** [`hardware/simulator.py:181-213`](../hardware/simulator.py:181-213)

---

### 4. Базовые значения для типов измерений

✅ **Атрибут:** `_base_values` - содержит базовые значения для всех типов измерений

**Соответствие:** Значения соответствуют ожидаемым диапазонам:
- VOLTAGE_DC: 5.0 В
- VOLTAGE_AC: 3.5 В
- CURRENT_DC: 0.5 А
- CURRENT_AC: 0.3 А
- RESISTANCE_2WIRE: 100.0 Ом
- RESISTANCE_4WIRE: 100.0 Ом
- CAPACITANCE: 1.0e-6 Ф
- FREQUENCY: 1000.0 Гц
- DIODE: 0.7 В
- CONTINUITY: 0.0 Ом
- TEMP_RTD: 25.0 °C
- TEMP_THERMOCOUPLE: 25.0 °C

**Код:** [`hardware/simulator.py:37-50`](../hardware/simulator.py:37-50)

---

### 5. Добавление шума к измерениям

✅ **Реализация:** Использование `random.uniform(-self._noise_level, self._noise_level)` для добавления случайных флуктуаций

**Соответствие:** Правильно имитирует реальные измерения с небольшим шумом.

---

## Приоритет исправлений

### Высокий приоритет (критические ошибки)

1. **Исправить ошибку с `self._base_value`** в [`hardware/simulator.py:90`](../hardware/simulator.py:90)
   - Это вызовет `AttributeError` при попытке чтения измерения

### Средний приоритет (улучшение функциональности)

2. **Добавить метод `get_device_info()`** для совместимости с API реального интерфейса
3. **Добавить метод `list_available_resources()`** для совместимости с API реального интерфейса
4. **Добавить сохранение текущей функции измерения** в `set_measurement_function()`

### Низкий приоритет (улучшение точности эмуляции)

5. **Добавить реализацию команд сканирования (ROUTe)** для более точной эмуляции
6. **Добавить метод `reset()`** для сброса к заводским настройкам

---

## Рекомендации по улучшению эмулятора

### 1. Добавить логирование SCPI команд

Для отладки и понимания поведения эмулятора можно добавить логирование всех "SCPI команд":

```python
def _send_scpi_command(self, command: str) -> None:
    """Log simulated SCPI command."""
    logger.debug(f"Simulator SCPI: {command}")
```

### 2. Добавить режим отладки

Добавить флаг для включения детального логирования:

```python
def __init__(self, resource_string: str = "", debug_mode: bool = False):
    self._debug_mode = debug_mode
    # ... остальной код ...

def _log_debug(self, message: str) -> None:
    """Log debug message if debug mode is enabled."""
    if self._debug_mode:
        logger.debug(f"Simulator DEBUG: {message}")
```

### 3. Добавить симуляцию ошибок

Для тестирования обработки ошибок можно добавить возможность симулировать ошибки:

```python
def simulate_error(self, error_type: str) -> None:
    """
    Simulate a specific error condition.
    
    Args:
        error_type: Type of error to simulate ('connection', 'read', 'scan')
    """
    self._simulated_error = error_type
    logger.warning(f"Simulator: Simulating error: {error_type}")
```

---

## Заключение

Эмулятор `VisaSimulator` в целом хорошо имитирует поведение API `VisaInterface` для целей разработки без реального оборудования. Однако есть одна критическая ошибка, которую необходимо исправить, и несколько улучшений, которые могут повысить точность эмуляции.

### Статус эмулятора

| Аспект | Статус | Приоритет |
|--------|--------|-----------|
| Управление подключением | ✅ Работает | - |
| Управление каналами | ✅ Работает | - |
| Чтение измерений | ❌ Ошибка | Высокий |
| Идентификация устройства | ⚠️ Частично | Средний |
| Список ресурсов | ❌ Отсутствует | Средний |
| Команды сканирования | ⚠️ Упрощено | Низкий |
| Команды конфигурации | ⚠️ Упрощено | Низкий |
| Команда сброса | ❌ Отсутствует | Низкий |

### Общая оценка

Эмулятор пригоден для разработки и тестирования UI, но требует исправления критической ошибки в методе `read_measurement()` перед использованием.
