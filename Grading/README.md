# Grader

## Install Dependancies
- be sure to have mysql, python3, and pip3 installed
  - more instructions in the DHS-HSPC repo Grader directory
- run `sudo pip3 install gitpython pymysql PyGithub`

## Setup
- You will also need to create tables
- To create a the table for results, run these mysql commands:
- Also make sure that old UVA practice problems are deleted from github
  - Unless you want to keep them
  - To find them search for `uva-hspc-practice` on
    [the club github page] (https://github.com/DHS-Computer-Science)
    under repositories(**NOT** the search bar at the very top)

```
CREATE SCHEMA IF NOT EXISTS `uva` ;
DROP TABLE IF EXISTS `uva`.`practice`;
CREATE TABLE `uva`.`practice` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `login` VARCHAR(25) NULL,
  `problem` VARCHAR(45) NULL,
  `status` VARCHAR(45) NULL,
  `date` INT NULL,
  PRIMARY KEY (`id`));
```

## Usage
- Run `./grader.py` to read info from github and grade stuff
  - There is a (daily, I think) limit to queries using the githubapi
  - This will update the mysql table with info
- Run `./gen_tables.sh` to get formatted info from mysql
  - The generated tables will appear in `uva_practice.txt`

## Notes
- Be sure to have:
  - Code writen in the Main.java file
  - Test input and output in `in-out/judging.in` and `in-out/judging.out`
    in the repo that is stored on github
  - java and javac installed and availible in the path
- For names to show up properly, have students (not sure if students is the
  best term to use) go to their [settings page]
  (https://github.com/settings/profile) and set their names
    - Otherwise their usernames will be used
    - Changes will take effect the next time `./grader.py` is run
      - Although you'll still need to run `./gen_tables.sh` after that to
        update the tables
