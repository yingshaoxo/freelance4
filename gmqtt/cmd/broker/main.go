package darkmqtt

import (
	"context"
	"log"
	"net"
	//"net/http"
	"os"
	"os/signal"
	"syscall"

	"github.com/DrmagicE/gmqtt"
)

func Run() {
	// listener
	ln, err := net.Listen("tcp", ":1883")
	if err != nil {
		log.Fatalln(err.Error())
		return
	}
	/*
		ws := &gmqtt.WsServer{
			Server: &http.Server{Addr: ":8080"},
			Path:   "/ws",
		}
	*/
	if err != nil {
		panic(err)
	}

	//l, _ := zap.NewDevelopment()
	s := gmqtt.NewServer(
		gmqtt.WithTCPListener(ln),
		//gmqtt.WithWebsocketServer(ws),
	)
	s.Run()
	signalCh := make(chan os.Signal, 1)
	signal.Notify(signalCh, os.Interrupt, syscall.SIGTERM)
	<-signalCh
	s.Stop(context.Background())
}
