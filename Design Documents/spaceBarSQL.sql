CREATE TABLE "drinks" (
  "drink_id" SERIAL PRIMARY KEY,
  "drink_name" varchar,
  "description" varchar,
  "price" varchar,
  "drink_type" varchar,
  "ingredients" varchar[]
);
