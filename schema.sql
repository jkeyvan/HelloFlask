drop table if exists entries;
create table entries (id integer primary key autoincrement,title text not null,text text not null);
create table members (id integer PRIMARY KEY autoincrement, username text not null , email text not null, password text not null)
