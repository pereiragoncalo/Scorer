"""Visual visitor allocation, not a claim about real ticket allocations."""
from dataclasses import dataclass

SMALL_CLUB_CAPACITY = 20000
FIRST_GOAL_STAIR_X = -35.5 + 135.5 * 71 / 163
CORNER_STAIR_X = 35.55
STAIR_HALF_WIDTH = .65

@dataclass(frozen=True)
class AwaySector:
    club_capacity: int
    enabled: bool = True

    @property
    def extended(self):
        return self.enabled and self.club_capacity > SMALL_CLUB_CAPACITY

    @property
    def goal_stair_x(self):
        return FIRST_GOAL_STAIR_X if self.extended else CORNER_STAIR_X

    def contains(self, x, tier=0, section='goal'):
        if not self.enabled or tier != 0:return False
        if section == 'corner':return True
        return section == 'goal' and self.extended and self.goal_stair_x + STAIR_HALF_WIDTH < x <= 36.2

    def stair(self, x, y, tier=0, section='goal'):
        if not self.enabled or tier != 0:return False
        if section == 'goal':return abs(x-self.goal_stair_x) <= STAIR_HALF_WIDTH
        if section == 'side':return -4.1 <= y <= -2.85
        return False

    def stewards(self, side_x, near_y, z):
        """Two files on EACH flanking staircase; positions follow every tread."""
        if not self.enabled:return ()
        return ((self.goal_stair_x-.22,near_y-.4,z,'goal',0),
                (self.goal_stair_x+.22,near_y-.4,z,'goal',1),
                (side_x+.4,-3.90,z,'side',0),
                (side_x+.4,-3.35,z,'side',1))
