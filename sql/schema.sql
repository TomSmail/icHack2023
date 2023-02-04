create table IF NOT exists locker(
    lockerId SERIAL primary key ,
    capacity INTEGER,
    latitude real,
    longitude real
);

CREATE TABLE  IF NOT exists parcel(
    parcelId  SERIAL PRIMARY KEY,
    dateIntoSystem DATE,
    dateIntoLocker DATE,
    lockerIn INTEGER,
    destinationLocker INTEGER,
    inTransit BOOLEAN,
    FOREIGN KEY (lockerIn) REFERENCES locker(lockerId),
    FOREIGN KEY(destinationLocker) REFERENCES locker(lockerId)
);

CREATE TABLE  IF NOT exists distributor(
    balance DECIMAL(10, 2),
    failedDeliveries INTEGER,
    succeededDeliveries INTEGER
);

CREATE TABLE IF NOT exists journey(
    journeyId SERIAL PRIMARY KEY,
    startTime TIME, 
    endTime TIME,
    distributorId INTEGER,
    FOREIGN key(distributorId) REFERENCES distributor(distributorId)
);

create table IF NOT exists point(
    pointId SERIAL primary key,
    latitude real,
    longitude real
);

create table IF NOT exists journeyPoint(
    ordinalNumber INTEGER,
    journeyId INTEGER,
    pointId INTEGER,
    foreign key(journeyId) references journey(journeyId),
    foreign key(pointId) references point(pointId)
);