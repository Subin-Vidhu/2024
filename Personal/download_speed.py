import colorama
from colorama import Fore, Style

def calculate_download_time():
    print(Fore.CYAN + "Download Time Calculator" + Style.RESET_ALL)
    print(Fore.CYAN + "-------------------------" + Style.RESET_ALL)

    while True:
        print()
        print(Fore.GREEN + "Choose an option:" + Style.RESET_ALL)
        print("1. Calculate download time")
        print("2. Calculate file size")
        print("3. Calculate internet speed")
        print("4. Quit")

        option = input(Fore.YELLOW + "Enter your choice (1-4): " + Style.RESET_ALL)

        if option == "1":
            print(Fore.MAGENTA + "Calculate Download Time" + Style.RESET_ALL)
            print("---------------------------------")
            size_mb = float(input(Fore.YELLOW + "Enter file size in MB: " + Style.RESET_ALL))
            speed_mbps = float(input(Fore.YELLOW + "Enter internet speed in Mbps: " + Style.RESET_ALL))
            time_seconds = (size_mb * 8) / speed_mbps
            print(Fore.CYAN + f"Download time: {time_seconds:.2f} seconds" + Style.RESET_ALL)

        elif option == "2":
            print(Fore.MAGENTA + "Calculate File Size" + Style.RESET_ALL)
            print("------------------------")
            time_seconds = float(input(Fore.YELLOW + "Enter download time in seconds: " + Style.RESET_ALL))
            speed_mbps = float(input(Fore.YELLOW + "Enter internet speed in Mbps: " + Style.RESET_ALL))
            size_mb = (time_seconds * speed_mbps) / 8
            print(Fore.CYAN + f"File size: {size_mb:.2f} MB" + Style.RESET_ALL)

        elif option == "3":
            print(Fore.MAGENTA + "Calculate Internet Speed" + Style.RESET_ALL)
            print("-------------------------")
            size_mb = float(input(Fore.YELLOW + "Enter file size in MB: " + Style.RESET_ALL))
            time_seconds = float(input(Fore.YELLOW + "Enter download time in seconds: " + Style.RESET_ALL))
            speed_mbps = (size_mb * 8) / time_seconds
            print(Fore.CYAN + f"Internet speed: {speed_mbps:.2f} Mbps" + Style.RESET_ALL)

        elif option == "4":
            print(Fore.RED + "Goodbye!" + Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)

calculate_download_time()