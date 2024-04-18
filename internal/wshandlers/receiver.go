package wshandlers

import (
	"github.com/gofiber/contrib/websocket"
)

func Receiver(c *websocket.Conn) {
	defer c.Close()
	c.SetReadLimit(512)

	// TODO: add pong mechanism
	// https://github.com/fasthttp/websocket/blob/master/_examples/filewatch/fasthttp/main.go#L27

	for {
		_, _, err := c.ReadMessage()
		if err != nil {
			break
		}
	}
}
