drop table if exists child;
drop table if exists parent;

create table parent (
    id int not null,
    description text,
    primary key (id)
) engine=innodb;


create table child (
    cid int,
    pid int,
    description text,

    foreign key (pid)
        references parent(id)
        on delete cascade
) engine=innodb;


insert into parent (id, description) values (0, 'foo0');
insert into parent (id, description) values (1, 'foo1');
insert into parent (id, description) values (2, 'foo2');

insert into child (cid, pid, description) values (0, 1, 'bar0');
insert into child (cid, pid, description) values (1, 1, 'bar1');    
insert into child (cid, pid, description) values (2, 0, 'bar2');        
insert into child (cid, pid, description) values (3, 2, 'bar3');        
