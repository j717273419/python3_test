CREATE TABLE news_cnbeta
(
  news_id      INT AUTO_INCREMENT
    PRIMARY KEY,
  news_time    TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  news_author  CHAR(100)                           NULL,
  news_content MEDIUMTEXT                          NULL,
  is_check     INT                                 NULL,
  is_delete    INT                                 NULL,
  news_title   VARCHAR(200)                        NULL,
  news_url     VARCHAR(500)                        NULL
)
  ENGINE = InnoDB
  CHARSET = utf8;


