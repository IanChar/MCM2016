use MCM;

drop table if exists TimeSlice;
drop table if exists Donation;
drop table if exists School;
drop table if exists Location;

CREATE table Location (
    loc_id      INT not null auto_increment,
    city        varchar(24) not null,
    state       varchar(24) not null,
    primary key (loc_id),
    UNIQUE KEY (city, state)
);

CREATE table School (
    unit_id     DECIMAL(8, 0),
    name        varchar(65),
    loc_id      INT,
    primary key (unit_id),
    foreign key (loc_id) references Location (loc_id) on delete cascade
);

CREATE table TimeSlice (
    t_id        int not null auto_increment,
    unit_id     DECIMAL(8, 0),
    ug          FLOAT(7,0),
    ug_nra      FLOAT(7,0),
    ug_unkn     FLOAT(7,0),
    ug_whitenh  FLOAT(7,0),
    ug_blacknh  FLOAT(7,0),
    ug_api      FLOAT(7,0),
    ug_aianold  FLOAT(7,0),
    ug_hispold  FLOAT(7,0),
    tuition_in  FLOAT(7,2),
    tuition_out FLOAT(7,2),
    tuitfte     FLOAT(7,2),
    inexpfte    FLOAT(7,2),
    d150_l4     FLOAT(7,0),
    yr2cmp      FLOAT(4,3),
    yr2wdr      FLOAT(4,3),
    fyr2cmp     FLOAT(4,3),
    fyr2wdr     FLOAT(4,3),
    yr3cmp      FLOAT(4,3),
    yr3wdr      FLOAT(4,3),
    yr4cmp      FLOAT(4,3),
    yr4wdr      FLOAT(4,3),
    findep      FLOAT(4,3),
    frstgen     FLOAT(4,3),
    parms       FLOAT(4,3),
    parhs       FLOAT(4,3),
    parps       FLOAT(4,3),
    indavg      FLOAT(8,2),
    depavg      FLOAT(8,2),
    debtgrad    FLOAT(7,2),
    debtngrad   FLOAT(7,2),
    debtdep     FLOAT(7,2),
    debtind     FLOAT(7,2),
    debtfem     FLOAT(7,2),
    debtmal     FLOAT(7,2),
    debtfrst    FLOAT(7,2),
    debtnfrst   FLOAT(7,2),
    repaydebt   INT,
    year        DECIMAL(4, 0),
    primary key (t_id),
    foreign key (unit_id) references School (unit_id) on delete cascade
);

CREATE table Donation (
    grant_id    int not null auto_increment,
    unit_id     DECIMAL(8,0),
    loc_id      INT,
    start_year  INT,
    end_year    INT,
    amount      DECIMAL(11, 2),
    primary key (grant_id),
    foreign key (unit_id) references School (unit_id) on delete cascade,
    foreign key (loc_id) references Location (loc_id) on delete cascade
);
