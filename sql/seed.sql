INSERT INTO locker(lockerId, capacity, latitude, longitude) VALUES (0, 200, 51.4999, -0.1781)
INSERT INTO locker(lockerId, capacity, latitude, longitude) VALUES (1, 200, 51.4994, -0.1771)
INSERT INTO locker(lockerId, capacity, latitude, longitude) VALUES (2, 200, 51.5009, -0.1774)
INSERT INTO locker(lockerId, capacity, latitude, longitude) VALUES (3, 200, 51.4998, -0.1757)

INSERT INTO locker(lockerId, capacity, latitude, longitude) VALUES (4, 200, 51.5013, -0.1248)
INSERT INTO locker(lockerId, capacity, latitude, longitude) VALUES (5, 200, 51.4994, -0.1771)
INSERT INTO locker(lockerId, capacity, latitude, longitude) VALUES (6, 200, 51.5007, -0.1246)


-- in delivery
--INSERT INTO parcel(parcelId, dateIntoSystem, dateIntoLocker, lockerIn, destinationLocker, inTransit)
--    VALUES (0, '2023-02-05 11:23:44', '2023-02-06 1:52:31', 0, 5, true)
-- delivered
--INSERT INTO parcel(parcelId, dateIntoSystem, dateIntoLocker, lockerIn, destinationLocker, inTransit)
--    VALUES (1, '2023-02-03 9:12:00', '2023-02-03 18:41:59', 6, 1, false)
-- to be delivered
--INSERT INTO parcel(parcelId, dateIntoSystem, dateIntoLocker, lockerIn, destinationLocker, inTransit)
--    VALUES (2, '2023-02-04 10:11:04', '2023-02-04 10:02:36', 3, 4, false)

INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
    VALUES (0, 0, '8:25:00', 51.4996, -0.1771)
INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
    VALUES (1, 0, '9:14:18', 50.4996, -0.1782)
INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
    VALUES (1, 0, '10:54:32', 51.5007, -0.1782)

INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
    VALUES (0, 1, '16:57:42', 51.4996, -0.1771)
INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
    VALUES (1, 1, '18:05:01', 50.4996, -0.1784)

INSERT INTO journey (journeyId, distributorId) VALUES (0, 0)
INSERT INTO journey (journeyId, distributorId) VALUES (1, 1)

INSERT INTO distributor (distributorId, balance, username, pfpUrl, failedDeliveries, succeededDeliveries)
    VALUES (0, 100.12, bross, 'https://www.bobross.com/content/bob_ross_img.png', 1, 1000)
INSERT INTO distributor (distributorId, balance, username, pfpUrl, failedDeliveries, succeededDeliveries)
    VALUES (0, 31.43, mbuble, 'https://upload.wikimedia.org/wikipedia/commons/f/f9/MichaelBubleSmileeb2011.jpg', 0, 300)

--INSERT INTO route (routeId, parcelId)
--    VALUES (0, 0)
--INSERT INTO route (routeId, parcelId)
--    VALUES (1, 1)
--
--INSERT INTO routeEvent (leaveTime, arrivalTime, nextLockerId, currLockerId, routeId, parcelId, userDoing)
--    VALUES ()