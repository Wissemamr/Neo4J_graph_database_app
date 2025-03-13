## Requêtes de création (Cypher Code)

### Création des noeuds Movie
```cypher
CREATE
  (:Movie {id: 1, title: 'Inception', genre: 'Sci-Fi', year: 2010}),
  (:Movie {id: 2, title: 'Interstellar', genre: 'Sci-Fi', year: 2014}),
  (:Movie {id: 3, title: 'The Dark Knight', genre: 'Action', year: 2008}),
  (:Movie {id: 4, title: 'Tenet', genre: 'Sci-Fi', year: 2020}),
  (:Movie {id: 5, title: 'Memento', genre: 'Thriller', year: 2000}),
  (:Movie {id: 6, title: 'The Prestige', genre: 'Drama', year: 2006}),
  (:Movie {id: 7, title: 'Dunkirk', genre: 'War', year: 2017}),
  (:Movie {id: 8, title: 'Parasite', genre: 'Drama', year: 2019}),
  (:Movie {id: 9, title: 'The Matrix', genre: 'Sci-Fi', year: 1999}),
  (:Movie {id: 10, title: 'Pulp Fiction', genre: 'Crime', year: 1994}),
  (:Movie {id: 11, title: 'Fight Club', genre: 'Drama', year: 1999}),
  (:Movie {id: 12, title: 'The Godfather', genre: 'Crime', year: 1972}),
  (:Movie {id: 13, title: 'Forrest Gump', genre: 'Drama', year: 1994}),
  (:Movie {id: 14, title: 'The Avengers', genre: 'Action', year: 2012}),
  (:Movie {id: 15, title: 'Avatar', genre: 'Sci-Fi', year: 2009});
```

### Création des noeuds Actor
```cypher
CREATE
  (:Actor {name: 'Leonardo DiCaprio'}),
  (:Actor {name: 'Joseph Gordon-Levitt'}),
  (:Actor {name: 'Christian Bale'}),
  (:Actor {name: 'Matthew McConaughey'}),
  (:Actor {name: 'Anne Hathaway'}),
  (:Actor {name: 'Hugh Jackman'}),
  (:Actor {name: 'Tom Hardy'}),
  (:Actor {name: 'Cillian Murphy'}),
  (:Actor {name: 'Brad Pitt'}),
  (:Actor {name: 'Samuel L. Jackson'}),
  (:Actor {name: 'Marlon Brando'}),
  (:Actor {name: 'Al Pacino'}),
  (:Actor {name: 'Robert Downey Jr.'}),
  (:Actor {name: 'Scarlett Johansson'}),
  (:Actor {name: 'Sigourney Weaver'});
```

### Création des noeuds Director
```cypher
CREATE
  (:Director {name: 'Christopher Nolan'}),
  (:Director {name: 'Quentin Tarantino'}),
  (:Director {name: 'Francis Ford Coppola'}),
  (:Director {name: 'Bong Joon-ho'}),
  (:Director {name: 'James Cameron'});
```

### Création des relations entre Movies et Actors
```cypher
MATCH (m:Movie {id: 1}), (a:Actor {name: 'Leonardo DiCaprio'}) CREATE (m)-[:FEATURES]->(a);
MATCH (m:Movie {id: 2}), (a:Actor {name: 'Matthew McConaughey'}) CREATE (m)-[:FEATURES]->(a);
MATCH (m:Movie {id: 3}), (a:Actor {name: 'Christian Bale'}) CREATE (m)-[:FEATURES]->(a);
MATCH (m:Movie {id: 14}), (a:Actor {name: 'Robert Downey Jr.'}) CREATE (m)-[:FEATURES]->(a);
MATCH (m:Movie {id: 15}), (a:Actor {name: 'Sigourney Weaver'}) CREATE (m)-[:FEATURES]->(a);
```

### Création des relations entre Movies et Directors
```cypher
MATCH (m:Movie {id: 1}), (d:Director {name: 'Christopher Nolan'}) CREATE (m)-[:DIRECTED_BY]->(d);
MATCH (m:Movie {id: 8}), (d:Director {name: 'Bong Joon-ho'}) CREATE (m)-[:DIRECTED_BY]->(d);
MATCH (m:Movie {id: 10}), (d:Director {name: 'Quentin Tarantino'}) CREATE (m)-[:DIRECTED_BY]->(d);
MATCH (m:Movie {id: 12}), (d:Director {name: 'Francis Ford Coppola'}) CREATE (m)-[:DIRECTED_BY]->(d);
MATCH (m:Movie {id: 15}), (d:Director {name: 'James Cameron'}) CREATE (m)-[:DIRECTED_BY]->(d);
```

### Suppression de toute la base
```cypher
MATCH (n)
DETACH DELETE n;
```

---

## CRUD Operations on Neo4j Database

### Trouver tous les films d'un genre spécifique
```cypher
MATCH (m:Movie)
WHERE m.genre = 'Sci-Fi'
RETURN m.title AS MovieTitle, m.year AS ReleaseYear;
```

### Trouver les films réalisés par un directeur spécifique
```cypher
MATCH (m:Movie)-[:DIRECTED_BY]->(d:Director {name: 'Christopher Nolan'})
RETURN m.title AS MovieTitle, m.year AS ReleaseYear;
```

### Trouver tous les acteurs qui ont joué dans un film spécifique
```cypher
MATCH (m:Movie {title: 'Pulp Fiction'})-[r:FEATURES]->(a:Actor)
RETURN m.title AS MovieTitle, type(r) AS RelationshipType, a.name AS ActorName;
```

### Compter le nombre de films par genre
```cypher
MATCH (m:Movie)
RETURN m.genre AS Genre, COUNT(m) AS MovieCount
ORDER BY MovieCount DESC;
```

### Trouver l'acteur le plus fréquent dans les films
```cypher
MATCH (m:Movie)-[:FEATURES]->(a:Actor)
RETURN a.name AS ActorName, COUNT(m) AS MoviesCount
ORDER BY MoviesCount DESC
LIMIT 1;
```

### Trouver tous les films avec plus d'un acteur
```cypher
MATCH (m:Movie)-[:FEATURES]->(a:Actor)
WITH m, COUNT(a) AS actorCount
WHERE actorCount > 1
RETURN m.title AS MovieTitle, actorCount AS ActorCount;
```

### Trouver les films sortis après une certaine année
```cypher
MATCH (m:Movie)
WHERE m.year > 2010
RETURN m.title AS MovieTitle, m.year AS ReleaseYear;
