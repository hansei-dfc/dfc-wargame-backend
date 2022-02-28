## .env for database

```
DBHOST=localhost
DBUSER=postgres
DBPASS=root
DBNAME=test
DBPORT=5432

SECRET_KEY=ciiwqfoxmezx
```

## Necessary Go Packages

```
"github.com/labstack/echo/v4"
"github.com/labstack/echo/v4/middleware"
"gorm.io/driver/postgres"
"gorm.io/gorm"
"github.com/golang-jwt/jwt"
"golang.org/x/crypto/bcrypt"
"github.com/joho/godotenv"
```
