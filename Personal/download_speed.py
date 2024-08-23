def calculate_download_time():
    print("Download Time Calculator")
    print("-------------------------")

    while True:
        print("Choose an option:")
        print("1. Calculate download time")
        print("2. Calculate file size")
        print("3. Calculate internet speed")
        print("4. Quit")
        print()
        option = input("Enter your choice (1-4): ")

        if option == "1":
            size_mb = float(input("Enter file size in MB: "))
            speed_mbps = float(input("Enter internet speed in Mbps: "))
            time_seconds = (size_mb * 8) / speed_mbps
            print(f"Download time: {time_seconds:.2f} seconds")

        elif option == "2":
            time_seconds = float(input("Enter download time in seconds: "))
            speed_mbps = float(input("Enter internet speed in Mbps: "))
            size_mb = (time_seconds * speed_mbps) / 8
            print(f"File size: {size_mb:.2f} MB")

        elif option == "3":
            size_mb = float(input("Enter file size in MB: "))
            time_seconds = float(input("Enter download time in seconds: "))
            speed_mbps = (size_mb * 8) / time_seconds
            print(f"Internet speed: {speed_mbps:.2f} Mbps")

        elif option == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

        print()

calculate_download_time()