// db/connect.go
package db

import (
	"os"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

func Connect() *gorm.DB {
	USER := os.Getenv("DBUSER")   // DB 유저명
	PASS := os.Getenv("DBPASS")   // DB 유저의 패스워드
	DBNAME := os.Getenv("DBNAME") // 사용할 DB 명을 입력
	DBHOST := os.Getenv("DBHOST") // DB 서버의 호스트명
	DBPORT := os.Getenv("DBPORT") // DB 서버의 포트번호
	CONNECT := "host=" + DBHOST + " user=" + USER + " password=" + PASS + " dbname=" + DBNAME + " port=" + DBPORT + " sslmode=disable TimeZone=Asia/Seoul"
	db, err := gorm.Open(postgres.Open(CONNECT), &gorm.Config{})

	if err != nil {
		panic("💀 failed to connect database")
	}

	return db
}
