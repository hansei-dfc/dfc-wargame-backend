package main

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

type User struct {
	Name     string `json:"name"`
	Email    string `json:"email"`
	Password string `json:"password"`
}

func AuthRegister(c echo.Context) error {
	u := new(User)
	if err := c.Bind(u); err != nil {
		return c.JSONPretty(http.StatusBadRequest, &StandardMsg{Message: "Invalid request body"}, "  ")
	}
	return c.JSONPretty(http.StatusOK, u, "  ")
}
