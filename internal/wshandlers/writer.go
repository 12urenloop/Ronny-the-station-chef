package wshandlers

import (
	"errors"
	"io"
	"os"
	"strings"
	"time"

	"github.com/12urenloop/Ronny-the-station-chef/internal/db"
	"github.com/gofiber/contrib/websocket"
	"github.com/sirupsen/logrus"
)

var batch_size = 10000

func Writer(c *websocket.Conn, lastId int64) {
	closeChan := make(chan bool)

	db := c.Locals("db").(*db.DB)

	lastDbId, err := db.GetLastDetectionId()
	if err != nil {
		logrus.Errorf("Failed to get last detection id: %+v\n", err)
		closeChan <- true
	}

	if lastId > lastDbId {
		lastId = lastDbId
	}

	for {
		select {
		case <-closeChan:
			return
		default:
			{
				if c.Conn == nil {
					closeChan <- true
				}

				lastDbId, err := db.GetLastDetectionId()
				if err != nil {
					logrus.Errorf("Failed to get last detection id: %+v\n", err)
					closeChan <- true
				}

				if lastDbId == lastId {
					continue
				}

				detections, err := db.GetDetectionsBetweenIds(lastId+1, lastDbId)

				if err != nil {
					logrus.Errorf("Failed fetching detections: %+v\n", err)
					continue
				}

				for i := 0; i < len(*detections); i += batch_size {
					detection_batch := (*detections)[i:min(i+batch_size, len(*detections))]

					err = c.SetWriteDeadline(time.Now().Add(10 * time.Second))
					if err != nil {
						logrus.Errorf("Failed set write deadline on WS: %+v\n", err)
						continue
					}

					if err = c.WriteJSON(detection_batch); err != nil {
						if errors.Is(err, os.ErrDeadlineExceeded) {
							logrus.Errorf("Failed to write data to websocket: deadline exceeded")
							continue
						}
						if errors.Is(err, io.ErrClosedPipe) || errors.Is(err, os.ErrDeadlineExceeded) || strings.Contains(err.Error(), "broken pipe") {
							// Handle connection closure
							logrus.Debugln("Connection closed")
							closeChan <- true
							return
						}
						// Do some error recovery/restart procedure
						logrus.Errorf("Failed to send detections over websocket: %+v\n", err)
						continue
					}
					lastId = lastDbId

					// Do not spam the loop
					time.Sleep(10 * time.Millisecond)
				}
			}
		}
	}
}
