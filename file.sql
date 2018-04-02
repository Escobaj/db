-- MySQL Script generated by MySQL Workbench
-- Sun Apr  1 18:50:10 2018
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `db` ;

-- -----------------------------------------------------
-- Schema db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `db` DEFAULT CHARACTER SET utf8 ;
USE `db` ;

-- -----------------------------------------------------
-- Table `db`.`table1`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`table1` ;

CREATE TABLE IF NOT EXISTS `db`.`table1` (
)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`users` ;

CREATE TABLE IF NOT EXISTS `db`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `password` VARCHAR(32) NOT NULL,
  `created` DATETIME GENERATED ALWAYS AS (NOW()) VIRTUAL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`series`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`series` ;

CREATE TABLE IF NOT EXISTS `db`.`series` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `release` YEAR NULL,
  `end` YEAR NULL,
  `status` VARCHAR(45) NULL,
  `duration` INT NULL,
  `nb_saison` INT NULL,
  `description` TEXT NULL,
  `picture` TINYTEXT NULL,
  `awards` TINYTEXT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`movies`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`movies` ;

CREATE TABLE IF NOT EXISTS `db`.`movies` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `release` YEAR NULL,
  `duration` INT NULL,
  `description` TEXT NULL,
  `awards` TEXT NULL,
  `picture` TINYTEXT NULL,
  `production` TINYTEXT NULL,
  `box_office` INT NULL,
  `website` TINYTEXT NULL,
  `rated` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`evaluate_movie`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`evaluate_movie` ;

