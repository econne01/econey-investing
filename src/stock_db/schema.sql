DROP TABLE IF EXISTS stocks;
CREATE TABLE stocks (
  date date not null,
  ticker text not null,
  volume real not null,
  price real not null
);