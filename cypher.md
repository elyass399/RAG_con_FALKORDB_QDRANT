# NODI
-- nodo qualsiasi
(n)

-- nodo con tipo
(n:Concept)

-- nodo con proprietà
(n:Concept {name: "ANNIBALE"})

-- nodo con variabile e tipo
(c:Chunk)
# RELAZIONI
-- direzione uscente
(a)-[:ATTRAVERSA]->(b)

-- direzione entrante
(a)<-[:ATTRAVERSA]-(b)

-- bidirezionale
(a)-[:ATTRAVERSA]-(b)

-- qualsiasi relazione
(a)-[r]->(b)

-- relazione con variabile
(a)-[r:CONTIENE]->(b)

-- profondità variabile
(a)-[r*1..2]->(b)   -- da 1 a 2 hop
(a)-[r*]->(b)       -- qualsiasi profondità

# MATCH (trova)

MATCH (n:Concept) RETURN n

MATCH (n:Concept {name: "ANNIBALE"}) RETURN n

MATCH (a)-[r]->(b) RETURN a.name, type(r), b.name

# WHERE (filtra)

MATCH (n:Concept)
WHERE n.name = "ANNIBALE"
RETURN n

WHERE n.name CONTAINS "ANNI"      -- contiene
WHERE n.manual CONTAINS "STORIA"  -- contiene
WHERE n.name STARTS WITH "A"      -- inizia con
WHERE n.score > 0.75              -- numerico

# MERGE ( crea se non esiste)

-- crea nodo se non esiste
MERGE (n:Concept {name: "ANNIBALE"})

-- crea relazione se non esiste
MERGE (a)-[:ATTRAVERSA]->(b)

-- ON CREATE → solo alla creazione
MERGE (n:Concept {name: "ANNIBALE"})
ON CREATE SET n.manual = "STORIA"

-- ON MATCH → solo se già esiste
MERGE (n:Concept {name: "ANNIBALE"})
ON MATCH SET n.resolved = true

# CREATE (crea sempre)

CREATE (n:Concept {name: "ANNIBALE"})

CREATE (a)-[:ATTRAVERSA]->(b)

# SET (aggiorna proprietà)

MATCH (n:Concept {name: "ANNIBALE"})
SET n.resolved = true

SET n.manual = n.manual + "|STORIA"

# DELETE (cancella)

-- cancella nodo (solo se senza relazioni)
MATCH (n:Concept {name: "ANNIBALE"})
DELETE n

-- cancella nodo + tutte le relazioni
MATCH (n:Concept {name: "ANNIBALE"})
DETACH DELETE n

-- cancella solo relazioni
MATCH ()-[r:SINONIMO_DI]->()
DELETE r

# RETURN (cosa restituire):

RETURN n                       -- nodo intero
RETURN n.name                  -- proprietà
RETURN type(r)                 -- tipo relazione
RETURN count(n)                -- conta
RETURN n.name, type(r), m.name

# LIMIT/ORDER

RETURN n LIMIT 10
ORDER BY n.name
ORDER BY n.name DESC

# Le query che usiamo piu

-- conta tutti i nodi
MATCH (n) RETURN count(n)

-- trova chunk per id
MATCH (ch:Chunk {id: $id}) RETURN ch.content

-- relazioni uscenti depth 2
MATCH (c:Concept {name: $name})-[r*1..2]->(m:Concept)
RETURN c.name, type(r[0]), m.name

-- chunk collegati a concept
MATCH (ch:Chunk)-[:CONTIENE]->(c:Concept {name: $name})
RETURN ch.id

-- cancella tutti i SINONIMO_DI
MATCH ()-[r:SINONIMO_DI]->() DELETE r

-- cancella tutto
MATCH (n) DETACH DELETE n

--trova tutto--
MATCH (n)-[e]->(m) RETURN n,e,m LIMIT 100000

MATCH  p=()-[r:SINONIMO_DI]->() RETURN p LIMIT 100000
MATCH (n:Concept {name: "ANNIBALE"}) RETURN n