package logger

import (
	"os"

	"github.com/sirupsen/logrus"
)

func InitLogger() {
	logLevel, err := logrus.ParseLevel(os.Getenv("LOG_LEVEL"))
	if err != nil {
		logLevel = logrus.InfoLevel
	}

	logrus.SetLevel(logLevel)
}
