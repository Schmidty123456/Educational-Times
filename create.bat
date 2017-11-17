CREATE TABLE educational(
   number char(10),
   etvol integer,
   etdate char(20),
   proposer char(60),
   solver char(150),
   etvols char(40),
   etdates char(80),
   mqvol char(40),
   qtype char(10),
   PRIMARY KEY (number, proposer)
);

