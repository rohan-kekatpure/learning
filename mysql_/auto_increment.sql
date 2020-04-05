drop table if exists enum_foo;

create table enum_foo (
    code smallint(6) auto_increment,
    definition varchar(64),
    primary key (code),
    constraint unique_definition unique(definition)
) engine=innodb;