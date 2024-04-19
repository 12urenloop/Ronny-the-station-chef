package db

type Detection struct {
	ID                int64  `json:"id" gorm:"primaryKey,autoIncrement"`
	DetectionTime     int64  `json:"detection_timestamp"`
	Mac               string `json:"mac"`
	Rssi              int    `json:"rssi"`
	UptimeMs          uint64 `json:"uptime_ms"`
	BatteryPercentage uint8  `json:"battery"`
}

func (D *Detection) TableName() string {
	// Python does not use plural table names
	return "detection"
}
