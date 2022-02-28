//"users" table model

package models

import "gorm.io/gorm"

type User struct {
	gorm.Model
	// Id       uint   `json:"id"`
	// CreateAt string `json:"create_at"`
	// UpdateAt string `json:"update_at"`
	// DeleteAt string `json:"delete_at"`

	Email    string `json:"email"`
	Password string `json:"password"`
	UserType string `json:"user_type"`

	Name        string `json:"name"`
	Major       string `json:"major"`
	Grade       uint   `json:"grade"`
	ClassNumber uint   `json:"class_number"`
}
