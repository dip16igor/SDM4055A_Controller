"""
Configuration file loader for SDM4055A-SC multimeter controller.

Supports loading channel configurations from CSV files including:
- Channel number
- Measurement type
- Range (AUTO or specific value)
- Lower threshold
- Upper threshold
"""

import csv
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ChannelThresholdConfig:
    """Configuration for a single channel including thresholds."""
    channel_num: int
    measurement_type: str
    range_value: str
    lower_threshold: Optional[float]
    upper_threshold: Optional[float]

    def is_value_in_threshold(self, value: float) -> bool:
        """
        Check if a value is within the configured thresholds.
        
        Args:
            value: The measured value to check.
            
        Returns:
            True if value is within thresholds (or no thresholds set), False otherwise.
        """
        if self.lower_threshold is None and self.upper_threshold is None:
            return True  # No thresholds configured
        
        if self.lower_threshold is not None and value < self.lower_threshold:
            return False
        
        if self.upper_threshold is not None and value > self.upper_threshold:
            return False
        
        return True


class ConfigLoader:
    """Loader for CSV configuration files."""
    
    # Valid measurement types matching the MeasurementType enum
    VALID_MEASUREMENT_TYPES = {
        "VOLT:DC", "VOLT:AC",
        "CURR:DC", "CURR:AC",
        "RES", "FRES",
        "CAP", "FREQ",
        "DIOD", "CONT",
        "TEMP:RTD", "TEMP:THER"
    }
    
    # Valid ranges for each measurement type
    VALID_RANGES = {
        "VOLT:DC": ["200 mV", "2 V", "20 V", "200 V", "1000 V", "AUTO"],
        "VOLT:AC": ["200 mV", "2 V", "20 V", "200 V", "750 V", "AUTO"],
        "CURR:DC": ["200 uA", "2 mA", "20 mA", "200 mA", "2 A", "10 A", "AUTO"],
        "CURR:AC": ["20 mA", "200 mA", "2 A", "10 A", "AUTO"],
        "RES": ["200 Ohm", "2 kOhm", "20 kOhm", "200 kOhm", "2 MOhm", "10 MOhm", "100 MOhm", "AUTO"],
        "FRES": ["200 Ohm", "2 kOhm", "20 kOhm", "200 kOhm", "2 MOhm", "10 MOhm", "100 MOhm", "AUTO"],
        "CAP": ["2 nF", "20 nF", "200 nF", "2 uF", "20 uF", "200 uF", "2 mF", "20 mF", "100 mF", "AUTO"],
    }
    
    # User-friendly names for measurement types (for validation messages)
    MEASUREMENT_TYPE_NAMES = {
        "VOLT:DC": "DC Voltage",
        "VOLT:AC": "AC Voltage",
        "CURR:DC": "DC Current",
        "CURR:AC": "AC Current",
        "RES": "2-Wire Resistance",
        "FRES": "4-Wire Resistance",
        "CAP": "Capacitance",
        "FREQ": "Frequency",
        "DIOD": "Diode",
        "CONT": "Continuity",
        "TEMP:RTD": "RTD Temperature",
        "TEMP:THER": "Thermocouple"
    }
    
    def __init__(self):
        """Initialize configuration loader."""
        self.configs: Dict[int, ChannelThresholdConfig] = {}
        self.config_file_path: Optional[Path] = None
    
    def load_from_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Load configuration from a CSV file.
        
        Args:
            file_path: Path to the CSV configuration file.
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return False, f"File not found: {file_path}"
            
            if not path.suffix.lower() == '.csv':
                return False, "Configuration file must be a .csv file"
            
            self.configs.clear()
            self.config_file_path = path
            
            with open(path, 'r', encoding='utf-8') as f:
                # Read all lines and filter out comment lines
                lines = []
                for line in f:
                    stripped = line.strip()
                    # Skip empty lines and comment lines
                    if stripped and not stripped.startswith('#'):
                        lines.append(line)
                
                # Create CSV reader from filtered lines
                reader = csv.DictReader(lines)
                
                # Validate required columns
                required_columns = ['channel', 'measurement_type', 'range']
                if not all(col in reader.fieldnames for col in required_columns):
                    return False, f"CSV must contain columns: {', '.join(required_columns)}"
                
                # Parse each row
                for row_num, row in enumerate(reader, start=2):  # Start at 2 (row 1 is header)
                    try:
                        # Skip empty rows
                        channel_str = row.get('channel', '').strip()
                        if not channel_str:
                            continue
                        
                        # Parse channel number
                        try:
                            channel_num = int(channel_str)
                        except ValueError:
                            return False, f"Row {row_num}: Invalid channel number '{channel_str}'"
                        
                        if channel_num < 1 or channel_num > 16:
                            return False, f"Row {row_num}: Channel number must be between 1 and 16"
                        
                        # Parse measurement type
                        measurement_type = row.get('measurement_type', '').strip().upper()
                        if measurement_type not in self.VALID_MEASUREMENT_TYPES:
                            valid_types = ', '.join(sorted(self.MEASUREMENT_TYPE_NAMES.values()))
                            return False, f"Row {row_num}: Invalid measurement type '{measurement_type}'. Valid types: {valid_types}"
                        
                        # Validate measurement type for channel
                        if channel_num <= 12:
                            # Channels 1-12: voltage/resistance/capacitance only
                            if measurement_type in ['CURR:DC', 'CURR:AC']:
                                return False, f"Row {row_num}: Current measurements not supported on channel {channel_num} (channels 1-12)"
                        else:
                            # Channels 13-16: current only
                            if measurement_type not in ['CURR:DC', 'CURR:AC']:
                                return False, f"Row {row_num}: Only current measurements supported on channel {channel_num} (channels 13-16)"
                        
                        # Parse range (case-insensitive, but preserve correct case)
                        range_value_input = row.get('range', 'AUTO').strip()
                        if not range_value_input:
                            range_value = 'AUTO'
                        elif range_value_input.upper() == 'AUTO':
                            range_value = 'AUTO'
                        else:
                            # Find matching range (case-insensitive)
                            measurement_type_valid_ranges = self.VALID_RANGES.get(measurement_type, [])
                            range_value = None
                            for valid_range in measurement_type_valid_ranges:
                                if valid_range.upper() == range_value_input.upper():
                                    range_value = valid_range
                                    break
                            
                            if range_value is None:
                                valid_ranges = ', '.join(sorted(measurement_type_valid_ranges))
                                return False, f"Row {row_num}: Invalid range '{range_value_input}' for measurement type '{measurement_type}'. Valid ranges: {valid_ranges}"
                        
                        # Parse lower threshold (optional)
                        lower_threshold = None
                        lower_str = row.get('lower_threshold', '').strip()
                        if lower_str:
                            try:
                                lower_threshold = float(lower_str)
                            except ValueError:
                                return False, f"Row {row_num}: Invalid lower threshold '{lower_str}'"
                        
                        # Parse upper threshold (optional)
                        upper_threshold = None
                        upper_str = row.get('upper_threshold', '').strip()
                        if upper_str:
                            try:
                                upper_threshold = float(upper_str)
                            except ValueError:
                                return False, f"Row {row_num}: Invalid upper threshold '{upper_str}'"
                        
                        # Validate threshold consistency
                        if lower_threshold is not None and upper_threshold is not None:
                            if lower_threshold >= upper_threshold:
                                return False, f"Row {row_num}: Lower threshold ({lower_threshold}) must be less than upper threshold ({upper_threshold})"
                        
                        # Create configuration
                        config = ChannelThresholdConfig(
                            channel_num=channel_num,
                            measurement_type=measurement_type,
                            range_value=range_value,
                            lower_threshold=lower_threshold,
                            upper_threshold=upper_threshold
                        )
                        
                        # Check for duplicate channels
                        if channel_num in self.configs:
                            logger.warning(f"Row {row_num}: Channel {channel_num} already configured, overwriting")
                        
                        self.configs[channel_num] = config
                        
                    except Exception as e:
                        return False, f"Row {row_num}: Error parsing row - {str(e)}"
            
            if not self.configs:
                return False, "No valid channel configurations found in file"
            
            logger.info(f"Successfully loaded {len(self.configs)} channel configurations from {file_path}")
            return True, f"Loaded {len(self.configs)} channel configurations"
            
        except Exception as e:
            logger.error(f"Error loading configuration file: {e}")
            return False, f"Error loading file: {str(e)}"
    
    def get_channel_config(self, channel_num: int) -> Optional[ChannelThresholdConfig]:
        """
        Get configuration for a specific channel.
        
        Args:
            channel_num: Channel number (1-16).
            
        Returns:
            ChannelThresholdConfig if configured, None otherwise.
        """
        return self.configs.get(channel_num)
    
    def get_all_configs(self) -> Dict[int, ChannelThresholdConfig]:
        """
        Get all channel configurations.
        
        Returns:
            Dictionary mapping channel numbers to configurations.
        """
        return self.configs.copy()
    
    def get_configured_channels(self) -> List[int]:
        """
        Get list of configured channel numbers.
        
        Returns:
            Sorted list of channel numbers.
        """
        return sorted(self.configs.keys())
    
    def get_config_file_name(self) -> str:
        """
        Get the name of the loaded configuration file.
        
        Returns:
            File name or empty string if no file loaded.
        """
        if self.config_file_path:
            return self.config_file_path.name
        return ""
    
    def clear(self) -> None:
        """Clear all loaded configurations."""
        self.configs.clear()
        self.config_file_path = None
    
    def create_sample_config(self, file_path: str) -> Tuple[bool, str]:
        """
        Create a sample configuration file.
        
        Args:
            file_path: Path where to create the sample file.
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            sample_content = """# SDM4055A-SC Channel Configuration File
# 
# Format: channel,measurement_type,range,lower_threshold,upper_threshold
#
# Columns:
#   channel: Channel number (1-16)
#   measurement_type: Measurement type (see valid types below)
#   range: Measurement range (AUTO or specific value)
#   lower_threshold: Optional lower threshold (leave empty for no threshold)
#   upper_threshold: Optional upper threshold (leave empty for no threshold)
#
# Valid measurement types:
#   VOLT:DC - DC Voltage
#   VOLT:AC - AC Voltage
#   RES - 2-Wire Resistance
#   FRES - 4-Wire Resistance
#   CAP - Capacitance
#   FREQ - Frequency
#   DIOD - Diode
#   CONT - Continuity
#   TEMP:RTD - RTD Temperature
#   TEMP:THER - Thermocouple
#   CURR:DC - DC Current (channels 13-16 only)
#   CURR:AC - AC Current (channels 13-16 only)
#
# Notes:
#   - Channels 1-12: Voltage, Resistance, Capacitance, etc.
#   - Channels 13-16: Current measurements only
#   - Thresholds are optional - leave empty if not needed
#   - Values within thresholds display in GREEN
#   - Values outside thresholds display in RED
#   - You can configure only the channels you need

# Example configurations:
channel,measurement_type,range,lower_threshold,upper_threshold
1,VOLT:DC,AUTO,0,5
2,VOLT:DC,AUTO,-10,10
3,VOLT:AC,AUTO,0,120
4,RES,AUTO,0,1000
5,CAP,AUTO,1e-6,100e-6
13,CURR:DC,1A,0,0.5
14,CURR:DC,100mA,0,50e-3
"""
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(sample_content)
            
            logger.info(f"Created sample configuration file: {file_path}")
            return True, f"Sample configuration file created: {file_path}"
            
        except Exception as e:
            logger.error(f"Error creating sample configuration file: {e}")
            return False, f"Error creating sample file: {str(e)}"
