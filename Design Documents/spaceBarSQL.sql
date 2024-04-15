CREATE TABLE IF NOT EXISTS "drinks" (
  "drink_id" SERIAL PRIMARY KEY,
  "drink_name" varchar UNIQUE,
  "description" varchar,
  "price" varchar,
  "drink_type" varchar,
  "ingredients" varchar[]
);

CREATE TABLE IF NOT EXISTS "users" (
  "user_id" SERIAL PRIMARY KEY,
  "username" varchar UNIQUE NOT NULL,
  "password" varchar NOT NULL,
  "email" varchar UNIQUE NOT NULL
);
