# fast-food-fast

Fast food fast is a food ordering web application.
This branch is for the fast-food-fast api. The app entry point is at ` app.py `

## implemented endpoints

### 1 . Authentication

`POST /api/v1/login` for user login. *same paragraph*
`POST /api/v1/register` for user registration. *same paragraph*  
`POST /api/v1/admin/login` for admin login. *same paragraph*  
`GET /api/v1/logout` for user logout. *same paragraph*
`GET /api/v1/admin/logout` for admin logout. *same paragraph*  
`GET  /api/v1/me` for checking for an existing user session. *same paragraph*
`GET  /api/v1/admin/me` for checking for an existing admin session. *same paragraph*  


### 2 . Orders endpoints

`GET /api/v1/orders` returns a list of all orders. *same paragraph*
`GET /api/v1/orders/<orderId>` returns one order corresponding to the submitted order id. *same paragraph*   
`GET /api/v1/orders/<clinetId>` returns list of orders from the same client/user. *same paragraph*
`POST /api/v1/orders` add a new order to the service. *same paragraph*
`PUT /api/v1/orders/<orderId>` update the status of an order from the service.


### 3 . menu endpoints
`GET /api/v1/menu` returns a list of all menu items.*same paragraph*
`POST /api/v1/menu` adds a new menu item to the menu.*same paragraph*
`POST /api/v1/menu/remove` removes a  menu item from the menu.*same paragraph*
