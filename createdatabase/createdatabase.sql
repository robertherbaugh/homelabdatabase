-- Create Network Table
CREATE TABLE Network (
    NetworkID BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    NetworkName VARCHAR(255),
    NetworkVLAN INT,
    IPSpace VARCHAR(18),
    SubnetMask VARCHAR(18)
);

-- Create Servers Table
CREATE TABLE Servers (
    ServerID BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ServerName VARCHAR(255),
    IPAddress VARCHAR(15),
    Location VARCHAR(255),
    Description TEXT,
    NetworkID BIGINT UNSIGNED,
    Type VARCHAR(50),
    OS VARCHAR(50),
    FOREIGN KEY (NetworkID) REFERENCES Network(NetworkID)
);

-- Create Services Table
CREATE TABLE Services (
    ServiceID BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ServerID BIGINT UNSIGNED,
    NetworkID BIGINT UNSIGNED,
    ServiceName VARCHAR(255),
    Port INT,
    Status VARCHAR(50),
    IP VARCHAR(15),
    WazuhAgentInstalled BOOLEAN,
    FQDN VARCHAR(255),
    CloudflareProxyConfigured BOOLEAN,
    ReverseProxyConfigured BOOLEAN,
    LDN VARCHAR(255),
    DNSConfigured BOOLEAN,
    HttpsEnabled BOOLEAN,
    FOREIGN KEY (ServerID) REFERENCES Servers(ServerID),
    FOREIGN KEY (NetworkID) REFERENCES Network(NetworkID)
);

-- Create Credentials Table
CREATE TABLE Credentials (
    CredentialID BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255),
    Password TEXT,
    LastUpdated DATE,
    MFAEnabled BOOLEAN,
    MFASource VARCHAR(50),
    SSO BOOLEAN,
    AccountType VARCHAR(50),
    CredName VARCHAR(255) UNIQUE
);

-- Create ServerCredential Join Table
CREATE TABLE ServerCredential (
    ServerID BIGINT UNSIGNED,
    CredentialID BIGINT UNSIGNED,
    PRIMARY KEY (ServerID, CredentialID),
    FOREIGN KEY (ServerID) REFERENCES Servers(ServerID),
    FOREIGN KEY (CredentialID) REFERENCES Credentials(CredentialID)
);

-- Create ServiceCredential Join Table
CREATE TABLE ServiceCredential (
    ServiceID BIGINT UNSIGNED,
    CredentialID BIGINT UNSIGNED,
    PRIMARY KEY (ServiceID, CredentialID),
    FOREIGN KEY (ServiceID) REFERENCES Services(ServiceID),
    FOREIGN KEY (CredentialID) REFERENCES Credentials(CredentialID)
);

-- Create ServerService Join Table
CREATE TABLE ServerService (
    ServerID BIGINT UNSIGNED,
    ServiceID BIGINT UNSIGNED,
    PRIMARY KEY (ServerID, ServiceID),
    FOREIGN KEY (ServerID) REFERENCES Servers(ServerID),
    FOREIGN KEY (ServiceID) REFERENCES Services(ServiceID)
);