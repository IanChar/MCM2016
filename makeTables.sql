use MCM;

drop table if exists TimeSlice;
drop table if exists Donation;
drop table if exists School;
drop table if exists Location;

CREATE table Location (
    loc_id      int not null auto_increment,
    city        varchar(24) not null,
    state       varchar(24) not null,
    primary key (loc_id)
);

CREATE table School (
    unit_id     DECIMAL(8, 0),
    name        varchar(65),
    loc_id      int not null,
    primary key (unit_id),
    foreign key (loc_id) references Location (loc_id) on delete cascade
);

CREATE table TimeSlice (
    t_id        int not null auto_increment,
    unit_id     DECIMAL(8, 0),
    preddeg     INT,
    control     INT,
    pcip51      FLOAT(6,5),
    pcip52      FLOAT(6,5),
    ugds        INT,
    ugds_white  FLOAT(6,5),
    ugds_black  FLOAT(6,5),
    ugds_hisp   FLOAT(6,5),
    ugds_asian  FLOAT(6,5),
    ugds_AIAN   FLOAT(6,5),
    ugds_nhpi   FLOAT(6,5),
    ugds_2mor   FLOAT(6,5),
    ugds_nra    FLOAT(6,5),
    ugds_unkn   FLOAT(6,5),
    pptug_ef    INT,
    pctpell     FLOAT(6,5),
    pctfloan    FLOAT(6,5),
    ug25avb     FLOAT(6,5),
    gdmdn       INT,
    gmdn10      INT,
    rpy3yr      FLOAT(6,5),
    mdearn      FLOAT(5, 2),
    primary key (t_id),
    foreign key (unit_id) references School (unit_id) on delete cascade
);

CREATE table Donation (
    grant_id    int not null,
    unit_id     DECIMAL(8,0),
    loc_id      INT,
    start_year  INT,
    end_year    INT,
    amount      DECIMAL(7, 2),
    primary key (grant_id),
    foreign key (unit_id) references School (unit_id) on delete cascade,
    foreign key (loc_id) references Location (loc_id) on delete cascade
);
