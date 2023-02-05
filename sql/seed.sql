--INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.50073085460111, -0.18378635786638767);
--INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.50025666086443, -0.17269274202952095);
--INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.50464443426626, -0.174902882077271);
--INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.5109679594428, -0.17566443451947997);
--INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.51524263671098, -0.16861754808597962);
--INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.50562314209575, -0.1874391721539224);
--INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.518807437201076, -0.17271952636313428);
--
--INSERT INTO distributor ( balance, username, pfpUrl, failedDeliveries, succeededDeliveries)
--    VALUES ( 100.12, 'bross', 'https://www.bobross.com/content/bob_ross_img.png', 1, 1000);
--INSERT INTO distributor ( balance, username, pfpUrl, failedDeliveries, succeededDeliveries)
--    VALUES ( 31.43, 'mbuble', 'https://upload.wikimedia.org/wikipedia/commons/f/f9/MichaelBubleSmileeb2011.jpg', 0, 300);
--
---- in delivery
---- INSERT INTO parcel(dateIntoSystem, dateIntoLocker, lockerIn, destinationLocker, inTransit)
----    VALUES ('2023-02-05 11:23:44', '2023-02-06 1:52:31', 1, 7, false);
---- delivered
----INSERT INTO parcel(parcelId, dateIntoSystem, dateIntoLocker, lockerIn, destinationLocker, inTransit)
----    VALUES (1, '2023-02-03 9:12:00', '2023-02-03 18:41:59', 6, 1, false)
---- to be delivered
----INSERT INTO parcel(parcelId, dateIntoSystem, dateIntoLocker, lockerIn, destinationLocker, inTransit)
----    VALUES (2, '2023-02-04 10:11:04', '2023-02-04 10:02:36', 3, 4, false)
--
--INSERT INTO journey ( distributorId) VALUES ( 1);
--INSERT INTO journey ( distributorId) VALUES ( 2);
--
--INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
--    VALUES (0, 1, '8:25:00', 51.516527191127125, -0.1708326439641144);
--INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
--    VALUES (1, 1, '9:14:18', 51.50666838287783, -0.17104711045078022);
--INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
--    VALUES (2, 1, '10:54:32', 51.49885223966222, -0.17679456094944745);
--
--INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
--    VALUES (0, 2, '16:57:42', 51.4999, -0.1781);
--INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
--    VALUES (1, 2, '18:05:01', 51.5007, -0.1246);
--
--




--INSERT INTO route (routeId, parcelId)
--    VALUES (0, 0)
-- INSERT INTO route (parcelId) VALUES (1);
--
-- Garbage
-- INSERT INTO routeEvent (leaveTime, arrivalTime, nextLockerId, currLockerId, routeId, parcelId, userDoing, journeyPointStartId, journeyPointEndId)
--    VALUES ('2023-02-05 11:23:44', '2023-02-05 11:23:46', 7, 1, 1, 1,  2, 4, 5);




INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.4999, -0.1781);
INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.4994, -0.1771);
INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.5009, -0.1774);
INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.4998, -0.1757);

INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.5013, -0.1248);
INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.5014, -0.1248);
INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.5007, -0.1246);

INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.4507, -0.1246);


INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.5114, -0.1921);
INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.5052, -0.1521);

INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.5220, -0.1421);
INSERT INTO locker( capacity, latitude, longitude) VALUES (200, 51.5200, -0.1621);


INSERT INTO distributor ( balance, username, pfpUrl, failedDeliveries, succeededDeliveries)
   VALUES ( 100.12, 'bross', 'https://www.bobross.com/content/bob_ross_img.png', 1, 1000);
INSERT INTO distributor ( balance, username, pfpUrl, failedDeliveries, succeededDeliveries)
   VALUES ( 31.43, 'mbuble', 'https://upload.wikimedia.org/wikipedia/commons/f/f9/MichaelBubleSmileeb2011.jpg', 0, 300);


-- in delivery
-- INSERT INTO parcel(dateIntoSystem, dateIntoLocker, lockerIn, destinationLocker, inTransit)
--    VALUES ('2023-02-05 11:23:44', '2023-02-06 1:52:31', 1, 7, false);
-- delivered
--INSERT INTO parcel(parcelId, dateIntoSystem, dateIntoLocker, lockerIn, destinationLocker, inTransit)
--    VALUES (1, '2023-02-03 9:12:00', '2023-02-03 18:41:59', 6, 1, false)
-- to be delivered
-- INSERT INTO parcel(parcelId, dateIntoSystem, dateIntoLocker, lockerIn, destinationLocker, inTransit)
--    VALUES (2, '2023-02-04 10:11:04', '2023-02-04 10:02:36', 3, 5, false);


INSERT INTO journey ( distributorId) VALUES ( 1);
INSERT INTO journey ( distributorId) VALUES ( 2);


INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
   VALUES (0, 1, '11:25:00', 51.5000, -0.1781);
INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
   VALUES (1, 1, '11:55:00', 51.5012, -0.1248);
INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
   VALUES (0, 2, '17:14:18', 51.4996, -0.1782);
INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
   VALUES (1, 2, '17:54:32', 51.2006, -0.1245);
INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
   VALUES (2, 2, '18:01:25', 51.4511, -0.1246);

-- INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
--    VALUES (0, 2, '16:57:42', 51.4999, -0.1781);
-- INSERT INTO journeyPoint(ordinalNumber, journeyId, arrivalTime, latitude, longitude)
--    VALUES (1, 2, '18:05:01', 51.5007, -0.1246);








--INSERT INTO route (routeId, parcelId)
--    VALUES (0, 0)
-- INSERT INTO route (parcelId) VALUES (1);


-- Garbage
-- INSERT INTO routeEvent (leaveTime, arrivalTime, nextLockerId, currLockerId, routeId, parcelId, userDoing, journeyPointStartId, journeyPointEndId)
--    VALUES ('2023-02-05 11:23:44', '2023-02-05 11:23:46', 7, 1, 1, 1,  2, 4, 5);
