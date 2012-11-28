drop table if exists users;
drop table if exists polls;
drop table if exists questions;
drop table if exists choices;
drop table if exists votes;

create table users (
  id integer primary key autoincrement,
  username text not null,
  firstname text not null,
  lastname text not null,
  password text not null
);

create table polls (
  id integer primary key autoincrement,
  user_id integer not null,
  title text not null,
  state integer not null   -- 0 
);

create table questions (
  id integer primary key autoincrement,
  poll_id integer not null,
  question text not null
);

create table choices (
  id integer primary key autoincrement,
  question_id integer not null,
  choice text not null
);

create table votes (
  id integer primary key autoincrement,
  choice_id integer not null,
  user_id integer not null,
  vote integer not null
);
