package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Name struct {
	Fname string
	Lname string
}

func main() {
	// Prompt the user for the name of the text file
	fmt.Print("Enter the name of the text file: ")
	var fileName string
	fmt.Scanln(&fileName)

	// Open the file
	file, err := os.Open(fileName)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	// Create a slice to hold the Name structs
	var names []Name

	// Read each line from the file
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.Fields(line)
		if len(parts) == 2 {
			fname := parts[0]
			lname := parts[1]
			names = append(names, Name{Fname: fname, Lname: lname})
		}
	}

	if err := scanner.Err(); err != nil {
		fmt.Println("Error reading file:", err)
		return
	}

	// Print the names from the slice
	for _, name := range names {
		fmt.Printf("First Name: %s, Last Name: %s\n", name.Fname, name.Lname)
	}
}
