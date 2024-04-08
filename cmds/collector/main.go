package main

import (
	blescanner "github.com/12urenloop/gonny-the-station-chef/internal/ble_scanner"
	"github.com/12urenloop/gonny-the-station-chef/internal/db"
	"github.com/12urenloop/gonny-the-station-chef/internal/logger"
)

func main() {
	logger.InitLogger()

	// Open DB conn
	db := db.New()

	scanner := blescanner.New(db)

	scanner.Scan()
}
