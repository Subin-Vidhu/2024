package main

import (
	"fmt"
	"math"
)

func main() {
	// Prompt the user to enter a floating point number
	var input float64
	fmt.Print("Enter a floating point number: ")
	fmt.Scan(&input)

	// Truncate the floating point number to an integer
	truncated := int64(math.Trunc(input))

	// Print the truncated integer
	fmt.Printf("The truncated integer is: %d\n", truncated)
}
