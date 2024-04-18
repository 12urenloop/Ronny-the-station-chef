package main

import (
	"fmt"
	"log"
	"os"
	"os/signal"
	"strconv"
	"syscall"
	"time"

	"github.com/12urenloop/Ronny-the-station-chef/internal/db"
	"github.com/12urenloop/Ronny-the-station-chef/internal/logger"
	"github.com/12urenloop/Ronny-the-station-chef/internal/wshandlers"
	"github.com/gofiber/contrib/websocket"
	"github.com/gofiber/fiber/v2"
	"github.com/sirupsen/logrus"
)

func main() {
	logger.InitLogger()

	conn := db.New()

	app := fiber.New()

	stationId, err := os.Hostname()
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	// Backward compatibility with ronny
	app.Get("/detections/:last_id", func(c *fiber.Ctx) error {
		lastIdStr := c.Params("last_id")
		if lastIdStr == "" {
			return c.Status(400).SendString("last_id is required")
		}
		lastId, err := strconv.Atoi(lastIdStr)
		if err != nil {
			logrus.Errorf("Failed to convert last_id to int: %+v\n", err)
			return c.Status(400).SendString("last_id must be an integer")
		}

		limit := c.QueryInt("limit", 1000)

		detections, err := conn.GetLimitedIdsAfter(lastId, limit)
		if err != nil {
			logrus.Errorf("Failed to retrieve detections from DB: %+v\n", err)
			return c.Status(500).SendString("Failed to retrieve detections from DB")
		}

		return c.JSON(struct {
			Detections *[]db.Detection `json:"detections"`
			StationId  string          `json:"station_id"`
		}{
			detections,
			stationId,
		})
	})

	app.Get("/time", func(c *fiber.Ctx) error {
		return c.JSON(struct {
			Timestamp int64 `json:"timestamp"`
		}{
			Timestamp: time.Now().UnixMilli(),
		})
	})

	app.Get("/last_detection", func(c *fiber.Ctx) error {
		detection, err := conn.GetLastDetection()
		if err != nil {
			logrus.Errorf("Failed to retrieve last detection from DB: %+v\n", err)
			return c.Status(500).SendString("Failed to retrieve last detection from DB")
		}

		return c.JSON(struct {
			Detection *db.Detection `json:"detection"`
			StationId string        `json:"station_id"`
		}{
			detection,
			stationId,
		})
	})

	app.Use("/", func(c *fiber.Ctx) error {
		if websocket.IsWebSocketUpgrade(c) {
			c.Locals("allowed", true)
			return c.Next()
		}
		return fiber.ErrUpgradeRequired
	})

	app.Get("/", websocket.New(func(c *websocket.Conn) {
		initMsg := struct {
			LastId int64 `json:"lastId"`
		}{}

		if err := c.ReadJSON(&initMsg); err != nil {
			logrus.Errorf("Failed to read initial WS msg: %+v\n", err)
			c.Close()
			return
		}

		c.Locals("db", conn)
		go wshandlers.Writer(c, initMsg.LastId)
		wshandlers.Receiver(c)
	}))

	go func() {
		if err := app.Listen(":8000"); err != nil {
			log.Panic(err)
		}
	}()

	c := make(chan os.Signal, 1)                    // Create channel to signify a signal being sent
	signal.Notify(c, os.Interrupt, syscall.SIGTERM) // When an interrupt or termination signal is sent, notify the channel

	<-c // This blocks the main thread until an interrupt is received
	fmt.Println("Gracefully shutting down...")
	_ = app.Shutdown()

	fmt.Println("Fiber was successful shutdown.")
}
