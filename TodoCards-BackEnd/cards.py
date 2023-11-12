# This is the script cards.py, which will be handling all-things cards and subcards
# This includes: getting, creating, editing, finishing, and deleting cards and subcards
# Author: Panisara S 6422781326, Nachat K 6422770774

# using this access check function for the "create card" feature
#from decks import check_deck_view_access, check_deck_edit_access
import decks

# Utility function to check access for your card_id
def check_card_view_access(mydb, card_id, username):
    mycursor = mydb.cursor()
    mycursor.execute(
        """
            SELECT deckId
            FROM card 
            WHERE cardid = %s
            """, (card_id,)
    )
    
    result = mycursor.fetchall()
    mycursor.close()
    mydb.commit()
    for row in result:
        if (decks.check_deck_view_access(mydb, row[0], username) == True or decks.check_deck_edit_access(mydb, row[0], username) == True):
            return True
    return False


# Utility function to check access for your subcard_id
def check_subcard_view_access(mydb, subcard_id, username):
    mycursor = mydb.cursor()
    mycursor.execute(
        """
            SELECT cardID
            FROM subcard
            WHERE scardid = %s
            """, (subcard_id,)
    )
    
    result = mycursor.fetchall()
    mycursor.close()
    mydb.commit()
    for row in result:
        if (check_card_view_access(mydb, row[0], username) == True or check_card_edit_access(mydb, row[0], username) == True):
            return True
    return False


# Utility function to check access for your card_id
def check_card_edit_access(mydb, card_id, username):
    mycursor = mydb.cursor()
    mycursor.execute(
        """
            SELECT deckId
            FROM card 
            WHERE cardid = %s
            """, (card_id,)
    )
    
    result = mycursor.fetchall()
    mycursor.close()
    mydb.commit()
    for row in result:
        if (decks.check_deck_edit_access(mydb, row[0], username) == True):
            return True
    return False


# Utility function to check access for your subcard_id
def check_subcard_edit_access(mydb, subcard_id, username):
    mycursor = mydb.cursor()
    mycursor.execute(
        """
            SELECT cardID
            FROM subcard
            WHERE scardid = %s
            """, (subcard_id,)
    )
    
    result = mycursor.fetchall()
    mycursor.close()
    mydb.commit()
    for row in result:
        if (check_card_edit_access(mydb, row[0], username) == True):
            return True
    return False

# Retrieve all cards within a deck
# must also check view access of the deck (using check_deck_view_access function)
# Otherwise, returns empty list
def get_cards_list(mydb, deck_id, username):

    if not decks.check_deck_view_access(mydb, deck_id, username):
        return []

    mycursor = mydb.cursor()
    mycursor.execute(
        """
        SELECT 
            cardId, cardName, cardDescription, cardDue, cardIsFinished, cardcolor
        FROM card WHERE deckID = %s
        """, (deck_id,))
    
    result = mycursor.fetchall()
    for i, r in enumerate(result):
        result[i] = {
            "cardId": int(r[0]),
            "cardName": r[1],
            "cardDescription": r[2],
            "cardDue": r[3],
            "cardIsFinished": r[4],
            "cardColor": r[5]
        }
        #print(result[i])

    mycursor.close()
    mydb.commit()
    return result

# Retrieve all subcards within a card
# must also check view access of that card_id
# Otherwise, returns empty list
def get_subcards_list(mydb, card_id, username):
    if not check_card_view_access(mydb, card_id, username):
        return []
    
    mycursor = mydb.cursor()
    mycursor.execute(
        """
        SELECT 
            scardid, scardName, scardIsFinished 
        FROM subcard 
        WHERE cardid = %s
        """, (card_id,))
    
    result = mycursor.fetchall()
    for i, r in enumerate(result):
        result[i] = {
            "subcardId": int(r[0]),  
            "subcardName": r[1],
            "subcardIsFinished": int(r[2]),
        }
        #print(result[i])

    mycursor.close()
    mydb.commit()
    return result

# updates a card by setting isFinished = True
# must also check edit access of that card_id
# returns True if success, False otherwise
def finish_card(mydb, card_id, username):
    if check_card_edit_access(mydb, card_id, username):
        mycursor = mydb.cursor()
        mycursor.execute(
            """
                UPDATE card
                SET cardIsFinished = '1'
                WHERE cardid = %s
                """, (card_id,)
        )
        mycursor.close()
        mydb.commit()
        return True
    return False


# updates a subcard by setting isFinished = True
# must also check edit access of that subcard_id
# returns True if success, False otherwise
def finish_subcard(mydb, subcard_id, username):
    
    if check_subcard_edit_access(mydb, subcard_id, username):
        mycursor = mydb.cursor()
        mycursor.execute(
            """
                UPDATE subcard
                SET scardIsFinished = '1'
                WHERE scardid = %s
                """, (subcard_id,)
        )
        mycursor.close()
        mydb.commit()
        return True
    return False


# updates a card with card_info
# must also check edit access of card_info["cardId"]
# returns True if success, False otherwise
def edit_card(mydb, card_info, username):

    return "Unimplemented"

# updates a subcard with card_info
# must also check edit access
# returns True if success, False otherwise
def edit_subcard(mydb, card_info, username):
    return "Unimplemented"

# creates a new card within the deck
# must also check edit access for that deck_id
# returns True if success, False otherwise
def create_card(mydb, deck_id, card_info, username):
    return "Unimplemented"

# creates a new card within the deck
# must also check edit access for that card_id
# returns True if success, False otherwise
def create_subcard(mydb, card_id, subcard_info, username):
    return "Unimplemented"

# deletes a card within the deck
# must also check edit access for that card_id
# returns True if success, False otherwise
def delete_card(mydb, card_id, username):
    
    if check_card_edit_access(mydb, card_id, username):
        mycursor = mydb.cursor()
        mycursor.execute(
            """
                DELETE FROM card
                WHERE cardid = %s
                """, (card_id,)
        )
        mycursor.close()
        mydb.commit()
        return True
    
    return False
    

# deletes a subcard within the card
# must also check edit access for that subcard_id
# returns True if success, False otherwise
def delete_subcard(mydb, subcard_id, username):

    if check_subcard_edit_access(mydb, subcard_id, username):
        mycursor = mydb.cursor()
        mycursor.execute(
            """
                DELETE FROM subcard
                WHERE scardid = %s
                """, (subcard_id,)
        )
        mycursor.close()
        mydb.commit()
        return True
    
    return False