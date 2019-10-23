create database project;
use project;

create table students(
	id varchar(8) primary key,
    name varchar(20)
    );
    
create table dataset(
	id varchar(15) primary key,
    s_id varchar(8) not null,
    foreign key (s_id) references students(id)
    );
    
create table attendance(
	d_id varchar(15),
    time timestamp not null,
    status varchar(3) not null,
    foreign key (d_id) references dataset(id)
    );


DELIMITER $$
CREATE PROCEDURE addData(s_id varchar(8), name varchar(20), d_id varchar(15))
BEGIN
   insert into `students` values (s_id, name);
   insert into `dataset` values (d_id, s_id);
END; $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE attend(d_id varchar(15), s_id varchar(8), status varchar(3))
BEGIN
   declare current_time timestamp;
   insert into `dataset` values (d_id, s_id);
   select current_timestamp() into current_time; 
   insert into `attendance` values (d_id, current_time, );
END; $$
DELIMITER ;