print('###### Start creating db ###########')

db = db.getSiblingDB('think_mongo')
db.createUser(
    {
        user: "zfCxePvYBPHa3w",
        pwd: "jV9xRs8tZ",
        roles: [
            {
                role: "readWrite",
                db: "think_mongo"
            }
        ]
    }
)