package db

import (
	"fmt"
	"log"
	"strconv"

	"database/sql"

	"github.com/12urenloop/Ronny-the-station-chef/internal/utils"
	_ "github.com/joho/godotenv/autoload"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var (
	host     = utils.GetEnvOrFallback("DATABASE_HOST", "localhost")
	port, _  = strconv.ParseUint(utils.GetEnvOrFallback("DATABASE_PORT", "5432"), 10, 16)
	user     = utils.GetEnvOrFallback("DATABASE_USER", "ronny")
	password = utils.GetEnvOrFallback("DATABASE_PASSWORD", "ronnydbpassword")
	dbname   = utils.GetEnvOrFallback("DATABASE_DB", "ronny")
	psqldsn  = fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable", host, port, user, password, dbname)
)

type DB struct {
	raw  *sql.DB
	conn *gorm.DB
}

func New() *DB {
	sqlDb, err := sql.Open("pgx", psqldsn)
	if err != nil {
		log.Fatalf("Failed to open a DB connection: %+v\n", err)
	}
	conn, err := gorm.Open(postgres.New(postgres.Config{
		Conn: sqlDb,
	}), &gorm.Config{})

	if err != nil {
		log.Fatalf("Failed to open a DB connection: %+v\n", err)
	}

	db := DB{
		raw:  sqlDb,
		conn: conn,
	}

	err = conn.AutoMigrate(&Detection{})
	if err != nil {
		log.Fatalf("Failed to do auto migration for tables: %+v\n", err)
	}

	return &db
}

func (db *DB) InsertDetection(detection *Detection) (int64, error) {
	// err := db.conn.Create(detection).Error
	id := int64(0)
	err := db.raw.QueryRow("INSERT INTO detection (rssi, mac, uptime_ms, detection_time, battery_percentage) VALUES ($1, $2, $3, $4, $5) RETURNING id", detection.Rssi, detection.Mac, detection.UptimeMs, detection.DetectionTime, detection.BatteryPercentage).Scan(&id)
	detection.ID = id
	return detection.ID, err
}

func (db *DB) GetDetectionsBetweenIds(a, b int64) (*[]Detection, error) {
	detections := []Detection{}

	err := db.conn.Where("id BETWEEN ? AND ?", a, b).Find(&detections).Error

	return &detections, err
}

func (db *DB) GetLimitedIdsAfter(a, limit int) (*[]Detection, error) {
	detections := []Detection{}

	err := db.conn.Where("id >", a).Limit(limit).Find(&detections).Error

	return &detections, err
}

func (db *DB) GetLastDetectionId() (int64, error) {
	var detection Detection
	err := db.conn.Last(&detection).Error
	return detection.ID, err
}

func (db *DB) GetLastDetection() (*Detection, error) {
	detection := Detection{}

	err := db.conn.Order("id desc").Limit(1).First(&detection).Error

	if err != nil && err == gorm.ErrRecordNotFound {
		return nil, nil
	}

	return &detection, err
}
