#!/bin/bash

mysql -u dhs -ptitans -t << EOF  > uva_practice.txt
SELECT name,status,COUNT(*)
FROM uva.practice
WHERE status = 'complete'
GROUP BY name
ORDER BY name,COUNT(*);

SELECT name,status,COUNT(*)
FROM uva.practice
GROUP BY name,status
ORDER BY name,status;

SELECT name,problem,status
FROM uva.practice
ORDER BY name,status;
EOF
