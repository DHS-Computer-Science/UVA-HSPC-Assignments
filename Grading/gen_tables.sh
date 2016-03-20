#!/bin/bash
tmp=""
for i in `mysql -u dhs -ptitans -Ne "
SELECT DISTINCT
  SUBSTRING_INDEX(problem, '-', -1) AS difficulty
FROM uva.practice WHERE status = 'complete'
ORDER BY difficulty "`
do
  tmp="$tmp,SUM(case WHEN SUBSTRING_INDEX(problem, '-', -1) = $i then 1 else 0 end) '$i'"
done

mysql -u dhs -ptitans -t > uva_practice.txt -e "
SELECT
  name,
  COUNT(*) AS '# complete'
FROM uva.practice
WHERE status = 'complete'
GROUP BY name
ORDER BY '# complete' DESC;

SELECT
  name
  $tmp
FROM uva.practice
WHERE status = 'complete'
GROUP BY name
ORDER BY name;

SELECT
  name,
  status,
  COUNT(*) AS 'number'
FROM uva.practice
GROUP BY name,status
ORDER BY name,status;

SELECT
  name,
  problem,
  status
FROM uva.practice
ORDER BY name,status;
"
