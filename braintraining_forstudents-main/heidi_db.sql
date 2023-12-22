-- MySQL Script generated by MySQL Workbench
-- Mon Nov  6 12:08:30 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mygame
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mygame
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `mygame`;

CREATE SCHEMA IF NOT EXISTS `mygame` DEFAULT CHARACTER SET utf8 ;
USE `mygame` ;

-- -----------------------------------------------------
-- Table `mygame`.`game`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mygame`.`results` (
  `idgame` INT NOT NULL,
  `exercise` VARCHAR(45) NOT NULL,
  `date_hour` DATE NOT NULL,
  `duration` TIME NOT NULL,
  `nbok` INT NOT NULL,
  PRIMARY KEY (`idgame`, `exercise`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `mygame`.`users` (
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `level` INT NOT NULL,
  PRIMARY KEY (`username`))
ENGINE = INNODB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
