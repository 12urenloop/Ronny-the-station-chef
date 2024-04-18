package utils

import "os"

func GetEnvOrFallback(key, defaultValue string) string {
	envVar := os.Getenv(key)
	if envVar == "" {
		return defaultValue
	}
	return envVar
}
