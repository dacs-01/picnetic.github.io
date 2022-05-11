drop database if exists picnetic_db;
CREATE DATABASE IF NOT EXISTS picnetic_db;
use picnetic_db;

create table if not exists users (
	user_id int not null auto_increment,
    user_name varchar(255) not null,
    email varchar(255) not null,
    f_name varchar(255) ,
    l_name varchar(255) ,
    passed longtext not null,
    primary key (user_id),
    unique (user_name)
);

create table if not exists friend (
	user_id int not null auto_increment,
    friend_id int not null,
    pending bool,
    primary key (user_id, friend_id),
    foreign key (user_id) references users (user_id),
    foreign key (friend_id) references users (user_id)
);

create table if not exists post (
	user_name varchar(255) not null,
    post_id int not null auto_increment,
    post_label varchar(255) default null,
    post_cap varchar(255) default null,
    post_picture varchar(255) not null,
    primary key (post_id),
    foreign key (user_name) references users (user_name)
);

create table if not exists comments (
    comment_id int not null auto_increment,
    user_id int not null,
    comment varchar(255),
    post_id int not null,
    primary key(comment_id),
    foreign key (user_id) references users (user_id),
    foreign key (post_id) references post (post_id)
);

create table if not exists contact (
	contact_id int not null auto_increment, 
	user_id int not null,
    date datetime,
    email varchar(45) not null,
    description varchar(255) default null,
    primary key (contact_id),
    foreign key (user_id) references users (user_id)
); 