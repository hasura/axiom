CREATE DATABASE emergent_holotel;

\c emergent_holotel;

CREATE TABLE Calls (
    CallID SERIAL PRIMARY KEY,
    CustomerID INT NOT NULL,
    DeviceID INT NOT NULL,
    TimeStamp TIMESTAMP WITH TIME ZONE NOT NULL,
    Duration INT NOT NULL,
    CallType VARCHAR(50),
    ReceiverNumber VARCHAR(15),
    NodeId INT
);

CREATE TABLE Texts (
    TextID SERIAL PRIMARY KEY,
    CustomerID INT NOT NULL,
    DeviceID INT NOT NULL,
    TimeStamp TIMESTAMP WITH TIME ZONE NOT NULL,
    MessageType VARCHAR(50),
    ReceiverNumber VARCHAR(15),
    NodeId Int
);
