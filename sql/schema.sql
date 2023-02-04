create table locker(
    lockerId SERIAL primary key ,
    capacity INTEGER,
    latitude real,
    longitude real
);

CREATE TABLE parcel(
    parcelId  SERIAL PRIMARY KEY,
    dateIntoSystem DATE,
    dateIntoLocker DATE,
    lockerIn INTEGER,
    destinationLocker INTEGER,
    inTransit BOOLEAN,
    FOREIGN KEY lockerIn REFERENCES locker.lockerId,
    FOREIGN KEY destinationLocker REFERENCES locker.lockerId
);

CREATE TABLE user(
    balance DECIMAL(10, 2),
    failedDeliveries INTEGER,
    succeededDeliveries INTEGER
);

CREATE TABLE journey(
    journeyId SERIAL PRIMARY KEY,
    startTime TIME, 
    endTime TIME,
    userId INTEGER,
    FOREIGN key(userId) REFERENCES user.userId
);

create table point(
    pointId SERIAL primary key,
    latitude real,
    longitude real
);

create table journeyPoint(
    ordinalNumber INTEGER,
    journeyId INTEGER,
    pointId INTEGER,
    foreign key(journeyId) references journey.journeyId,
    foreign key(pointId) references point.pointId
);