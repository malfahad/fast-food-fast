# fast-food-fast

Fast food fast is a food ordering web application.
This branch is for the fast-food-fast api. The app entry point is at ` app.py `

## implemented endpoints

### 1 . Authentication

`POST /api/v1/login` for user login. \n
`POST /api/v1/register` for user registration. \n  
`POST /api/v1/admin/login` for admin login. \n  
`GET /api/v1/logout` for user logout. \n
`GET /api/v1/admin/logout` for admin logout. \n  
`GET  /api/v1/me` for checking for an existing user session. \n
`GET  /api/v1/admin/me` for checking for an existing admin session. \n  


### 2 . Orders endpoints

`GET /api/v1/orders` returns a list of all orders. \n
`GET /api/v1/orders/<orderId>` returns one order corresponding to the submitted order id. \n   
`GET /api/v1/orders/<clinetId>` returns list of orders from the same client/user. \n
`POST /api/v1/orders` add a new order to the service. \n
`PUT /api/v1/orders/<orderId>` update the status of an order from the service.


### 3 . menu endpoints
`GET /api/v1/menu` returns a list of all menu items.\n
`POST /api/v1/menu` adds a new menu item to the menu.\n
`POST /api/v1/menu/remove` removes a  menu item from the menu.\n
