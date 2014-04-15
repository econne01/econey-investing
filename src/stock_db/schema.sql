DROP TABLE IF EXISTS stocks;
CREATE TABLE stocks (
  date date not null,
  ticker text not null,
  volume real not null,
  price real not null
);

DROP TABLE IF EXISTS macro_jobs;
CREATE TABLE macro_jobs (
  year smallint not null,
  month smallint not null,
  series_key varchar(13) not null,
  series_prefix varchar(2) not null,
  adjusted varchar(1) not null,
  supersector varchar(2) not null,
  industry varchar(6) not null,
  datatype varchar(2) not null,
  value real not null
);
