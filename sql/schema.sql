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
    distributorId SERIAL PRIMARY KEY,
    balance DECIMAL(10, 2),
    username VARCHAR(50),
    pfpUrl VARCHAR(100)
    failedDeliveries INTEGER,
    succeededDeliveries INTEGER,
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
    ordinalNumber INTEGER,
    journeyId INTEGER,
    pointId INTEGER,
<<<<<<< HEAD
    foreign key(journeyId) references journey(journeyId),
    foreign key(pointId) references point(pointId)
);
=======
    FOREIGN KEY journeyId REFERENCES journey.journeyId,
    FOREIGN KEY pointId REFERENCES point.pointId
);

CREATE TABLE route(
    routeId INTEGER,
    userDoing INTEGER
    parcelId INTEGER,
    FOREIGN KEY userDoing REFERENCES user.userId    
);

CREATE TABLE routeEvent(
    timeOccurs DATETIME,
    nextLockerId INTEGER,
    routeId INTEGER,
    FOREIGN KEY parcelId REFERENCES parcel.parcelId,
    FOREIGN KEY nextLockerId REFERENCES locker.lockerId,
    FOREIGN KEY routeId REFERENCES route.routeId
);
>>>>>>> 18d9a50c76db1be26cb1f66b40a988cf01b8e130
