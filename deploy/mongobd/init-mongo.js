print('###### Start creating db ###########')

db = db.getSiblingDB('ml_product_mongo')
db.createUser(
    {
        user: "admin1",
        pwd: "pass123357789",
        roles: [
            {
                role: "readWrite",
                db: "ml_product_mongo"
            }
        ]
    }
)