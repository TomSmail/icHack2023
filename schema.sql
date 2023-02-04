CREATE TABLE locker(
    lockerId INTEGER PRIMARY KEY AUTOINCREMENT,
    capacity INTEGER,
    latitude REAL,
    longitude REAL
);

CREATE TABLE parcel(
    parcelId INTEGER PRIMARY KEY AUTOINCREMENT,
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
    journeyId INTEGER PRIMARY KEY AUTOINCREMENT,
    startTime TIME, 
    endTime TIME,
    userId INTEGER,
    FOREIGN KEY userId REFERENCES user.userId
);

CREATE TABLE point(
    pointId INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude REAL,
    longitude REAL
);

CREATE TABLE journeyPoint(
    ordinalNumber INTEGER,
    journeyId INTEGER,
    pointId INTEGER,
    FOREIGN KEY journeyId REFERENCES journey.journeyId,
    FOREIGN KEY pointId REFERENCES point.pointId
);