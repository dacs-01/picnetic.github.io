CREATE DATABASE IF NOT EXISTS picnetic_db;
use picnetic_db;

create table if not exists friend (
	user_id int not null,
    friend_id int not null,
    pending bool,
    primary key (user_id, friend_id)
);

create table if not exists post (
	user_name varchar(255) not null,
    post_id int not null,
    post_label enum('campus','sports',
    'stuorg','norm','alums','meme'),
    post_cap varchar(255) null,
    com_thread_id int not null,
    primary key (post_id),
    foreign key (com_thread_id) references comments(com_thread_id)
);

create table if not exists comments (
	com_thread_id int not null,
    user_id int not null,
    comment varchar(255),
    primary key(com_thread_id),
    foreign key (user_id) references friend(user_id)
);