package main

import (
	"encoding/json"
	"fmt"
)

func main() {
	// Create a map to store name and address
	info := make(map[string]string)

	// Prompt the user to enter a name
	fmt.Print("Enter a name: ")
	var name string
	fmt.Scanln(&name)
	info["name"] = name

	// Prompt the user to enter an address
	fmt.Print("Enter an address: ")
	var address string
	fmt.Scanln(&address)
	info["address"] = address

	// Marshal the map into a JSON object
	jsonData, err := json.Marshal(info)
	if err != nil {
		fmt.Println("Error marshalling to JSON:", err)
		return
	}

	// Print the JSON object
	fmt.Println(string(jsonData))
}
