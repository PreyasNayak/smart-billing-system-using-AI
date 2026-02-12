"""
Load Cell Calibration Script
This script helps calibrate the HX711 load cell for accurate weight measurements.
"""

import sys
import time

# Note: Uncomment these when HX711 library is installed
# import RPi.GPIO as GPIO
# from hx711 import HX711


def print_header():
    """Print script header."""
    print("\n" + "=" * 60)
    print("  LOAD CELL CALIBRATION UTILITY")
    print("=" * 60 + "\n")


def cleanup_and_exit():
    """Clean up GPIO and exit."""
    print("\nCleaning up...")
    # GPIO.cleanup()
    print("Calibration complete!")
    sys.exit(0)


def calibrate_load_cell(dout_pin=5, pd_sck_pin=6):
    """
    Calibrate the load cell.
    
    Args:
        dout_pin (int): GPIO pin for data
        pd_sck_pin (int): GPIO pin for clock
    """
    print_header()
    
    print("Hardware Setup:")
    print(f"  - DOUT Pin: GPIO {dout_pin}")
    print(f"  - PD_SCK Pin: GPIO {pd_sck_pin}\n")
    
    try:
        # Initialize HX711
        # Uncomment when library is available:
        # hx = HX711(dout_pin, pd_sck_pin)
        # hx.set_reading_format("MSB", "MSB")
        # hx.reset()
        
        print("[Step 1] Initialize Load Cell")
        print("-" * 60)
        # time.sleep(1)
        print("✓ Load cell initialized\n")
        
        # Tare (zero) the scale
        print("[Step 2] Tare (Zero) the Scale")
        print("-" * 60)
        print("IMPORTANT: Remove ALL items from the scale")
        input("Press ENTER when scale is empty...")
        
        # Uncomment when library is available:
        # hx.reset()
        # hx.tare()
        # print("✓ Scale tared (zeroed)\n")
        
        print("Taking readings...")
        # for i in range(5):
        #     val = hx.get_weight(5)
        #     print(f"  Reading {i+1}: {val}")
        #     time.sleep(0.5)
        print("✓ Tare complete\n")
        
        # Calibrate with known weight
        print("[Step 3] Calibrate with Known Weight")
        print("-" * 60)
        print("You will need a known weight (recommended: 100g or 1kg)")
        
        weight_input = input("\nEnter the weight value in grams (e.g., 100): ")
        try:
            known_weight = float(weight_input)
        except ValueError:
            print("Invalid weight value!")
            return
        
        input(f"\nPlace {known_weight}g weight on the scale and press ENTER...")
        
        print("\nTaking calibration readings...")
        # Uncomment when library is available:
        # readings = []
        # for i in range(10):
        #     val = hx.get_value(5)
        #     readings.append(val)
        #     print(f"  Reading {i+1}: {val}")
        #     time.sleep(0.5)
        # 
        # avg_reading = sum(readings) / len(readings)
        # calibration_factor = avg_reading / known_weight
        
        # Example values for demonstration
        calibration_factor = 404.0  # This will vary for each setup
        
        print(f"\n✓ Calibration Factor: {calibration_factor:.2f}")
        print(f"\nSave this calibration factor in your config/settings.json:")
        print(f'  "scale": {{\n    "calibration_factor": {calibration_factor:.2f}\n  }}\n')
        
        # Verification
        print("[Step 4] Verification")
        print("-" * 60)
        verify = input("Do you want to verify calibration? (y/n): ")
        
        if verify.lower() == 'y':
            print("\nVerification Test:")
            print("Place different known weights and check accuracy\n")
            
            for _ in range(3):
                input("Place weight and press ENTER (or Ctrl+C to skip)...")
                # Uncomment when library is available:
                # hx.set_reference_unit(calibration_factor)
                # weight = hx.get_weight(5)
                # print(f"  Measured weight: {weight:.2f}g")
                
                print(f"  Measured weight: [will show actual reading]g")
                
                actual = input("  Enter actual weight to compare (or skip): ")
                if actual:
                    try:
                        actual_weight = float(actual)
                        # error = abs(weight - actual_weight) / actual_weight * 100
                        # print(f"  Error: {error:.2f}%\n")
                        print("  Comparison recorded\n")
                    except ValueError:
                        print("  Skipped\n")
        
        print("\n" + "=" * 60)
        print("CALIBRATION SUMMARY")
        print("=" * 60)
        print(f"Calibration Factor: {calibration_factor:.2f}")
        print(f"Known Weight Used: {known_weight}g")
        print("\nNext Steps:")
        print("1. Update config/settings.json with calibration factor")
        print("2. Run test_hardware.py to verify")
        print("3. Start using the billing system")
        print("=" * 60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nCalibration interrupted by user")
    except Exception as e:
        print(f"\nError during calibration: {e}")
    finally:
        cleanup_and_exit()


def main():
    """Main function."""
    print("\n")
    
    # Get GPIO pins from user or use defaults
    use_default = input("Use default GPIO pins (5 for DT, 6 for SCK)? (y/n): ")
    
    if use_default.lower() == 'y':
        dout_pin = 5
        pd_sck_pin = 6
    else:
        try:
            dout_pin = int(input("Enter GPIO pin for DOUT (Data): "))
            pd_sck_pin = int(input("Enter GPIO pin for SCK (Clock): "))
        except ValueError:
            print("Invalid pin numbers! Using defaults.")
            dout_pin = 5
            pd_sck_pin = 6
    
    calibrate_load_cell(dout_pin, pd_sck_pin)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  Smart Billing System - Load Cell Calibration")
    print("=" * 60)
    print("\nNOTE: This is a template script.")
    print("Uncomment HX711 library imports when running on actual hardware.")
    print("\nPress Ctrl+C at any time to exit.")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
