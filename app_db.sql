drop database if exists picnetic_db;
CREATE DATABASE IF NOT EXISTS picnetic_db;
use picnetic_db;

create table if not exists users (
	user_id int not null,
    user_name varchar(45) not null,
    f_name varchar(45) not null,
    l_name varchar(45) not null,
    primary key (user_id),
    unique (user_name)
);

create table if not exists friend (
	user_id int not null,
    pending bool,
    primary key (user_id),
    foreign key (user_id) references users (user_id)
);

create table if not exists comments (
	com_thread_id int not null,
    user_id int not null,
    comment varchar(255),
    primary key(com_thread_id),
    foreign key (user_id) references users (user_id)
);

create table if not exists post (
	user_name varchar(45) not null,
    post_id int not null,
    post_label enum('campus','sports',
    'stuorg','norm','alums','meme'),
    post_cap varchar(255) null,
    com_thread_id int not null,
    primary key (post_id),
    foreign key (com_thread_id) references comments (com_thread_id),
    foreign key (user_name) references users (user_name)
);

create table if not exists contact (
	user_id int not null,
    date datetime,
    email varchar(45) not null,
    description varchar(255) null,
    primary key (user_id)
); 
