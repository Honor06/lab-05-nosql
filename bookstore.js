// Step 2: 
// use bookstore 
db = db.getSiblingDB("bookstore")

// Step 3: load authors.json
// paste your drop and insertMany commands here
db.authors.drop()
doc = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(doc)
// Step 4: load books.json
// paste your drop and insertMany commands here
db.books.drop()
doc = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(doc)
// Step 5: list authors and books
// paste your find commands here
db.authors.find()
db.books.find()
// Step 6: insert two new books
// paste your insert commands here
db.books.insertMany([
   {
     title: "The Lord of the Rings",
     published_year: 1954,
     author_ids: ["author_004"]
   },
   {
     title: "Jane Eyre",
     published_year: 1847,
     author_ids: ["author_005"]
   }
 ])

// Step 7: add missing authors
// paste your insert commands here
db.authors.insertMany([
   {
     _id: "author_004",
     name: "J.R.R. Tolkien",
     nationality: "British",
     bio: {
       short: "Author of The Hobbit and The Lord of the Rings.",
       long: "J.R.R. Tolkien was a British writer and academic best known for his fantasy novels, including The Hobbit, published in 1937."
     }
   },
   {
     _id: "author_005",
     name: "Charlotte Bronte",
     nationality: "British",
     bio: {
       short: "Author of Jane Eyre and other gothic novels.",
       long: "Charlotte Bronte (1816–1855) was an English novelist and poet whose best-known work, Jane Eyre, explores themes of independence and love."
     }
   }
 ])

// Step 8: filter books by a list of authors
// paste your find command here
db.books.find({ author_ids: { $in: ["author_001", "author_004"] } })

