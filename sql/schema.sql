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

CREATE TABLE IF NOT exists distributor(
    distributorId SERIAL PRIMARY KEY,
    balance DECIMAL(10, 2),
    username VARCHAR(50),
    pfpUrl VARCHAR(100),
    failedDeliveries INTEGER,
    succeededDeliveries INTEGER
    -- also need some way to hit them up via push notifications
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
    ordinalNumber SERIAL,
    journeyId INTEGER,
    pointId INTEGER,
    foreign key(journeyId) references journey(journeyId),
    foreign key(pointId) references point(pointId)
);

CREATE TABLE route(
    routeId SERIAL primary key,
    userDoing INTEGER,
    parcelId INTEGER,
    FOREIGN KEY (userDoing) REFERENCES distributor(distributorId)   
);

CREATE TABLE routeEvent(
    timeOccurs timestamp,
    nextLockerId INTEGER,
    routeId INTEGER,
    parcelId INTEGER,
    FOREIGN KEY (parcelId) REFERENCES parcel(parcelId),
    FOREIGN KEY (nextLockerId) REFERENCES locker(lockerId),
    FOREIGN KEY (routeId) REFERENCES route(routeId)
);
	