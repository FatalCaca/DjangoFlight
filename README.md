# Réservation de vols
WebService pour la réservation de vols

* Frédéric TURPIN
* Simon BALLUAIS

17 avril 2015

# REST API

## Prérequis

Il est possible d'utiliser le WebService au format _JSON_. Pour cela, vous devrez impérativement passer en en-tête de toutes vos requêtes le paramètre `Content-Type` avec la valeur `application/json`. Exemple de requête possible :

```
GET /flights/ HTTP/1.1
Content-Type: application/json
```

## Données disponibles

| Vol (Flight)          |  Type  |
|-----------------------|--------|
| pk                    | entier |
| departure             | chaîne |
| arrival               | chaîne |
| total_available_seats | entier |
| date                  | chaîne |
| flightClasses         | tableau de Classes |

| Classe (FlightClass) |  Type  |
|-----------------------|--------|
| pk                    | entier |
| text                  | chaîne |
| available_seats       | entier |
| price                 |  réel  |

| Réservation           |  Type  |
|-----------------------|--------|
| pk                    | entier |
| flight                | entier |
| flight_class          | entier |
| price                 |  réel  |

![Modèle des données de l'API](doc/data-api.png)
Diagramme des données de l'API.

## Vols
### Tous les vols
Obtenir tous les vols disponibles :

```
GET /flights/
```

Retourne une liste d'objets :

```json
[
	{
		"pk": 1,
		"departure": "London (UK)",
		"destination": "Beijing (CN)",
		"total_available_seats": 100,
		"date": "2015-04-22T12:10:00"
	},
	{
		"pk": 2,
		"departure": "London (UK)",
		"destination": "Beijing (CN)",
		"total_available_seats": 100,
		"date": "2015-04-22T12:10:00"
	},
]
```

## Vols disponibles
### Obtenir tous les vols disponibles :

```
GET /available_flights/
```

Retourne une liste d'objets :

```json
[
	{
		"pk": 1,
		"departure": "London (UK)",
		"destination": "Beijing (CN)",
		"total_available_seats": 100,
		"date": "2015-04-22T12:10:00"
	},
	{
		"pk": 2,
		"departure": "London (UK)",
		"destination": "Beijing (CN)",
		"total_available_seats": 100,
		"date": "2015-04-22T12:10:00"
	},
]
```

### Détail des vols
Obtenir les détails d'un vol en particulier :

```
GET /flights/<pk>/
```

Retourne un vol :

```json
{
	"pk": 1,
	"departure": "London (UK)",
	"destination": "Beijing (CN)",
	"total_available_seats": 100,
	"date": "2015-04-22T12:10:00",
	"flightClasses": [
		{
			"pk": 1,
			"text": "Classe business",
			"seats_amount": 50,
			"price": 65.52
		},
		// ...
	]
}
```

## Reservations

Ces données ne sont accessibles qu'avec un jeton valable.

### Réservations prises

Obtenir tous les vols disponibles :

```
GET /reservations/
```

Retourne une liste d'objets :

```json
[
	{
		"pk": 1,
		"flight": 1,
		"flightClass": 1
	},
	{
		"pk": 2,
		"flight": 3,
		"flightClass": 2
	},
]
```

### Nouvelle réservation

Obtenir tous les vols disponibles :

```
PUT /reservation/
POST /reservation/
```

Demande un objet construit comme suit :

```json
{
	"flight_id": 1,
	"flight_class_id": 1
}
```

Retourne un objet :

```json
{
	"pk": 5,
	"status": "OK",
	"message": "Enregistrement réussi"
}
```

### Annulation

Annuler une réservation pour un vol :

```
POST /reservation/<pk_reservation>/cancel/
```

Retourne un objet :

```json
{
	"status": "OK",
	"message": "Réservation annulée",
	"id": 1
}
```

# Token Authentication

Pour les actions et échanges d'informations propres à un utilisateur, un jeton d'accès doit être utilisé. Ce jeton est généré et envoyé par le site via la page `/api-token-auth/`. 

Opération :

```
POST /api-token-auth/
```

Demande un objet construit comme suit :

```json
{
	"username": "john",
	"password": "P@ssw0rd"
}
```

La réponse contiendra seulement la clef d'accès si le compte est correct.

```json
{
	"token": "56c9dc878c93479d50330ccbf8888aeaf566988a"
}
```

Pour utiliser cette clef d'accès, il faudra l'inclure dans l'en-tête dans la propriété `Authorization` précédée de `Token `. Exemple de requête :

```
GET /reservations/ HTTP/1.1
Content-Type: application/json
Content-Length: 41
Authorization: Token 56c9dc878c93479d50330ccbf8888aeaf566988a
```
