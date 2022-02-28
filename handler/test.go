package handler

import (
	"hansei-ctf-backend/db"
	"hansei-ctf-backend/models"

	"net/http"

	"github.com/labstack/echo/v4"
)

func Test(c echo.Context) error {

	db := db.Connect()

	db.AutoMigrate(&models.Test{})
	db.Create(&models.Test{Code: "D42", Price: 100})

	// 모든 처리가 끝난 후 200, Success 메시지를 반환
	return c.JSON(http.StatusOK, map[string]string{
		"message": "Success",
	})
}
