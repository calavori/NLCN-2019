create database project;
use project;

create table students(
	id varchar(8) primary key,
    name varchar(20)
    );
    
create table dataset(
	id varchar(15) primary key,
    s_id varchar(8) not null,
    foreign key (s_id) references students(id) on delete cascade
    );
    
create table attendance(
	d_id varchar(15),
    time timestamp not null,
    status varchar(3) not null,
    foreign key (d_id) references dataset(id) on delete cascade
    );



DELIMITER $$
CREATE PROCEDURE attend(d_id varchar(15), sid varchar(8))
BEGIN
   declare cur_time timestamp;
   declare stt varchar(3);
   insert into `dataset` values (d_id, sid);
   select current_timestamp() into cur_time; 
   select status into stt
   from `attendance` join `dataset` on attendance.d_id = dataset.id
   where date(time) = date(cur_time) and dataset.s_id = sid
   order by abs(timediff(time, current_time)) limit 1;
   if stt = "in" then 
	insert into `attendance` values (d_id, cur_time, "out");
   else
	insert into `attendance` values (d_id, cur_time, "in");
   end if;
END; $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE attendList(d varchar(12))
BEGIN
   select s.id, s.name, a.d_id, a.time, a.status from students as s join
   (select * from attendance join dataset on attendance.d_id = dataset.id where date(attendance.time) = d) as a
   on s.id = a.s_id;
END; $$
DELIMITER ;
