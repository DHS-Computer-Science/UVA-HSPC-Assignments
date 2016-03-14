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