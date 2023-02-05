INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.4999, -0.1781);
INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.4994, -0.1771);
INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.5009, -0.1774);
INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.4998, -0.1757);
INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.5013, -0.1248);
INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.4994, -0.1771);
INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.5007, -0.1246);

INSERT INTO distributor ( balance, username, pfpUrl, failedDeliveries, succeededDeliveries)
    VALUES ( 100.12, 'bross', 'https://www.bobross.com/content/bob_ross_img.png', 1, 1000);
INSERT INTO distributor ( balance, username, pfpUrl, failedDeliveries, succeededDeliveries)
    VALUES ( 31.43, 'mbuble', 'https://upload.wikimedia.org/wikipedia/commons/f/f9/MichaelBubleSmileeb2011.jpg', 0, 300);

-- in delivery
INSERT INTO parcel(dateIntoSystem, dateIntoLocker, lockerIn, destinationLocker, inTransit)
   VALUES ('2023-02-05 11:23:44', '2023-02-06 1:52:31', 1, 7, false);
-- delivered
--INSERT INTO parcel(parcelId, dateIntoSystem, dateIntoLocker, lockerIn, destinationLocker, inTransit)
--    VALUES (1, '2023-02-03 9:12:00', '2023-02-03 18:41:59', 6, 1, false)
-- to be delivered
--INSERT INTO parcel(parcelId, dateIntoSystem, dateIntoLocker, lockerIn, destinationLocker, inTransit)
--    VALUES (2, '2023-02-04 10:11:04', '2023-02-04 10:02:36', 3, 4, false)

INSERT INTO journey ( distributorId) VALUES ( 1);
INSERT INTO journey ( distributorId) VALUES ( 2);

INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
    VALUES (0, 1, '8:25:00', 51.4996, -0.1771);
INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
    VALUES (1, 1, '9:14:18', 50.4996, -0.1782);
INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
    VALUES (2, 1, '10:54:32', 51.5007, -0.1782);

INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
    VALUES (0, 2, '16:57:42', 51.4999, -0.1781);
INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
    VALUES (1, 2, '18:05:01', 51.5007, -0.1246);




--INSERT INTO route (routeId, parcelId)
--    VALUES (0, 0)
INSERT INTO route (parcelId) VALUES (1);

-- Garbage
INSERT INTO routeEvent (leaveTime, arrivalTime, nextLockerId, currLockerId, routeId, parcelId, userDoing, journeyPointStartId, journeyPointEndId)
   VALUES ('2023-02-05 11:23:44', '2023-02-05 11:23:46', 7, 1, 1, 1,  2, 4, 5);
