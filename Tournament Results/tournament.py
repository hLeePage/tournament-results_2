#!/usr/bin/env python
# 
# tournament.py -- implementation of a simple Swiss-system tournament
#

import psycopg2

psycopg2.connect("dbname=tournament")

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    SQL = "DELETE FROM matches;"
    c.execute(SQL)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    SQL = "DELETE FROM players;"
    c.execute(SQL)
    conn.commit()
    conn.close()

    
def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    SQL = "SELECT COUNT(id) FROM players;"
    c.execute(SQL)
    result = c.fetchone()[0]    
    conn.close()
    return result

    
def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    SQL = "INSERT INTO players (name) VALUES (%s);"
    data = (name,)
    c.execute(SQL, data)
    conn.commit()   
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    SQL = "SELECT * FROM standings;"
    c.execute(SQL)
    result = c.fetchall()
    conn.close()
    return result
    


def reportMatch(winner, loser):
    """Records the outcome of a single match between players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    SQL = "INSERT INTO matches VALUES (%s, %s, %s);"
    data = (winner, loser, winner)
    c.execute(SQL, data)
    conn.commit()
    conn.close()
    


 
def swissPairings():

    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
        
    conn = connect()
    c = conn.cursor()
    SQL = "SELECT * FROM wins;"
    c.execute(SQL)
    result = c.fetchall()
    pairs = []
    for i in range(0, len(result), 2):
        pairs.append((result[i][0], result[i][1], result[i+1][0], result[i+1][1]))
    return pairs
    conn.close()

  