CREATE TABLE IF NOT EXISTS `db`.`evaluate_movie` (
  `users_id` INT NOT NULL,
  `movies_id` INT NOT NULL,
  `comment` TEXT NULL,
  `rate` INT(2) NULL,
  `created` DATETIME NULL,
  `updated` DATETIME NULL,
  PRIMARY KEY (`users_id`, `movies_id`),
  INDEX `fk_users_has_movies_movies1_idx` (`movies_id` ASC),
  INDEX `fk_users_has_movies_users_idx` (`users_id` ASC),
  UNIQUE INDEX `user_movie_unique` (`users_id` ASC, `movies_id` ASC),
  CONSTRAINT `fk_users_has_movies_users`
    FOREIGN KEY (`users_id`)
    REFERENCES `db`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_movies_movies1`
    FOREIGN KEY (`movies_id`)
    REFERENCES `db`.`movies` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`evaluate_serie`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`evaluate_serie` ;

CREATE TABLE IF NOT EXISTS `db`.`evaluate_serie` (
  `users_id` INT NOT NULL,
  `series_id` INT NOT NULL,
  `comment` TEXT NULL,
  `rate` INT NULL,
  `created` DATETIME NULL,
  `updated` DATETIME NULL,
  `evaluate_seriecol` VARCHAR(45) NULL,
  PRIMARY KEY (`users_id`, `series_id`),
  INDEX `fk_users_has_series_series1_idx` (`series_id` ASC),
  INDEX `fk_users_has_series_users1_idx` (`users_id` ASC),
  UNIQUE INDEX `user_serie_unique` (`users_id` ASC, `series_id` ASC),
  CONSTRAINT `fk_users_has_series_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `db`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_series_series1`
    FOREIGN KEY (`series_id`)
    REFERENCES `db`.`series` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`characters`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`characters` ;

CREATE TABLE IF NOT EXISTS `db`.`characters` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fullname` VARCHAR(255) NOT NULL,
  `picture` TINYTEXT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`genres`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`genres` ;

CREATE TABLE IF NOT EXISTS `db`.`genres` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`countries`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`countries` ;

CREATE TABLE IF NOT EXISTS `db`.`countries` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`countrie_serie`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`countrie_serie` ;

CREATE TABLE IF NOT EXISTS `db`.`countrie_serie` (
  `series_id` INT NOT NULL,
  `countries_id` INT NOT NULL,
  PRIMARY KEY (`series_id`, `countries_id`),
  INDEX `fk_series_has_countries_countries1_idx` (`countries_id` ASC),
  INDEX `fk_series_has_countries_series1_idx` (`series_id` ASC),
  CONSTRAINT `fk_series_has_countries_series1`
    FOREIGN KEY (`series_id`)
    REFERENCES `db`.`series` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_series_has_countries_countries1`
    FOREIGN KEY (`countries_id`)
    REFERENCES `db`.`countries` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`countrie_movie`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`countrie_movie` ;

CREATE TABLE IF NOT EXISTS `db`.`countrie_movie` (
  `movies_id` INT NOT NULL,
  `countries_id` INT NOT NULL,
  PRIMARY KEY (`movies_id`, `countries_id`),
  INDEX `fk_movies_has_countries_countries1_idx` (`countries_id` ASC),
  INDEX `fk_movies_has_countries_movies1_idx` (`movies_id` ASC),
  CONSTRAINT `fk_movies_has_countries_movies1`
    FOREIGN KEY (`movies_id`)
    REFERENCES `db`.`movies` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_movies_has_countries_countries1`
    FOREIGN KEY (`countries_id`)
    REFERENCES `db`.`countries` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`genre_movie`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`genre_movie` ;

CREATE TABLE IF NOT EXISTS `db`.`genre_movie` (
  `movies_id` INT NOT NULL,
  `genres_id` INT NOT NULL,
  PRIMARY KEY (`movies_id`, `genres_id`),
  INDEX `fk_movies_has_genres_genres1_idx` (`genres_id` ASC),
  INDEX `fk_movies_has_genres_movies1_idx` (`movies_id` ASC),
  CONSTRAINT `fk_movies_has_genres_movies1`
    FOREIGN KEY (`movies_id`)
    REFERENCES `db`.`movies` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_movies_has_genres_genres1`
    FOREIGN KEY (`genres_id`)
    REFERENCES `db`.`genres` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`genre_serie`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`genre_serie` ;

CREATE TABLE IF NOT EXISTS `db`.`genre_serie` (
  `series_id` INT NOT NULL,
  `genres_id` INT NOT NULL,
  PRIMARY KEY (`series_id`, `genres_id`),
  INDEX `fk_series_has_genres_genres1_idx` (`genres_id` ASC),
  INDEX `fk_series_has_genres_series1_idx` (`series_id` ASC),
  CONSTRAINT `fk_series_has_genres_series1`
    FOREIGN KEY (`series_id`)
    REFERENCES `db`.`series` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_series_has_genres_genres1`
    FOREIGN KEY (`genres_id`)
    REFERENCES `db`.`genres` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`roles`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`roles` ;

CREATE TABLE IF NOT EXISTS `db`.`roles` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`character_serie`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`character_serie` ;

CREATE TABLE IF NOT EXISTS `db`.`character_serie` (
  `series_id` INT NOT NULL,
  `characters_id` INT NOT NULL,
  `roles_id` INT NOT NULL,
  PRIMARY KEY (`series_id`, `characters_id`, `roles_id`),
  INDEX `fk_series_has_characters_characters1_idx` (`characters_id` ASC),
  INDEX `fk_series_has_characters_series1_idx` (`series_id` ASC),
  INDEX `fk_character_serie_roles1_idx` (`roles_id` ASC),
  CONSTRAINT `fk_series_has_characters_series1`
    FOREIGN KEY (`series_id`)
    REFERENCES `db`.`series` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_series_has_characters_characters1`
    FOREIGN KEY (`characters_id`)
    REFERENCES `db`.`characters` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_character_serie_roles1`
    FOREIGN KEY (`roles_id`)
    REFERENCES `db`.`roles` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`character_movie`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`character_movie` ;

CREATE TABLE IF NOT EXISTS `db`.`character_movie` (
  `movies_id` INT NOT NULL,
  `characters_id` INT NOT NULL,
  `roles_id` INT NOT NULL,
  PRIMARY KEY (`movies_id`, `characters_id`, `roles_id`),
  INDEX `fk_movies_has_characters_movies1_idx` (`movies_id` ASC),
  INDEX `fk_character_movie_roles1_idx` (`roles_id` ASC),
  CONSTRAINT `fk_movies_has_characters_movies1`
    FOREIGN KEY (`movies_id`)
    REFERENCES `db`.`movies` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_character_movie_roles1`
    FOREIGN KEY (`roles_id`)
    REFERENCES `db`.`roles` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`wish_list_series`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`wish_list_series` ;

CREATE TABLE IF NOT EXISTS `db`.`wish_list_series` (
  `users_id` INT NOT NULL,
  `series_id` INT NOT NULL,
  PRIMARY KEY (`users_id`, `series_id`),
  INDEX `fk_users_has_series_series2_idx` (`series_id` ASC),
  INDEX `fk_users_has_series_users2_idx` (`users_id` ASC),
  CONSTRAINT `fk_users_has_series_users2`
    FOREIGN KEY (`users_id`)
    REFERENCES `db`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_series_series2`
    FOREIGN KEY (`series_id`)
    REFERENCES `db`.`series` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `db`.`wish_list_movies`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `db`.`wish_list_movies` ;

CREATE TABLE IF NOT EXISTS `db`.`wish_list_movies` (
  `users_id` INT NOT NULL,
  `movies_id` INT NOT NULL,
  PRIMARY KEY (`movies_id`),
  INDEX `fk_users_has_movies_movies2_idx` (`movies_id` ASC),
  INDEX `fk_users_has_movies_users1_idx` (`users_id` ASC),
  CONSTRAINT `fk_users_has_movies_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `db`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_movies_movies2`
    FOREIGN KEY (`movies_id`)
    REFERENCES `db`.`movies` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
