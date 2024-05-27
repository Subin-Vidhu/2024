package main

import (
	"fmt"
	"sort"
	"strconv"
	"strings"
)

func main() {
	// Create an empty integer slice
	var numbers []int

	for {
		// Prompt the user to enter an integer
		fmt.Print("Enter an integer (or 'X' to quit): ")

		// Read user input
		var input string
		fmt.Scan(&input)

		// Check if the user wants to quit
		if strings.ToUpper(input) == "X" {
			break
		}

		// Convert the input to an integer
		number, err := strconv.Atoi(input)
		if err != nil {
			fmt.Println("Invalid input. Please enter a valid integer.")
			continue
		}

		// Add the number to the slice
		numbers = append(numbers, number)

		// Sort the slice
		sort.Ints(numbers)

		// Print the sorted slice
		fmt.Println("Sorted slice:", numbers)
	}
}
