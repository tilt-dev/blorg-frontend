//go:generate protoc -I ../blorg-backend/proto --go_out=plugins=grpc:./proto ../blorg-backend/proto/backend.proto
package main

import (
	"context"
	"flag"
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"net/http"
	"strings"

	"github.com/gorilla/mux"
	pb "github.com/windmilleng/blorg-frontend/proto"
	"google.golang.org/grpc"
)

const endptRand = "/random"

var backend = flag.String("backendAddr", "localhost:8080", "address of the blorg backend server")
var blorglyBackend = flag.String("blorglyBackendAddr", "http://localhost:8082", "address of blorgly backend server")
var conn *grpc.ClientConn
var storage pb.BackendClient

func main() {
	flag.Parse()

	c, err := grpc.Dial(*backend, grpc.WithInsecure())
	if err != nil {
		log.Fatalf("Dialing backend server resulted in error: %v\n", err)
	}
	conn = c
	storage = pb.NewBackendClient(conn)
	r := mux.NewRouter()
	r.HandleFunc("/", Storage)
	r.HandleFunc(endptRand, Randomizer)

	http.Handle("/", r)
	http.Handle("/public/", http.StripPrefix("/public/", http.FileServer(http.Dir("public"))))
	fmt.Println("Starting up on 8081")
	log.Fatal(http.ListenAndServe(":8081", nil))
}

func Storage(w http.ResponseWriter, req *http.Request) {
	if req.Method == "POST" {
		req.ParseForm()

		ctx := context.Background()
		url := req.Form.Get("url")
		_, err := storage.CreateGolink(ctx, &pb.Golink{Name: "cat", Address: url})
		if err != nil {
			w.WriteHeader(500)
			fmt.Fprintf(w, "Request to backend server resulted in error: %v\n", err)
			return
		}
	}

	p := "tech"
	t, err := template.ParseFiles("index.html")
	if err != nil {
		http.Error(w, fmt.Sprintf("Template compile error: %v\n", err), 500)
		return
	}
	t.Execute(w, p)
}

func Randomizer(w http.ResponseWriter, req *http.Request) {
	// TODO: Will want to be more careful concat'ing base + endpt in future
	// see http://bit.ly/2lFlOCq
	url := fmt.Sprintf("%s%s", *blorglyBackend, endptRand)
	resp, err := http.Get(url)

	if err != nil {
		w.WriteHeader(500)
		fmt.Fprintf(w, "Request to backend server resulted in error: %v\n", err)
		return
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		w.WriteHeader(500)
		fmt.Fprintf(w, "Could not read backend server resp. with error: %v\n", err)
		return
	}

	if resp.StatusCode != 200 || strings.TrimSpace(string(body)) != "random" {
		w.WriteHeader(500)
		fmt.Fprintf(w,
			"Expected 'random'; backend server said '%s' (%s)\n", strings.TrimSpace(string(body)), resp.Status)
		return
	}

	fmt.Fprintf(w, "SUCCESS! ﾍ(=￣∇￣)ﾉ\nSUCCESS! ﾍ(=￣∇￣)ﾉ")
}
