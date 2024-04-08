package db

import (
	"time"
)

type Detection struct {
	ID                int64     `json:"id" gorm:"primaryKey,autoIncrement"`
	DetectionTime     time.Time `json:"detectionTime"`
	Mac               string    `json:"mac"`
	Rssi              int       `json:"rssi"`
	UptimeMs          uint64    `json:"uptimeMs"`
	BatteryPercentage uint8     `json:"batteryPercentage"`
}

func (D *Detection) TableName() string {
	// Python does not use plural table names
	return "detection"
}
