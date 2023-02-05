create table IF NOT exists locker(
    lockerId SERIAL primary key ,
    capacity INTEGER,
    latitude real,
    longitude real
);

CREATE TABLE IF NOT exists parcel(
    parcelId SERIAL PRIMARY KEY,
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
    balance DECIMAL(10, 2) DEFAULT 0,
    username VARCHAR(50),
    pfpUrl VARCHAR(500),
    failedDeliveries INTEGER DEFAULT 0,
    succeededDeliveries INTEGER DEFAULT 0
    -- also need some way to hit them up via push notifications
);

CREATE TABLE IF NOT exists journey(
    journeyId SERIAL PRIMARY KEY,
    distributorId INTEGER,
    FOREIGN key(distributorId) REFERENCES distributor(distributorId)
);

create table IF NOT exists journeyPoint(
    ordinalNumber SERIAL,
    journeyId INTEGER, 
    arrivalTime TIME,
    latitude real,
    longitude real,
    foreign key(journeyId) references journey(journeyId)
);

CREATE TABLE route(
    routeId SERIAL primary key,
    parcelId INTEGER
);

CREATE TABLE routeEvent(
    leaveTime timestamp,
    arrivalTime timestamp,
    nextLockerId INTEGER,
    currLockerId INTEGER,
    routeId INTEGER,
    parcelId INTEGER,
    userDoing INTEGER,
    routeEventId INTEGER,
    FOREIGN KEY (parcelId) REFERENCES parcel(parcelId),
    FOREIGN KEY (nextLockerId) REFERENCES locker(lockerId),
    FOREIGN KEY (currLockerId) REFERENCES locker(lockerId),	
    FOREIGN KEY (routeId) REFERENCES route(routeId),
    FOREIGN KEY (userDoing) REFERENCES distributor(distributorId)   
);
	