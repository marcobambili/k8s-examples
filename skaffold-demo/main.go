package main

import (
	"fmt"
	"net/http"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "ciao mondo")
	})

	fmt.Printf("Listening on port 8080\n")
	http.ListenAndServe(":8080", nil)

}
