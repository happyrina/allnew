create table buytbl (
    idnum       number(8) not null primary key,
    userid      char(8) not null,
    prodname    nchar(8) not null,
    groupname   nchar(4),
    price       number(8) not null,
    amount      number(3) not null,
    foreign key (userid) REFERENCES usertbl(userid)
);

create sequence idseq;
insert into buytbl values(idseq.nextval, 'KBS', '운동화', NULL, 30, 2);
insert into buytbl values(idseq.nextval, 'KBS', '노트', '전자', 1000, 1);
insert into buytbl values(idseq.nextval, 'JYP', '모니터', '전자', 200, 1);
insert into buytbl values(idseq.nextval, 'BBK', '모니터', '전자', 200, 1);
insert into buytbl values(idseq.nextval, 'KBS', '청바지', '의류', 50, 3);
insert into buytbl values(idseq.nextval, 'BBK', '메모리', '전자', 80, 10);
insert into buytbl values(idseq.nextval, 'SSK', '책', '서적', 15, 5);
insert into buytbl values(idseq.nextval, 'EJW', '책', '서적', 15, 2);
insert into buytbl values(idseq.nextval, 'EJW', '청바지', '의류', 50, 1);
insert into buytbl values(idseq.nextval, 'BBK', '운동화', NULL, 30, 2);
insert into buytbl values(idseq.nextval, 'EJW', '책', '서적', 15, 1);
insert into buytbl values(idseq.nextval, 'BBK', '운동화', NULL, 30, 2);


    