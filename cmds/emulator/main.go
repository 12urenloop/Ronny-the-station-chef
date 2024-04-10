package main

import (
	"fmt"
	"math/rand"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/12urenloop/Ronny-the-station-chef/internal/db"
	"github.com/12urenloop/Ronny-the-station-chef/internal/logger"
	"github.com/sirupsen/logrus"
)

func main() {
	logger.InitLogger()

	// Open DB conn
	db := db.New()

	c := make(chan os.Signal, 1)                    // Create channel to signify a signal being sent
	signal.Notify(c, os.Interrupt, syscall.SIGTERM) // When an interrupt or termination signal is sent, notify the channel

	for {
		select {
		case <-c:
			return
		default:
			{

				detection := generateRandomDetection()

				id, err := db.InsertDetection(detection)
				if err != nil {
					logrus.Fatalf("Failed to insert detection: %v", err)
				}
				logrus.Infof("Inserted detection with id: %d\n", id)

				time.Sleep(time.Duration(randInt(10, 500)) * time.Millisecond)
			}
		}
	}
}

func generateRandomDetection() *db.Detection {
	detection := db.Detection{
		DetectionTime:     time.Now(),
		Mac:               fmt.Sprintf("5a:45:55:53:00:f%d", randInt(0, 10)),
		Rssi:              randInt(-120, -40),
		UptimeMs:          0,
		BatteryPercentage: uint8(randInt(0, 101)),
	}

	return &detection
}

// [min, max[
func randInt(min int, max int) int {
	return min + rand.Intn(max-min)
}
