use testdb;

CREATE TABLE `user` ( 
	`user_id` bigint(20) not null auto_increment,
    `uuid` varchar(40) not null collate 'utf8mb4_unicode_520_ci',
	`name` varchar(20) not null collate 'utf8mb4_unicode_520_ci',
	`email` varchar(100) not null collate 'utf8mb4_unicode_520_ci',
	`password` varchar(100) not null collate 'utf8mb4_unicode_520_ci',
	`last_login_date` datetime null default current_timestamp,
	`created_at` datetime null default current_timestamp,
	`updated_at`  datetime NULL default current_timestamp on update current_timestamp,
    primary key(`user_id`)
);

