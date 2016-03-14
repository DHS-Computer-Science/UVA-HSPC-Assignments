# Grader

To create a the table for results

```
CREATE SCHEMA `uva` ;
CREATE TABLE `uva`.`practice` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `problem` VARCHAR(45) NULL,
  `status` VARCHAR(45) NULL,
  `date` INT NULL,
  PRIMARY KEY (`id`));
```

mysql -u dhs -ptitans -e "select name,problem,status from uva.practice; SELECT name,status,COUNT(status) from uva.practice GROUP BY name ORDER BY Status DESC" -t > uva_practice.txt