#!/usr/bin/env python3
"""
TPMS Serial Monitor
Visualizes data from USB TPMS receivers with multiple display formats
"""

import serial
import time
import sys
import threading
from datetime import datetime
import argparse

class TPMSMonitor:
    def __init__(self, port, baudrate=9600, log_file=None):
        self.port = port
        self.baudrate = baudrate
        self.log_file = log_file
        self.running = False
        self.ser = None
        
    def connect(self):
        """Connect to the serial port"""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
            print(f"✓ Connected to {self.port} at {self.baudrate} baud")
            return True
        except Exception as e:
            print(f"✗ Failed to connect: {e}")
            return False
    
    def format_hex_ascii(self, data):
        """Format data as hex with ASCII representation"""
        hex_str = ' '.join(f'{b:02X}' for b in data)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data)
        return f"HEX: {hex_str:<48} ASCII: [{ascii_str}]"
    
    def format_raw_bytes(self, data):
        """Format raw bytes as decimal"""
        return f"RAW: {' '.join(str(b) for b in data)}"
    
    def decode_tpms_packet(self, data):
        """Decode a TPMS packet and display human-readable information"""
        if len(data) != 8:
            return
        
        # Extract packet components
        header = (data[0] << 8) | data[1]  # 0x55AA
        length = data[2]  # 0x08
        sensor_id = data[3]
        pressure_value = data[4]  # PRESSURE in PSI!
        temp_value = data[5]     # TEMPERATURE in °F!
        reserved = data[6]       # Usually 0x00
        checksum = data[7]
        
        # Verify checksum (XOR of first 7 bytes)
        calc_checksum = 0
        for byte in data[:-1]:
            calc_checksum ^= byte
        
        checksum_valid = calc_checksum == checksum
        
        # Display decoded information
        print("🎯 DECODED TPMS DATA:")
        print(f"   Sensor ID: {sensor_id} (0x{sensor_id:02X})")
        print(f"   💨 Pressure: {pressure_value} PSI")
        print(f"   🌡️ Temperature: {temp_value}°F")
        print(f"   Checksum: {'✓ Valid' if checksum_valid else '✗ Invalid'}")
        
        # Add sensor location mapping (FULLY CONFIRMED through testing)
        sensor_locations = {
            0: "Front Left (FL) 🎯",        # CONFIRMED - 21 PSI, 73°F
            1: "Front Right (FR) 🎯",       # CONFIRMED - 30 PSI, 75°F
            5: "Internal/Reference (receiver)",
            16: "Rear Left (RL) 🎯",        # CONFIRMED - was 23 PSI
            17: "Rear Right (RR) 🎯"        # CONFIRMED - was 37 PSI
        }
        
        location = sensor_locations.get(sensor_id, f"Unknown Sensor {sensor_id}")
        print(f"   📍 Location: {location}")
        
        # Status assessment
        if pressure_value == 0:
            status = "🌙 Dormant (no pressure)"
        elif pressure_value < 15:
            status = "⚠️ Low pressure"
        elif pressure_value < 30:
            status = "✅ Normal pressure"
        elif pressure_value < 40:
            status = "📈 High pressure"
        else:
            status = "🚨 Very high pressure!"
            
        print(f"   Status: {status}")
        
        # Temperature status
        if temp_value < 32:
            temp_status = "🧊 Freezing"
        elif temp_value < 60:
            temp_status = "❄️ Cold"
        elif temp_value < 80:
            temp_status = "🌡️ Normal"
        elif temp_value < 100:
            temp_status = "🔥 Hot"
        else:
            temp_status = "🚨 Overheating!"
            
        print(f"   Temp Status: {temp_status}")
    
    def log_data(self, timestamp, data, formatted_lines):
        """Log data to file if logging is enabled"""
        if self.log_file:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n--- {timestamp} ---\n")
                for line in formatted_lines:
                    f.write(f"{line}\n")
    
    def monitor(self):
        """Main monitoring loop"""
        if not self.connect():
            return
        
        self.running = True
        print(f"\n🎯 Monitoring {self.port} - Press Ctrl+C to stop")
        print("=" * 80)
        
        buffer = bytearray()
        
        try:
            while self.running:
                if self.ser.in_waiting > 0:
                    data = self.ser.read(self.ser.in_waiting)
                    buffer.extend(data)
                    
                    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    
                    # Format the data multiple ways
                    formatted_lines = [
                        f"[{timestamp}] Received {len(data)} bytes:",
                        self.format_hex_ascii(data),
                        self.format_raw_bytes(data)
                    ]
                    
                    # Try to detect patterns or decode as text
                    try:
                        text = data.decode('utf-8', errors='ignore')
                        if any(c.isprintable() for c in text):
                            formatted_lines.append(f"TEXT: {repr(text)}")
                    except:
                        pass
                    
                    # Display raw data
                    for line in formatted_lines:
                        print(line)
                    
                    # Decode TPMS data if it's a valid packet
                    if len(data) == 8 and data[0] == 0x55 and data[1] == 0xAA and data[2] == 0x08:
                        self.decode_tpms_packet(data)
                    
                    # Look for potential packet boundaries
                    if len(buffer) > 50:  # Prevent buffer from growing too large
                        print(f"📦 Buffer summary: {len(buffer)} total bytes")
                        buffer.clear()
                    
                    print("-" * 40)
                    
                    # Log to file
                    self.log_data(timestamp, data, formatted_lines)
                
                time.sleep(0.01)  # Small delay to prevent excessive CPU usage
                
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        finally:
            if self.ser:
                self.ser.close()
            print("📡 Serial connection closed")

def main():
    parser = argparse.ArgumentParser(description='TPMS Serial Monitor')
    parser.add_argument('port', help='Serial port (e.g., COM20)')
    parser.add_argument('-b', '--baud', type=int, default=9600, 
                       help='Baud rate (default: 9600)')
    parser.add_argument('-l', '--log', help='Log file path')
    
    args = parser.parse_args()
    
    # Display connection info
    print("🚗 TPMS Serial Monitor")
    print(f"Port: {args.port}")
    print(f"Baud: {args.baud}")
    print(f"Settings: 8-N-1 (8 data bits, no parity, 1 stop bit)")
    if args.log:
        print(f"Logging: {args.log}")
    
    monitor = TPMSMonitor(args.port, args.baud, args.log)
    monitor.monitor()

if __name__ == "__main__":
    main()
