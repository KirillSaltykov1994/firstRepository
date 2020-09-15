BEGIN;
CREATE database TestDB;
--
-- Create model Choice
--
CREATE TABLE "forStudents_choice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "choice_text" varchar(200) NOT NULL, "votes" integer NOT NULL);
--
-- Create model Question
--
CREATE TABLE "forStudents_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "question_text" varchar(200) NOT NULL, "pub_date" datetime NOT NULL);
--
-- Add field question to choice
--
ALTER TABLE "forStudents_choice" RENAME TO "forStudents_choice__old";
CREATE TABLE "forStudents_choice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "choice_text" varchar(200) NOT NULL, "votes" integer NOT NULL, "question_id" integer NOT NULL REFERENCES "forStudents_question" ("id"));
INSERT INTO "forStudents_choice" ("choice_text", "votes", "id", "question_id") SELECT "choice_text", "votes", "id", NULL FROM "forStudents_choice__old";
DROP TABLE "forStudents_choice__old";
CREATE INDEX "forStudents_choice_question_id_1f5a0a97" ON "forStudents_choice" ("question_id");
COMMIT;
