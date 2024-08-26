package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strings"
)

func getStudyIDs(orthancURL, basicAuth, studyInstanceUID string) ([]string, error) {
	// Construct the URL for the query
	queryURL := fmt.Sprintf("%s/tools/find", orthancURL)

	// Construct the query parameters
	queryParams := map[string]interface{}{
		"Level": "Study",
		"Query": map[string]string{
			"StudyInstanceUID": studyInstanceUID,
		},
	}

	// Convert queryParams to JSON
	queryParamsJSON, err := json.Marshal(queryParams)
	if err != nil {
		return nil, err
	}

	// Construct the request
	req, err := http.NewRequest("POST", queryURL, strings.NewReader(string(queryParamsJSON)))
	if err != nil {
		return nil, err
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", basicAuth)

	// Send the request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	// Read the response body
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	// Print raw response body for debugging
	fmt.Printf("Raw response body: %s\n", string(body))

	// Check if request was successful
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("failed to retrieve study IDs: %s", resp.Status)
	}

	// Parse the JSON response as an array of strings
	var studyIDs []string
	if err := json.Unmarshal(body, &studyIDs); err != nil {
		return nil, err
	}

	if len(studyIDs) == 0 {
		return nil, fmt.Errorf("no studies found")
	}

	return studyIDs, nil
}

func downloadStudyAsZip(orthancURL, basicAuth, studyID string) ([]byte, error) {
	archiveURL := fmt.Sprintf("%s/studies/%s/archive", orthancURL, studyID)

	// Construct the request
	req, err := http.NewRequest("GET", archiveURL, nil)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Authorization", basicAuth)

	// Send the request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	// Check if request was successful
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("failed to download study: %s", resp.Status)
	}

	// Read the response body
	return ioutil.ReadAll(resp.Body)
}

func main() {
	// Example usage
	orthancURL := "http://localhost:8042"
	basicAuth := "Basic YWRtaW46cGFzc3dvcmQ=" // Replace with your Base64 encoded credentials
	studyInstanceUID := "1.3.12.2.1107.5.1.7.107889.30000024081417115758500000006"

	studyIDs, err := getStudyIDs(orthancURL, basicAuth, studyInstanceUID)
	if err != nil {
		log.Fatalf("Error getting study IDs: %v", err)
	}

	fmt.Printf("Study IDs: %v\n", studyIDs)

	if len(studyIDs) > 0 {
		studyID := studyIDs[0]
		zipData, err := downloadStudyAsZip(orthancURL, basicAuth, studyID)
		if err != nil {
			log.Fatalf("Error downloading study: %v", err)
		}

		// Save zip file to disk
		err = ioutil.WriteFile("study.zip", zipData, 0644)
		if err != nil {
			log.Fatalf("Error saving zip file: %v", err)
		}
	}
}
