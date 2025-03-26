class Castaway():
    def __init__(self, name : str = "Paul Atreides"):
        self.__name = name
        self.__weekly_points : dict[int,int] = {}
        self.__winner : bool = False
    
    def set_weekly_points (self, week_number : int, points_earned : int):
        self.__weekly_points[week_number] = points_earned

    def get_total_points (self) -> int :
        return sum(self.__weekly_points.values())
    
    def get_merge_points(self, week_number: int , after_merge : bool) -> int:
        if after_merge:
            return sum(points for week, points in self.__weekly_points.items() if week > week_number)
        else:
            return sum(points for week, points in self.__weekly_points.items() if week <= week_number)
    
    def name(self) -> str:
        return self.__name
    
    def get_weekly_points (self, week_number : int) -> int:
        return self.__weekly_points.get(week_number,0)
    
    def is_winner (self) -> bool:
        return self.__winner
    
    def won (self):
        self.__winner = True

    def __str__(self) -> str:
        """Return a human-readable string representation of the Castaway."""
        points_str = ", ".join(f"Week {w}: {p}" for w, p in sorted(self.__weekly_points.items()))
        if not self.__winner: return f"{self.__name}|Total Points: {self.get_total_points()} ({points_str})"
        return f"{self.__name}|**WINNER**|Total Points: {self.get_total_points()} ({points_str})"

    def __repr__(self) -> str:
        """Return a developer-friendly string representation of the Castaway."""
        return f"Castaway(name={self.__name!r}, winner={self.__winner}, weekly_points={self.__weekly_points})"