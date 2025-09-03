CREATE TABLE ged_documents (
  doc_id NUMBER PRIMARY KEY,
  original_name VARCHAR2(255) NOT NULL,
  storage_path VARCHAR2(4000) NOT NULL,
  content_type VARCHAR2(100),
  size_bytes NUMBER,
  created_by VARCHAR2(100),
  created_at TIMESTAMP DEFAULT SYSTIMESTAMP,
  ocr_status VARCHAR2(20) DEFAULT 'PENDING',
  full_text CLOB,
  doc_status VARCHAR2(20) DEFAULT 'ACTIVE'
);

CREATE SEQUENCE ged_documents_seq
  START WITH 1
  INCREMENT BY 1
  NOCACHE
  NOCYCLE;

CREATE OR REPLACE TRIGGER ged_documents_trigger
BEFORE INSERT ON ged_documents
FOR EACH ROW
BEGIN
  IF :NEW.doc_id IS NULL THEN
    SELECT ged_documents_seq.NEXTVAL INTO :NEW.doc_id FROM dual;
  END IF;
END;
/


-------------------------------------------------

CREATE TABLE ged_metadata (
  meta_id NUMBER PRIMARY KEY,
  doc_id NUMBER REFERENCES ged_documents(doc_id) ON DELETE CASCADE,
  meta_key VARCHAR2(100),
  meta_value VARCHAR2(4000)
);

CREATE SEQUENCE ged_metadata_seq
  START WITH 1
  INCREMENT BY 1
  NOCACHE
  NOCYCLE;

CREATE OR REPLACE TRIGGER ged_metadata_trigger
BEFORE INSERT ON ged_metadata
FOR EACH ROW
BEGIN
  IF :NEW.meta_id IS NULL THEN
    SELECT ged_metadata_seq.NEXTVAL INTO :NEW.meta_id FROM dual;
  END IF;
END;
/


----------------------------------------------

CREATE TABLE ged_users (
    user_id NUMBER PRIMARY KEY,
    username VARCHAR2(50) UNIQUE NOT NULL,
    password VARCHAR2(100) NOT NULL,
    role VARCHAR2(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT SYSTIMESTAMP
);

CREATE SEQUENCE ged_users_seq
  START WITH 1
  INCREMENT BY 1
  NOCACHE
  NOCYCLE;

CREATE OR REPLACE TRIGGER ged_users_trigger
BEFORE INSERT ON ged_users
FOR EACH ROW
BEGIN
  IF :NEW.user_id IS NULL THEN
    SELECT ged_users_seq.NEXTVAL INTO :NEW.user_id FROM dual;
  END IF;
END;
/

-----------------------------------

INSERT INTO ged_users (username, password, role)
VALUES ('admin', 'admin123', 'admin');