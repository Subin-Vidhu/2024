package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	// Prompt the user to enter a string
	fmt.Print("Enter a string: ")

	// Read the input string
	reader := bufio.NewReader(os.Stdin)
	input, _ := reader.ReadString('\n')

	// Trim whitespace and convert the string to lower case
	input = strings.TrimSpace(input)
	lowerInput := strings.ToLower(input)

	// Check if the string starts with 'i', ends with 'n', and contains 'a'
	if strings.HasPrefix(lowerInput, "i") && strings.HasSuffix(lowerInput, "n") && strings.Contains(lowerInput, "a") {
		fmt.Println("Found!")
	} else {
		fmt.Println("Not Found!")
	}
}
