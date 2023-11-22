#!/bin/bash
set -e

mongo -- "$MONGO_INITDB_db" <<EOF
    print('###### Start creating db ###########')
    db.createUser({user: '$MONGO_USER', pwd: '$MONGO_PASSWORD', roles:[{role: 'readWrite', db: '$MONGO_INITDB_db'}]})
EOF

