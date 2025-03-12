import sys

class RockchipGPIOCalculator:
    def __init__(self, gpio_bank_size=32, gpio_group_size=8):
        self.gpio_bank_size = gpio_bank_size
        self.gpio_group_size = gpio_group_size

    def gpio_name_to_number(self, gpio_name):
        """
        Convert a GPIO name (e.g., GPIO0_A3) to a GPIO number.
        
        :param gpio_name: The GPIO name in the format GPIO<bank>_<group><pin> (e.g., GPIO0_A3)
        :return: The GPIO number as an integer.
        """
        try:
            # Split the GPIO name into bank, group, and pin
            bank_part, pin_part = gpio_name.split('_')
            bank = int(bank_part.replace("GPIO", ""))
            group = pin_part[0]  # A, B, C, etc.
            pin = int(pin_part[1:])  # Pin number within the group

            # Calculate the GPIO number
            group_offset = (ord(group.upper()) - ord('A')) * self.gpio_group_size
            gpio_number = (bank * self.gpio_bank_size) + group_offset + pin

            return gpio_number
        except (ValueError, IndexError, AttributeError):
            raise ValueError(f"Invalid GPIO name format: {gpio_name}. Expected format: GPIO<bank>_<group><pin> (e.g., GPIO0_A3)")

    def gpio_number_to_name(self, gpio_number):
        """
        Convert a GPIO number to a GPIO name (e.g., GPIO1_C1).
        
        :param gpio_number: The GPIO number (e.g., 49 for GPIO1_C1)
        :return: The GPIO name in the format GPIO<bank>_<group><pin>.
        """
        if not isinstance(gpio_number, int) or gpio_number < 0:
            raise ValueError("GPIO number must be a positive integer.")

        # Calculate the bank and pin within the bank
        bank = gpio_number // self.gpio_bank_size
        pin_in_bank = gpio_number % self.gpio_bank_size

        # Calculate the group and pin within the group
        group_index = pin_in_bank // self.gpio_group_size
        pin_in_group = pin_in_bank % self.gpio_group_size

        # Determine the group letter (A, B, C, etc.)
        group = chr(ord('A') + group_index)

        # Format the GPIO name
        gpio_name = f"GPIO{bank}_{group}{pin_in_group}"

        return gpio_name

    def calculate_gpio_info(self, gpio_number):
        """
        Calculate the GPIO bank, pin number, and other relevant information.
        
        :param gpio_number: The GPIO number (e.g., 3 for GPIO0_A3, 49 for GPIO1_C1, etc.)
        :return: A dictionary containing the GPIO bank, pin number, and other info.
        """
        if not isinstance(gpio_number, int) or gpio_number < 0:
            raise ValueError("GPIO number must be a positive integer.")

        # Calculate the GPIO bank and pin number
        gpio_bank = gpio_number // self.gpio_bank_size
        pin_number = gpio_number % self.gpio_bank_size

        # Calculate the register offset (assuming 4 bytes per GPIO)
        register_offset = gpio_number * 4

        return {
            "GPIO Number": gpio_number,
            "GPIO Bank": gpio_bank,
            "Pin Number": pin_number,
            "Register Offset (hex)": f"0x{register_offset:08X}",
            "Register Offset (dec)": register_offset,
        }

    def print_gpio_info(self, gpio_number):
        """
        Print the GPIO information in a human-readable format.
        
        :param gpio_number: The GPIO number (e.g., 3 for GPIO0_A3, 49 for GPIO1_C1, etc.)
        """
        gpio_info = self.calculate_gpio_info(gpio_number)
        print(f"GPIO Number: {gpio_info['GPIO Number']}")
        print(f"GPIO Bank: {gpio_info['GPIO Bank']}")
        print(f"Pin Number: {gpio_info['Pin Number']}")
        print(f"Register Offset (hex): {gpio_info['Register Offset (hex)']}")
        print(f"Register Offset (dec): {gpio_info['Register Offset (dec)']}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python gpio_calculator.py <GPIO_NAME or GPIO_NUMBER>")
        print("Example 1: python gpio_calculator.py GPIO1_C1")
        print("Example 2: python gpio_calculator.py 49")
        sys.exit(1)

    input_value = sys.argv[1]
    gpio_calculator = RockchipGPIOCalculator()

    try:
        # Check if the input is a GPIO name (e.g., GPIO1_C1)
        if input_value.startswith("GPIO"):
            gpio_number = gpio_calculator.gpio_name_to_number(input_value)
            print(f"{input_value} corresponds to GPIO number: {gpio_number}")
            gpio_calculator.print_gpio_info(gpio_number)
        else:
            # Assume the input is a GPIO number
            gpio_number = int(input_value)
            gpio_name = gpio_calculator.gpio_number_to_name(gpio_number)
            print(f"GPIO number {gpio_number} corresponds to GPIO name: {gpio_name}")
            gpio_calculator.print_gpio_info(gpio_number)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()