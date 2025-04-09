import src.castaway
class Player():
    def __init__(self, name : str = "Frodo Baggins", castaway_names : list[str] = None, winner_pick : str = "Sauron",
                merge_pickup : str = None, merge_drop : str = None, merge_week : int = None):

        self.__name = name
        self.__castaway_names = castaway_names
        self.__winner_pick = winner_pick
        self.__merge_pickup = merge_pickup
        self.__merge_drop = merge_drop
        self.__merge_week = merge_week

    def points(self, castaway_lookup: dict[str,src.castaway.Castaway]) -> int:

        total_points = 0

        for name in self.__castaway_names:
            
            #Check if dropped at merge
            if name == self.__merge_drop:
                total_points += (castaway_lookup.get(name)).get_merge_points(self.__merge_week, False)
            else:
                total_points += (castaway_lookup.get(name)).get_total_points()

        #Add merge pickup points
        if self.__merge_pickup:
            total_points += (castaway_lookup.get(self.__merge_pickup)).get_merge_points(self.__merge_week, True)

        #Winner Bonus
        if (castaway_lookup.get(self.__winner_pick)).is_winner(): total_points+= 30

        return total_points
    
    def name(self) -> str:
        return self.__name
    
    def castaways(self) -> list[str]:
        return self.__castaway_names
    
    def winner_pick(self) -> str:
        return self.__winner_pick
    
    def merge_pickup(self) -> str:
        return self.__merge_pickup
    
    def merge_drop(self) -> str:
        return self.__merge_drop
    
    def __str__(self) -> str:
        output = f"Player: {self.__name}\nCastaways: {', '.join(self.__castaway_names)}\nWinner Pick: {self.__winner_pick}"
        if self.__merge_pickup or self.__merge_drop or self.__merge_week is not None:
            output += f"\nMerge Pickup: {self.__merge_pickup}"
            output += f"\nMerge Drop: {self.__merge_drop}"
            output += f"\nMerge Week: {self.__merge_week}"
        return output

    def __repr__(self) -> str:
        return (
            f"Player(name={self.__name!r}, castaways={self.__castaway_names!r}, "
            f"winner_pick={self.__winner_pick!r}, merge_pickup={self.__merge_pickup!r}, "
            f"merge_drop={self.__merge_drop!r}, merge_week={self.__merge_week!r})"
        )

