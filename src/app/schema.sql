CREATE TABLE IF NOT EXISTS stocks (
  date date not null,
  ticker text not null,
  volume real not null,
  price real not null
);

CREATE TABLE IF NOT EXISTS results_year (
  ticker text not null,
  year smallint not null,
  revenue real null,
  interest real null,
  net_income real null
);
CREATE UNIQUE INDEX IF NOT EXISTS IDX_Ticker_Year ON results_year (ticker, year);

CREATE TABLE IF NOT EXISTS macro_jobs (
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
